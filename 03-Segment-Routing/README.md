# Segment Routing

## Scope and status

SR-MPLS, segment identifiers, SR-TE, TI-LFA and SRv6.

**LAB 11 completed for SR-MPLS fundamentals:** Two IOS XRv classic 6.3.1 routers establish IS-IS L2 adjacency; advertise SRGB, Node/Prefix-SIDs and Adj-SIDs; install SR entries in the RIB and MPLS LFIB; and reach each other's loopback addresses with 5/5 ICMP replies in each direction. **Captured XR1/XR2 running configurations are published and verified against the collector ZIP.** Post-reboot persistence was not tested.

### Validated lab

- [LAB 11 — SR-MPLS Fundamentals with IS-IS (IOS XRv)](LAB11-SR-MPLS-ISIS-IOSXR.md) — LSDB/SRGB 16000–23999, Prefix-SIDs 16001/16002, local Adj-SID 24001 in both directions, MPLS forwarding Pop entries, traffic counters and ping. [XR1/XR2 configuration backups](configs/LAB11-SR-MPLS-2026-11-16/), explicit limitations and observed CLI are in the guide.

## Next study area

- Understand Adj-SID label scope and program a directed packet test, if supported.
- Expand to at least three SR-capable routers for an actual transit segment and path observability.
- Study SR-TE, explicit segment lists, TI-LFA and SRv6 only on platforms/topologies that support each feature.

## Evidence discipline

- Do not claim multi-hop SR forwarding, a deployed SR policy, TI-LFA or steering based only on two nodes' Prefix-SID entries.
- IP ping establishes IP connectivity; MPLS LFIB entries and counters provide separate evidence of label programming/activity.
- The previously shown illustrative configs are **not** running-config backups. Publish user-collected snapshots only after review for sensitive material.

Use the [lab template](../LAB-TEMPLATE.md) for future labs.
