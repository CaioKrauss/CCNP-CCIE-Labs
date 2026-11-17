# My High Availability Labs

| Lab | Result documented |
|---|---|
| [14 — LFA / TI-LFA](../03-Segment-Routing/LAB14-LFA-TI-LFA-ISIS-IOSXR.md) | Partial evidence: XR1 repair configuration preserved; operational repair and timing unavailable |
| [15 — BFD + IS-IS](LAB15-BFD-ISIS-IOSXR.md) | Evidence pending: original BFD outputs unavailable; historical shared backup has no BFD directives |

[Shared collection and evidence gaps](../03-Segment-Routing/evidencias/LABS12-16-2026-11-17/COLLECTION-AND-COVERAGE.md)

**My rule:** a protocol timer is not a measured outage or hitless failover. I keep configuration, installed repair and observed traffic recovery separate.

**Future topics:** VRRP, LACP and MSTP, with before/failure/after traffic and protocol state.
