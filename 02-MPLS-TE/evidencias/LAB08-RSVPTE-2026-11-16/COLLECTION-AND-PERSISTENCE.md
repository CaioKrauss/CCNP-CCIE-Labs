# LAB 08 — Collection and persistence manifest

**Collection source:** `20261116-012150.rar`, supplied by the lab owner. Device console snapshots taken on 16 November 2026 at approximately 01:21:50–01:21:52 (-03:00).

| Host | Running captured | Startup captured | Running = startup | Configuration register reported |
|---|---|---|---|---|
| R1 | yes, complete | yes | yes | `Configuration register is 0x2142 (will be 0x2102 at next reload)` |
| R2 | yes, complete | yes | yes | `Configuration register is 0x2142 (will be 0x2102 at next reload)` |
| R3 | yes, complete | yes | yes | `Configuration register is 0x2142 (will be 0x2102 at next reload)` |
| R4 | yes, complete | yes | yes | `Configuration register is 0x2142 (will be 0x2102 at next reload)` |

- Device state was **read** from the archive; the publication itself does not reconfigure or reboot routers. The collector metadata says `already_saved: true`, and the submitted snapshots independently match on each router. No fresh post-reboot check was performed.
- `Configuration register is 0x2142 (will be 0x2102 at next reload)` is the exact reported status. The pending `0x2102` takes effect on next reboot; startup loading after that reboot has **not** been validated.
- These are isolated lab-only configurations. Credentials, keys and production/customer addressing are absent from the configuration excerpts reviewed.
- The four running-config files are exact command snapshots after normalization of CRLF line endings and trailing newline; corresponding startup copies and command transcripts are provided. Device hardware identifiers and console-port numbers from auxiliary metadata are deliberately not published.
- `CLI-observed-during-lab.md` separately records console outputs pasted in conversation; they were not gathered by the same RAR capture session.
