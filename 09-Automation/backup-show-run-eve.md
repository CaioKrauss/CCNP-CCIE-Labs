# EVE-NG Telnet Console Backup Utility — Cisco IOS

[backup_show_run_eve.py](backup_show_run_eve.py) captures show running-config from the seven IOS multicast routers. It does not publish backups or modify persistent router configuration.

## What it does and why

| Step | Behavior | Reason |
|---|---|---|
| Connect | Uses the configured host and per-device console port | Each EVE console is a separate endpoint |
| Authenticate | Reads environment variables or prompts locally | Avoids embedding passwords in the script |
| Enter EXEC | Sends enable if the prompt ends in > | show running-config typically needs privilege |
| Prepare terminal | terminal length 0; optional terminal width 512 | Prevents pagination/wrapping from truncating output |
| Collect | Sends show running-config | Reads active configuration |
| Validate | Requires Current configuration, end and final prompt | Rejects obviously incomplete captures |
| Save | Writes .cfg or diagnostic/error files | Keeps failures visible instead of treating partial output as a valid backup |

## Usage

Run from the utility directory with Python 3.10+; it uses the standard library.

```powershell
python .\backup_show_run_eve.py --help
python .\backup_show_run_eve.py --host 192.0.2.10
python .\backup_show_run_eve.py --host 192.0.2.10 --only PE1 PE2 PE3
python .\backup_show_run_eve.py --host 192.0.2.10 --attempts 4 --timeout 180 --out .\private-backups
```

192.0.2.10 is a documentation placeholder, not a reachable server. Set the actual lab host and verify every entry in EQUIPAMENTOS before connecting. The bundled port/name mapping belongs to the multicast scenario; EVE ports may identify completely different routers after changing labs.

Optional environment variables: EVE_LOGIN_USERNAME, EVE_LOGIN_PASSWORD and EVE_ENABLE_PASSWORD. Do not commit their values. Default output is backups/01-Multicast/<timestamp>/<device>.cfg relative to the script directory.

## Boundaries and troubleshooting

- This utility's parser expects Cisco IOS output. It was not the IOS XR collection adapter used for the L3VPN validation.
- A valid-looking capture is not proof of correct forwarding or startup-config persistence.
- Close competing console sessions before collecting. If command echo/output appears shifted, stop and verify command-response alignment.
- A timeout can be console interaction, login or connectivity; it is not proof of configuration loss.
- Preserve diagnostic files locally and review them for secrets before sharing.
- No VM start/stop/reboot or configuration restoration is performed.

The English revision changes explanatory text, prompts and messages. Existing callable names, CLI options, environment variables and legacy .erro.txt filenames remain compatible.
