# Coletor show running-config via console Telnet EVE-NG

O arquivo [backup_show_run_eve.py](backup_show_run_eve.py) é um utilitário de laboratório para capturar `show running-config` de CE1, PE1, CE2, PE3, CE3, RR-P e PE2.

- Tenta entrar no modo privilegiado com `enable` quando o prompt está em `>`.
- Desabilita paginação com `terminal length 0`, coleta e valida o cabeçalho e fim da configuração.
- Faz novas tentativas e registra saídas de erro/diagnóstico quando necessário.
- Salva os backups sob `backups/01-Multicast/<data-hora>/<roteador>.cfg` no computador do usuário.

```powershell
.\.venv\Scripts\python.exe .\backup_show_run_eve.py
.\.venv\Scripts\python.exe .\backup_show_run_eve.py --only PE1 PE2 PE3
```

Configurar host/portas do EVE-NG para cada ambiente; os valores do script são de uma rede de laboratório privada. O programa **não deve** ser usado para coletar ou publicar informações sensíveis de roteadores de produção.

`backups/`, `.env` e credenciais não pertencem ao repositório público.
