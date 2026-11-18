# LAB 17 — Collected running configurations

Collected directly from **XR1, XR2, R1 and R2** on **2026-11-17, 02:48–02:49 São Paulo (05:48–05:49 UTC)**. This is the current collected LAB 17 state; it is not a reconstruction from the earlier ZIP.

| Device | Running configuration | Captured state |
|---|---|---|
| XR1 | [XR1-running.cfg](XR1-running.cfg) | IOS XR 6.3.1; last configuration change 05:33:29 UTC |
| XR2 | [XR2-running.cfg](XR2-running.cfg) | IOS XR 6.3.1; last configuration change 05:26:55 UTC |
| R1 | [R1-running.cfg](R1-running.cfg) | IOS config version 15.2; AS 65101; 10.0.13.1 |
| R2 | [R2-running.cfg](R2-running.cfg) | IOS config version 15.2; AS 65102; 10.0.24.2 |

XR1 contains `bgp bestpath as-path multipath-relax` and `maximum-paths eibgp 2`. XR2 applies `EBGP-R2-ECMP-IN` inbound from R2, setting LOCAL_PREF 200 for 198.51.100.0/24. R1 sends communities and attaches LAB16-COMM outbound. Its retained MED/prepend route-maps are not currently attached.

## Provenance and integrity

- The original console transcripts, detailed manifest and collection attempts remain in the local ZIP; only the four reviewed running-configs and their byte hashes are published here.
- [SHA-256](SHA256SUMS.txt) records the exact published CFG bytes.
- Local export: `20261117-024813.zip`; SHA-256 `59ff3ff84558f7fb0f04c69c90534b27ca25ca5e51323e8ba7d1692b055d517b`.
- No configuration commit, write memory, reboot or failure injection was performed. Startup persistence and forwarding were not retested. Login credentials are not included. The detailed collection metadata was excluded from public publication.

The [older 02:23 export](../../../03-Segment-Routing/configs/LABS12-16-2026-11-17/README.md) stays unchanged as historical evidence. This new snapshot closes the current-config gap but cannot recreate removed LAB 13–16 intermediate states. The owner confirms that LAB 13–15 operational evidence is in the source chat; recovering those older messages remains pending.
