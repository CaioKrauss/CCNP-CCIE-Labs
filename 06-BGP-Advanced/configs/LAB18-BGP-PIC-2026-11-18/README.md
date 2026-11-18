# LAB 18 — Collected and saved configurations

Live collection: **2026-11-18, 16:13–16:14 São Paulo / 19:13–19:14 UTC**. These files came from the four consoles, not from reconstructed commands or previous lab backups.

| Router | Running configuration | Persistence |
|---|---|---|
| XR1 | [XR1-running.cfg](XR1-running.cfg) | commit executed; no pending changes |
| XR2 | [XR2-running.cfg](XR2-running.cfg) | commit executed; no pending changes |
| R1 | [R1-running.cfg](R1-running.cfg) | write memory OK; [startup](R1-startup.cfg) equals running |
| R2 | [R2-running.cfg](R2-running.cfg) | write memory OK; [startup](R2-startup.cfg) equals running |

XR commit returned “No configuration changes to commit.” Existing committed running state was preserved; no new commit ID was generated. Configuration persistence was checked without rebooting.

Files contain the complete displayed configuration from the version header through end. CLI echo, timestamps preceding the configuration and prompts remain in the [live transcripts](../../evidencias/LAB18-BGP-PIC-2026-11-18/). Text is normalized as UTF-8/LF. Credentials were not included; no configuration lines required redaction.

[Manifest](manifest.json) records collection times and running-config hashes. [SHA256SUMS](SHA256SUMS.txt) covers all six configuration files. Earlier LAB 17 snapshots are unchanged.

[Full lab guide](../../LAB18-BGP-PIC-EDGE-CORE-IOSXR.md).
