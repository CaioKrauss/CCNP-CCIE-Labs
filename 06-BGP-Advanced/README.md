# My Advanced BGP Labs

| Lab | What I tested | Result documented |
|---|---|---|
| [16 — Policy and best path](LAB16-BGP-POLICY-BESTPATH-IOSXR.md) | MED, communities, LOCAL_PREF and iBGP propagation | Community/LOCAL_PREF and RIB choices validated; MED test state preserved; earlier prepending evidence pending |
| [17 — Multipath / ECMP and failover](LAB17-BGP-MULTIPATH-ECMP-IOSXR.md) | Two paths, recovery and ADD-PATH distinction | Restored BGP/RIB multipath state captured; four running-configs collected; FIB and failure measurements pending |
| [18 — BGP PIC Edge / Core](LAB18-BGP-PIC-EDGE-CORE-IOSXR.md) | Installed BGP backup and Local-LFA transport protection | Historical Core CEF failover; live restored state and four saved configs; timing unmeasured |
| [19 — ADD-PATH + Route Reflection](LAB19-BGP-ADD-PATH-RR-IOSXR.md) | Negotiated Send/Receive and alternate path visibility | Historical failover/recovery; current Path ID 3, single CEF exit and four saved configs |

[Original CLI](evidencias/LAB16-BGP-2026-11-17/CLI-OBSERVED.md) · [Shared XR configs](../03-Segment-Routing/configs/LABS12-16-2026-11-17/README.md)

**Next topics:** multi-client/cluster route reflection, measured PIC and RPKI. LAB 19 validates negotiated ADD-PATH in the current two-XR setup. Two paths in BGP do not by themselves establish two forwarding paths.
