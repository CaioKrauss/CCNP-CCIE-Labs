# My Segment Routing Labs

## LAB 11 — SR-MPLS with two IOS XRv

I used **two classic IOS XRv 6.3.1** routers to test IS-IS SR-MPLS fundamentals.

- Both advertised **SRGB 16000–23999**.
- XR1 used **Node-SID 16001**; XR2 used **16002**.
- Both advertised a **local Adj-SID 24001**.
- I saw SR-labeled routes, LFIB `Pop` entries and **5/5** loopback pings in both directions.

[Read my LAB 11 notes](LAB11-SR-MPLS-ISIS-IOSXR.md) · [XR1/XR2 running configs](configs/LAB11-SR-MPLS-2026-11-16/) · [Detailed evidence](evidencias/LAB11-SR-MPLS-2026-11-16/DETAILED-ORIGINAL-REPORT.md)

**My takeaway:** Prefix-SID identifies a destination; Adj-SID identifies a local outgoing adjacency. I verified SID distribution and LFIB entries, **not** explicit multi-hop SR-TE forwarding.

**Next:** expand to more SR-capable routers for segment stacks, SR-TE and TI-LFA. Those features are **not tested yet**.
