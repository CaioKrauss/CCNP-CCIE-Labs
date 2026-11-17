# My Segment Routing Labs

## LAB 11 — SR-MPLS with two IOS XRv

I used **two classic IOS XRv 6.3.1** routers to test IS-IS SR-MPLS fundamentals.

- Both advertised **SRGB 16000–23999**.
- XR1 used **Node-SID 16001**; XR2 used **16002**.
- Both advertised a **local Adj-SID 24001**.
- I saw SR-labeled routes, LFIB `Pop` entries and **5/5** loopback pings in both directions.

[Read my LAB 11 notes](LAB11-SR-MPLS-ISIS-IOSXR.md) · [XR1/XR2 running configs](configs/LAB11-SR-MPLS-2026-11-16/) · [Detailed evidence](evidencias/LAB11-SR-MPLS-2026-11-16/DETAILED-ORIGINAL-REPORT.md)

**My takeaway:** Prefix-SID identifies a destination; Adj-SID identifies a local outgoing adjacency. I verified SID distribution and LFIB entries, **not** explicit multi-hop SR-TE forwarding.

## Night-session follow-up — LABs 12–14

| Lab | Result documented |
|---|---|
| [12 — SRMS / LDP interworking](LAB12-SR-MPLS-SRMS-LDP-INTERWORKING.md) | Mapping distribution, LFIB swaps and **20/20** pings each way |
| [13 — SR-TE](LAB13-SR-TE-IOSXR.md) | Partial evidence: committed explicit policy and color/VPN config; operational outputs unavailable |
| [14 — LFA / TI-LFA](LAB14-LFA-TI-LFA-ISIS-IOSXR.md) | Partial evidence: XR1 FRR config; repair/failure results unavailable |

[Shared final XR configs](configs/LABS12-16-2026-11-17/README.md) · [Evidence coverage and timezone correction](evidencias/LABS12-16-2026-11-17/COLLECTION-AND-COVERAGE.md)

The same session also includes [LAB 15 — BFD + IS-IS](../07-High-Availability/LAB15-BFD-ISIS-IOSXR.md) and [LAB 16 — BGP Advanced](../06-BGP-Advanced/LAB16-BGP-POLICY-BESTPATH-IOSXR.md). The original LAB 11 findings above retain their original scope.
