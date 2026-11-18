# My Advanced BGP Labs

| Lab | What I tested | Result documented |
|---|---|---|
| [16 — Policy and best path](LAB16-BGP-POLICY-BESTPATH-IOSXR.md) | MED, communities, LOCAL_PREF and iBGP propagation | Community/LOCAL_PREF and RIB choices validated; MED test state preserved; earlier prepending evidence pending |
| [17 — Multipath / ECMP and failover](LAB17-BGP-MULTIPATH-ECMP-IOSXR.md) | Two paths, recovery and ADD-PATH distinction | Restored BGP/RIB multipath state captured; four running-configs collected; FIB and failure measurements pending |

[Original CLI](evidencias/LAB16-BGP-2026-11-17/CLI-OBSERVED.md) · [Shared XR configs](../03-Segment-Routing/configs/LABS12-16-2026-11-17/README.md)

**Next topics:** route reflection, negotiated Add-Path, measured PIC and RPKI. These are not validated by LABs 16–17. Two paths in BGP do not by themselves establish two forwarding paths.
