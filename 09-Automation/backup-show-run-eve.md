# My Cisco IOS Backup Script for EVE-NG

I use [`backup_show_run_eve.py`](backup_show_run_eve.py) to collect **`show running-config`** from my seven-router IOS multicast lab over Telnet consoles.

## What it does

1. Connects to the host/console port mapped to each router.
2. Logs in using **locally provided credentials**, then enters privileged EXEC when needed.
3. Sends `terminal length 0` (and optionally `terminal width 512`) so output is not paginated.
4. Captures `show running-config` and checks for a recognizable start, `end` and final prompt.
5. Saves complete `.cfg` files or separate diagnostic/error files if the capture fails.

## How I run it (Python 3.10+)

```powershell
python .\backup_show_run_eve.py --help
python .\backup_show_run_eve.py --host 192.0.2.10
python .\backup_show_run_eve.py --host 192.0.2.10 --only PE1 PE2 PE3
```

**`192.0.2.10` is only an example.** I supply my actual EVE-NG IP, check the `EQUIPAMENTOS` console ports and never commit credentials.

For optional authentication I use `EVE_LOGIN_USERNAME`, `EVE_LOGIN_PASSWORD` and `EVE_ENABLE_PASSWORD` environment variables or local prompts. The default output is under `backups/01-Multicast/<timestamp>/`, excluded by `.gitignore`.

**Limit:** this script expects **Cisco IOS** console output, not IOS XR. A captured running-config does not prove startup persistence or packet forwarding. I review files for secrets before sharing them. The script does not reboot routers or apply configuration.
