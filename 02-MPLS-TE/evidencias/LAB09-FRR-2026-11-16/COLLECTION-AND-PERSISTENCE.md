# LAB 09 — Collection and persistence manifest (2026-11-16)

## Origin and collection

- Original input: user-supplied `routers.zip`, containing the R1–R4 console collection files.
- Each R1–R4 host uses Cisco 7200 `C7200-ADVENTERPRISEK9-M`, IOS **15.2(4)S7** according to the captured `show version` text.
- Complete running-configuration and startup-configuration snapshots were present for all four routers.
- `result.json` from the supplied ZIP reports `running_complete: true`, `already_saved: true`, and `startup_matches_running: true` for each router. The snapshots were independently compared byte-for-byte before publication.
- These snapshots preserve the **final running/startup configuration**, not intermediate interface shutdowns or the transient FRR state.
- Console output for **Ready → Active → Ready** was supplied separately by the lab owner in the conversation, and is recorded as selected observed excerpts in `FRR-CLI-OBSERVED.md`; it is **not** part of the ZIP's baseline collector command transcripts.

## Collected at (America/Sao_Paulo, per the archive)

| Router | Collection timestamp | Running = startup | Platform |
|---|---|---|---|
| R1 | 2026-11-16T01:55:08.723751-03:00 | Yes | Cisco 7200 IOS 15.2(4)S7 |
| R2 | 2026-11-16T01:55:08.724003-03:00 | Yes | Cisco 7200 IOS 15.2(4)S7 |
| R3 | 2026-11-16T01:55:10.909818-03:00 | Yes | Cisco 7200 IOS 15.2(4)S7 |
| R4 | 2026-11-16T01:55:11.100418-03:00 | Yes | Cisco 7200 IOS 15.2(4)S7 |

## Important boot caveat

On **all four devices**, `show version` states:

```text
Configuration register is 0x2142 (will be 0x2102 at next reload)
```

This **does not prove the correction has taken effect**. The register switch to `0x2102` is pending the next reload; no post-reload validation was supplied. A startup-config matching running-config is proof of saved config at the collection time, not proof of successful boot-time loading afterward.

## File provenance

- `configs/LAB09-FRR-2026-11-16/`: reviewed `show running-config` and `show startup-config` snapshots from the supplied archive, only line endings normalized to LF.
- `evidencias/LAB09-FRR-2026-11-16/R*-running-console.txt`, `R*-startup-before-console.txt`, `R*-show-version.txt`: the original associated text transcripts from the ZIP, only line endings normalized to LF.
- `evidencias/LAB09-FRR-2026-11-16/FRR-CLI-OBSERVED.md`: faithfully selected excerpts of separately user-pasted live CLI output; not a new execution by the publisher.

## Security review

Configurations were reviewed for secrets/credentials and environment-specific data before publishing; no passwords, authentication tokens, SNMP communities or keys were found in the released files. The ZIP's machine-local Telnet ports and `result.json` are not published; their needed provenance is summarized above. The addresses shown here are inside a lab, not public routing recommendations.
