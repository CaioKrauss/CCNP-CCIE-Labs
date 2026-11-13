#!/usr/bin/env python3
"""Capture validated 'show running-config' output over EVE-NG Telnet consoles (Cisco IOS).

Standard library only; Python 3.10+.

Examples:
    python backup_show_run_eve.py
    python backup_show_run_eve.py --only PE1 PE2 PE3
    python backup_show_run_eve.py --attempts 4 --timeout 180

Keep the backup directory private: configurations and logs may contain passwords.
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

EVE_HOST = "192.0.2.10"  # Documentation placeholder; override with --host.
EQUIPAMENTOS = [
    ("CE1", 32769),
    ("PE1", 32770),
    ("CE2", 32771),
    ("PE3", 32772),
    ("CE3", 32773),
    ("RR-P", 32774),
    ("PE2", 32775),
]

# Detect the prompt at the end of the text, not on an earlier buffered line.
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
    """Only accept a prompt on the LAST line."""
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
        """Negotiate basic Telnet options without depending on telnetlib."""
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
                # Reject optional extensions and keep negotiation bytes out of IOS input.
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
        """Read until the prompt, or a login/password request when autenticar=True."""
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
                    raise ConnectionError("Telnet connection closed by the console")
            except socket.timeout:
                bloco = b""

            if bloco:
                parte = self._telnet(bloco)
                bruto.extend(parte)
                ultimo_dado = time.monotonic()
                if len(bruto) > 5_000_000:
                    raise RuntimeError("Output exceeds 5 MB; collection stopped")

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
                # After boot, some routers display a banner and wait for Enter.
                # Limit prompt nudges and use them only during the initial read.
                if (estimular and tentativas_enter < 3
                        and time.monotonic() - max(ultimo_enter, ultimo_dado) >= 2):
                    self.enviar()
                    ultimo_enter = time.monotonic()
                    tentativas_enter += 1
                if bruto and time.monotonic() - ultimo_dado > self.idle:
                    raise TimeoutError(f"No response for {self.idle:g}s; trailing output: {self.last_response[-180:]!r}")

        raise TimeoutError(f"Total timeout {self.timeout:g}s; trailing output: {self.last_response[-180:]!r}")

    def preparar(self, autenticacao: "Credenciais"):
        # Do not send Enter immediately if the console already printed a prompt:
        # an extra buffered prompt could confuse the enable step.
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
            raise RuntimeError("Could not reach the device prompt")

        prompt = ultimo_prompt(resposta)
        if prompt is None:
            raise RuntimeError("Cisco prompt not recognized")
        if prompt.endswith(">"):
            self.enviar("enable")
            resposta, tipo = self.ler(autenticar=True)
            if tipo == "password":
                self.enviar(autenticacao.senha_enable())
                resposta, tipo = self.ler(autenticar=True)
            prompt = ultimo_prompt(resposta)
            if tipo != "prompt" or prompt is None or not prompt.endswith("#"):
                raise RuntimeError("Could not enter privileged EXEC: check enable credentials")
        elif not prompt.endswith("#"):
            raise RuntimeError(f"Unexpected prompt: {prompt!r}")

        # Set pagination for each connection; it may reset after a reboot.
        self.executar("terminal length 0", exigir_sucesso=True)
        # 'terminal width' is optional; ignore it if unsupported by the IOS image.
        self.executar("terminal width 512", exigir_sucesso=False)

    def executar(self, comando: str, exigir_sucesso: bool = False) -> str:
        self.enviar(comando)
        resposta, tipo = self.ler()
        if tipo != "prompt":
            raise RuntimeError(f"No prompt returned after {comando}")
        if exigir_sucesso and ("% Invalid input" in resposta or "% Unrecognized" in resposta):
            raise RuntimeError(f"Unsupported command: {comando}")
        return resposta


class Credenciais:
    """Read environment variables or prompt with getpass without echoing passwords."""

    def __init__(self):
        self._login = os.environ.get("EVE_LOGIN_PASSWORD")
        self._enable = os.environ.get("EVE_ENABLE_PASSWORD")
        self._usuario = os.environ.get("EVE_LOGIN_USERNAME")

    def usuario(self) -> str:
        if self._usuario is None:
            self._usuario = input("Cisco console username: ").strip()
        return self._usuario

    def senha_login(self) -> str:
        if self._login is None:
            self._login = getpass.getpass("Console login password: ")
        return self._login

    def senha_enable(self) -> str:
        if self._enable is None:
            self._enable = getpass.getpass("Enable password (if configured): ")
        return self._enable


def extrair_running_config(resposta: str) -> str:
    txt = normalizar(resposta)
    cabecalho = HEADER_RE.search(txt)
    if cabecalho is None:
        raise ValueError("Missing 'Current configuration : N bytes' header")
    conteudo = txt[cabecalho.start():]
    fins = list(END_RE.finditer(conteudo))
    if not fins:
        raise ValueError("Truncated output: final 'end' line missing")
    fim = fins[-1]
    depois = conteudo[fim.end():].strip()
    if not re.fullmatch(r"[A-Za-z0-9_.:/()-]+#", depois):
        raise ValueError(f"Truncated output: prompt missing after 'end' ({depois[-90:]!r})")
    config = conteudo[:fim.end()].strip() + "\n"
    if len(config) < 80 or "\n" not in config:
        raise ValueError("Incomplete or unexpectedly short running-config")
    return config


def main() -> int:
    p = argparse.ArgumentParser(description="Back up show running-config from Cisco IOS routers in EVE-NG")
    p.add_argument("--host", default=EVE_HOST, help="EVE-NG host")
    p.add_argument("--only", nargs="+", help="Collect only these routers, e.g. --only PE1 PE2 PE3")
    p.add_argument("--attempts", type=int, default=3, help="Attempts per router (default: 3)")
    p.add_argument("--timeout", type=float, default=150, help="Total timeout per command (seconds)")
    p.add_argument("--idle", type=float, default=30, help="Idle time before failure (seconds)")
    p.add_argument("--out", help="Alternative output directory")
    a = p.parse_args()

    equipamentos = EQUIPAMENTOS
    if a.only:
        escolhidos = {x.upper() for x in a.only}
        desconhecidos = escolhidos - {x for x, _ in EQUIPAMENTOS}
        if desconhecidos:
            p.error(f"Unknown routers: {', '.join(sorted(desconhecidos))}")
        equipamentos = [(x, y) for x, y in EQUIPAMENTOS if x in escolhidos]

    agora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    raiz = Path(__file__).resolve().parent
    pasta = Path(a.out) if a.out else raiz / "backups" / "01-Multicast" / agora
    pasta.mkdir(parents=True, exist_ok=True)
    print(f"Running-config backup | {len(equipamentos)} routers | {agora}")
    print("The script enters enable from a '>' prompt and disables pagination per connection.")
    print("Close other Telnet/SecureCRT sessions to these routers before starting.\n")
    credenciais = Credenciais()
    ok, erros = 0, 0

    for nome, porta in equipamentos:
        print(f"Collecting {nome} ({a.host}:{porta})...", flush=True)
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
                        # Preserve actual diagnostic output without saving an invalid .cfg file.
                        (pasta / f"{nome}.debug.txt").write_text(resposta, encoding="utf-8")
                        raise
                destino = pasta / f"{nome}.cfg"
                destino.write_text(config, encoding="utf-8")
                print(f"[OK]   {nome:<5} -> {destino}")
                ok += 1
                break
            except (OSError, ConnectionError, TimeoutError, RuntimeError, ValueError) as exc:
                motivo = f"attempt {tentativa}: {type(exc).__name__}: {exc}"
                motivos.append(motivo)
                if terminal.last_response:
                    # Preserve partial output even after a timeout.
                    (pasta / f"{nome}.debug.txt").write_text(terminal.last_response, encoding="utf-8")
                if tentativa < max(1, a.attempts):
                    print(f"  [RETRY] {nome}: {motivo}", flush=True)
                    time.sleep(1.5)
        else:
            erros += 1
            print(f"[ERROR] {nome}: {motivos[-1]}")
            (pasta / f"{nome}.erro.txt").write_text("\n".join(motivos) + "\n", encoding="utf-8")

    print(f"\nFinished: {ok} OK, {erros} failed")
    print(f"Directory: {pasta}")
    print("NOTICE: .cfg and .debug.txt files may contain passwords and keys. Keep them private.")
    if erros:
        print("Inspect *.erro.txt and *.debug.txt to diagnose failures.")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
