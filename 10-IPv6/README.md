# IPv6

## Documented result

[LAB 05 — IPv6 multicast](../01-Multicast/LAB05-IPv6-Multicast.md) covers OSPFv3 reachability, PIM-SM ASM, a static RP, MLDv2, SSM and source selection on seven Cisco IOS routers.

The recorded tests include receiver replies, multicast state and positive/negative source cases. MLDv1 was not tested. The [post-LAB05 snapshot](../01-Multicast/configs/snapshot-2026-11-13/) preserves the reviewed running configurations; it does not establish startup persistence.

## Questions answered in LAB 05

- How does OSPFv3 provide the reachability used by the multicast topology?
- Which RP serves the ASM group, and what Register evidence was captured?
- How does source selection change reception for the SSM group?
- Why can a local receiver show a null outgoing-interface list?

See the lab's command matrix for the observed IOS syntax and result interpretation.

## Future scope

Neighbor Discovery, ICMPv6, MP-BGP, path-MTU discovery and IPv6 security remain separate planned studies. The multicast result does not validate all IPv6 features.

- [x] First IPv6 lab documented
- [x] Evidence limits and snapshot provenance recorded
- [ ] MLDv1-specific experiment
- [ ] Dedicated PMTUD/security experiments
