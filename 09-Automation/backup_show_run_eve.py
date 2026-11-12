#!/usr/bin/env python3
"""Backup confiavel de 'show running-config' por console Telnet EVE-NG (Cisco IOS).

Sem bibliotecas externas; Python 3.9+.

Exemplos:
    python backup_show_run_eve.py
    python backup_show_run_eve.py --only PE1 PE2 PE3
    python backup_show_run_eve.py --attempts 4 --timeout 180

Proteja o diretorio de backups: as configuracoes e logs podem conter senhas.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import getpass
import os
from pathlib import Path
import re
import socket
import sys
import time

EVE_HOST = "192.168.238.128"
EQUIPAMENTOS = [
    ("CE1", 32769),
    ("PE1", 32770),
    ("CE2", 32771),
    ("PE3", 32772),
    ("CE3", 32773),
    ("RR-P", 32774),
    ("PE2", 32775),
]

# Detecta o prompt no fim do texto (nao em uma linha antiga do buffer).
PROMPT_RE = re.compile(r"(?m)^[ \t]*([A-Za-z0-9_.:/()-]+[>#])[ \t]*$")
PASSWORD_RE = re.compile(r"(?i)(?:^|\n)[ \t]*(?:password|senha):[ \t]*$")
USERNAME_RE = re.compile(r"(?i)(?:^|\n)[ \t]*(?:username|login):[ \t]*$")
MORE_RE = re.compile(r"(?i)--More--|<---\s*More\s*--->|\(more\)")
ANSI_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
HEADER_RE = re.compile(r"(?mi)^[ \t]*Current configuration\s*:\s*\d+\s+bytes[ \t]*$")
END_RE = re.compile(r"(?m)^end[ \t]*$")


def normalizar(raw: bytes | str) -> str:
    if isinstance(raw, bytes):
        raw = raw.decode("latin1", errors="replace")
    raw = ANSI_RE.sub("", raw).replace("\r\n", "\n").replace("\r\x00", "\n").replace("\r", "\n")
    raw = MORE_RE.sub("", raw)
    resultado = []
    for ch in raw:
        if ch == "\b":
            if resultado and resultado[-1] != "\n":
                resultado.pop()
        elif ch in "\t\n" or " " <= ch <= "~" or ord(ch) >= 160:
            resultado.append(ch)
    return "".join(resultado)


def ultimo_prompt(texto: str) -> str | None:
    """Somente considera o prompt quando esta na ULTIMA linha."""
    m = list(PROMPT_RE.finditer(texto))
    if m and not texto[m[-1].end():].strip():
        return m[-1].group(1)
    return None


class Console:
    IAC, DONT, DO, WONT, WILL, SB, SE = 255, 254, 253, 252, 251, 250, 240

    def __init__(self, host: str, port: int, timeout: float, idle: float):
        self.host, self.port = host, port
        self.timeout, self.idle = timeout, idle
        self.sock: socket.socket | None = None
        self.state = "normal"
        self.iac_cmd = 0
        self.last_response = ""

    def __enter__(self):
        self.sock = socket.create_connection((self.host, self.port), timeout=12)
        self.sock.settimeout(0.6)
        return self

    def __exit__(self, *args):
        if self.sock is not None:
            self.sock.close()

    def enviar(self, texto: str = ""):
        assert self.sock is not None
        self.sock.sendall(texto.encode("utf-8") + b"\r\n")

    def _telnet(self, dados: bytes) -> bytes:
        """Negocia opcoes basicas do Telnet sem depender do telnetlib (Python 3.13)."""
        out = bytearray()
        for b in dados:
            if self.state == "normal":
                if b == self.IAC:
                    self.state = "iac"
                else:
                    out.append(b)
            elif self.state == "iac":
                if b == self.IAC:
                    out.append(b)
                    self.state = "normal"
                elif b in (self.DO, self.DONT, self.WILL, self.WONT):
                    self.iac_cmd = b
                    self.state = "option"
                elif b == self.SB:
                    self.state = "subneg"
                else:
                    self.state = "normal"
            elif self.state == "option":
                # Recusa extensoes opcionais e evita enviar os bytes de negociacao ao IOS.
                if self.iac_cmd == self.DO:
                    self.sock.sendall(bytes([self.IAC, self.WONT, b]))
                elif self.iac_cmd == self.WILL:
                    self.sock.sendall(bytes([self.IAC, self.DONT, b]))
                self.state = "normal"
            elif self.state == "subneg":
                if b == self.IAC:
                    self.state = "subneg_iac"
            elif self.state == "subneg_iac":
                self.state = "normal" if b == self.SE else "subneg"
        return bytes(out)

    def ler(self, *, autenticar: bool = False, estimular: bool = False) -> tuple[str, str]:
        """Le ate o prompt (ou pedido de login/senha quando autenticar=True)."""
        assert self.sock is not None
        prazo = time.monotonic() + self.timeout
        ultimo_dado = time.monotonic()
        ultimo_enter = time.monotonic()
        tentativas_enter = 0
        bruto = bytearray()
        ultima_paginacao = -1

        while time.monotonic() < prazo:
            try:
                bloco = self.sock.recv(65536)
                if not bloco:
                    raise ConnectionError("Conexao Telnet encerrada pelo console")
            except socket.timeout:
                bloco = b""

            if bloco:
                parte = self._telnet(bloco)
                bruto.extend(parte)
                ultimo_dado = time.monotonic()
                if len(bruto) > 5_000_000:
                    raise RuntimeError("Saida maior que 5MB; interrompido por seguranca")

                texto_bruto = bruto.decode("latin1", errors="replace")
                paginacoes = list(MORE_RE.finditer(texto_bruto))
                if paginacoes and paginacoes[-1].start() > ultima_paginacao:
                    ultima_paginacao = paginacoes[-1].start()
                    self.sock.sendall(b" ")
                    continue

                limpo = normalizar(texto_bruto)
                self.last_response = limpo
                prompt = ultimo_prompt(limpo)
                if prompt:
                    return limpo, "prompt"
                if autenticar and PASSWORD_RE.search(limpo):
                    return limpo, "password"
                if autenticar and USERNAME_RE.search(limpo):
                    return limpo, "username"
            else:
                # Apos reboot alguns roteadores exibem banner e aguardam Enter.
                # Limita o numero de nudges e apenas na leitura inicial.
                if (estimular and tentativas_enter < 3
                        and time.monotonic() - max(ultimo_enter, ultimo_dado) >= 2):
                    self.enviar()
                    ultimo_enter = time.monotonic()
                    tentativas_enter += 1
                if bruto and time.monotonic() - ultimo_dado > self.idle:
                    raise TimeoutError(f"Sem resposta por {self.idle:g}s; trecho final: {self.last_response[-180:]!r}")

        raise TimeoutError(f"Timeout total {self.timeout:g}s; trecho final: {self.last_response[-180:]!r}")

    def preparar(self, autenticacao: "Credenciais"):
        # Nao envia Enter imediatamente: se o console ja imprimiu o prompt,
        # um segundo prompt pode ficar no buffer e confundir a etapa enable.
        resposta, tipo = self.ler(autenticar=True, estimular=True)
        for _ in range(6):
            if tipo == "username":
                self.enviar(autenticacao.usuario())
            elif tipo == "password":
                self.enviar(autenticacao.senha_login())
            else:
                break
            resposta, tipo = self.ler(autenticar=True)
        if tipo != "prompt":
            raise RuntimeError("Nao foi possivel chegar ao prompt do equipamento")

        prompt = ultimo_prompt(resposta)
        if prompt is None:
            raise RuntimeError("Prompt Cisco nao identificado")
        if prompt.endswith(">"):
            self.enviar("enable")
            resposta, tipo = self.ler(autenticar=True)
            if tipo == "password":
                self.enviar(autenticacao.senha_enable())
                resposta, tipo = self.ler(autenticar=True)
            prompt = ultimo_prompt(resposta)
            if tipo != "prompt" or prompt is None or not prompt.endswith("#"):
                raise RuntimeError("Nao entrou em modo privilegiado: verifique enable/secret")
        elif not prompt.endswith("#"):
            raise RuntimeError(f"Prompt nao esperado: {prompt!r}")

        # Executar a cada conexao: depois do reboot o terminal volta a paginar.
        self.executar("terminal length 0", exigir_sucesso=True)
        # 'terminal width' e opcional em alguns IOS; se nao suportado, ignorar.
        self.executar("terminal width 512", exigir_sucesso=False)

    def executar(self, comando: str, exigir_sucesso: bool = False) -> str:
        self.enviar(comando)
        resposta, tipo = self.ler()
        if tipo != "prompt":
            raise RuntimeError(f"Nao retornou prompt apos {comando}")
        if exigir_sucesso and ("% Invalid input" in resposta or "% Unrecognized" in resposta):
            raise RuntimeError(f"Comando nao suportado: {comando}")
        return resposta


class Credenciais:
    """Consulta variaveis de ambiente ou pergunta com getpass sem expor senha."""

    def __init__(self):
        self._login = os.environ.get("EVE_LOGIN_PASSWORD")
        self._enable = os.environ.get("EVE_ENABLE_PASSWORD")
        self._usuario = os.environ.get("EVE_LOGIN_USERNAME")

    def usuario(self) -> str:
        if self._usuario is None:
            self._usuario = input("Usuario do console Cisco: ").strip()
        return self._usuario

    def senha_login(self) -> str:
        if self._login is None:
            self._login = getpass.getpass("Senha de login do console: ")
        return self._login

    def senha_enable(self) -> str:
        if self._enable is None:
            self._enable = getpass.getpass("Senha de enable (se configurada): ")
        return self._enable


def extrair_running_config(resposta: str) -> str:
    txt = normalizar(resposta)
    cabecalho = HEADER_RE.search(txt)
    if cabecalho is None:
        raise ValueError("Nao encontrei o cabecalho 'Current configuration : N bytes'")
    conteudo = txt[cabecalho.start():]
    fins = list(END_RE.finditer(conteudo))
    if not fins:
        raise ValueError("Saida truncada: linha final 'end' ausente")
    fim = fins[-1]
    depois = conteudo[fim.end():].strip()
    if not re.fullmatch(r"[A-Za-z0-9_.:/()-]+#", depois):
        raise ValueError(f"Saida truncada: prompt ausente apos 'end' ({depois[-90:]!r})")
    config = conteudo[:fim.end()].strip() + "\n"
    if len(config) < 80 or "\n" not in config:
        raise ValueError("Running-config incompleto/curto")
    return config


def main() -> int:
    p = argparse.ArgumentParser(description="Faz backup do show run dos roteadores Cisco no EVE-NG")
    p.add_argument("--host", default=EVE_HOST, help="Host EVE-NG")
    p.add_argument("--only", nargs="+", help="Coletar somente estes roteadores, ex.: --only PE1 PE2 PE3")
    p.add_argument("--attempts", type=int, default=3, help="Tentativas por roteador (padrao: 3)")
    p.add_argument("--timeout", type=float, default=150, help="Timeout total por comando (s)")
    p.add_argument("--idle", type=float, default=30, help="Tempo sem dados antes de erro (s)")
    p.add_argument("--out", help="Pasta de destino alternativa")
    a = p.parse_args()

    equipamentos = EQUIPAMENTOS
    if a.only:
        escolhidos = {x.upper() for x in a.only}
        desconhecidos = escolhidos - {x for x, _ in EQUIPAMENTOS}
        if desconhecidos:
            p.error(f"Roteadores desconhecidos: {', '.join(sorted(desconhecidos))}")
        equipamentos = [(x, y) for x, y in EQUIPAMENTOS if x in escolhidos]

    agora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    raiz = Path(__file__).resolve().parent
    pasta = Path(a.out) if a.out else raiz / "backups" / "01-Multicast" / agora
    pasta.mkdir(parents=True, exist_ok=True)
    print(f"Backup running-config | {len(equipamentos)} roteadores | {agora}")
    print("O script entra em enable se encontrar prompt '>' e desativa paginacao a cada conexao.")
    print("Feche outros consoles Telnet/SecureCRT desses roteadores antes de iniciar.\n")
    credenciais = Credenciais()
    ok, erros = 0, 0

    for nome, porta in equipamentos:
        print(f"Coletando {nome} ({a.host}:{porta})...", flush=True)
        motivos = []
        for tentativa in range(1, max(1, a.attempts) + 1):
            terminal = Console(a.host, porta, a.timeout, a.idle)
            try:
                with terminal:
                    terminal.preparar(credenciais)
                    resposta = terminal.executar("show running-config")
                    try:
                        config = extrair_running_config(resposta)
                    except ValueError:
                        # Preserva a saida real para diagnosticar sem guardar arquivo .cfg invalido.
                        (pasta / f"{nome}.debug.txt").write_text(resposta, encoding="utf-8")
                        raise
                destino = pasta / f"{nome}.cfg"
                destino.write_text(config, encoding="utf-8")
                print(f"[OK]   {nome:<5} -> {destino}")
                ok += 1
                break
            except (OSError, ConnectionError, TimeoutError, RuntimeError, ValueError) as exc:
                motivo = f"tentativa {tentativa}: {type(exc).__name__}: {exc}"
                motivos.append(motivo)
                if terminal.last_response:
                    # Guardar saida parcial mesmo se ocorreu timeout.
                    (pasta / f"{nome}.debug.txt").write_text(terminal.last_response, encoding="utf-8")
                if tentativa < max(1, a.attempts):
                    print(f"  [RETRY] {nome}: {motivo}", flush=True)
                    time.sleep(1.5)
        else:
            erros += 1
            print(f"[ERRO] {nome}: {motivos[-1]}")
            (pasta / f"{nome}.erro.txt").write_text("\n".join(motivos) + "\n", encoding="utf-8")

    print(f"\nFinalizado: {ok} OK, {erros} com erro")
    print(f"Diretorio: {pasta}")
    print("ATENCAO: arquivos .cfg e .debug.txt podem conter senhas e chaves. Mantenha-os privados.")
    if erros:
        print("Consulte *.erro.txt e *.debug.txt para diagnosticar as falhas.")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
