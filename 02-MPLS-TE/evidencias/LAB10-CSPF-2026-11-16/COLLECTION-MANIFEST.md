# LAB 10 — Collection and persistence manifest

**Source:** EVE-NG lab owner collector ZIP `20261116-024805.zip`, topology file name `CSPF.unl`, captured locally on **2026-11-16 02:48 (UTC−03:00)**. These snapshots are distinct from the interactive CLI outputs observed earlier during the exercise.

| Device | Running snapshot | Startup snapshot | Exact match | Collection outcome |
|---|---|---|---|---|
| R1 | Complete | Complete | Yes, byte-identical | Collector saved configuration during collection |
| R2 | Complete | Complete | Yes, byte-identical | Already saved before collection |
| R3 | Complete | Complete | Yes, byte-identical | Collector saved configuration during collection |
| R4 | Complete | Complete | Yes, byte-identical | Collector saved configuration during collection |

## Observed saved state

- **R1**: `Tunnel100`, RSVP bandwidth **8000 kbps**, priority **7/7**, affinity **0x1/0x1**, CSPF dynamic, Autoroute on; interface to R3 has `attribute-flags 0x1`.
- **R2**: IS-IS level 2, LDP and RSVP-TE transport; no configured lab TE tunnel.
- **R3**: `Tunnel200` to R4, RSVP bandwidth **5000 kbps**, priority **0/0**, affinity **0x1/0x1**, CSPF dynamic; interface **administratively shut down** in this final snapshot. This permits Tunnel100 to recover and reserve its bandwidth. Both R3 transport links have `attribute-flags 0x1`.
- **R4**: IS-IS, LDP and RSVP-TE with R4–R3 directional attribute `0x1`.

Every router reports `Configuration register is 0x2142 (will be 0x2102 at next reload)`. Persistence to startup is verified; **the next-reload config-register change was not verified with a reboot**.

## Publication hygiene

The full running and startup **configurations** are published exactly as collected (normalized line endings only). Selected CLI collection transcripts and a reviewed `show version` excerpt are published. Machine-local Telnet console ports, the collector internal lab UUID, and machine-specific JSON/terminal connection records are deliberately excluded. There are no credentials in the reviewed configuration files.

The CSPF path changes, RSVP preemption events, and recovery states are **owner-supplied interactive CLI evidence from the chat**; the final ZIP contains configuration snapshots and collector logs, not a replay of all intermediate tests. The separate [observed CLI sequence](CLI-OBSERVATIONS.md) documents that distinction.

## SHA-256 of original running/startup pairs

- `R1`: `d24e8a0bd7752f06fd20fad873a4b6be187ce3e04b61719033d64be8b2e6f1d2` (both running and startup)
- `R2`: `23e087f8b72f9efb4d5afea2624a5850a016ed32433d59dde403c8381c8907c3` (both running and startup)
- `R3`: `961c22a70c445dace13e398b782e424af0dc845c5beb9498f1f9823602fa564c` (both running and startup)
- `R4`: `f5dfaf9d804f5c7c724ad239382d9a68c92fffca05132d8146c6aa9c6fb9667b` (both running and startup)
