# My IPv6 Studies

I started IPv6 with [LAB 05 — IPv6 Multicast](../01-Multicast/LAB05-IPv6-Multicast.md).

## What I tested

- **OSPFv3:** IPv6 loopback reachability in the seven-router topology.
- **ASM:** PIM-SM and static RP `2001:DB8:100::1`.
- **SSM:** MLDv2 source-specific joins and permitted/unselected-source tests.
- **Forwarding:** both receiver sites replied to the selected source's multicast probes.

The [post-test running configs](../01-Multicast/configs/snapshot-2026-11-13/) are published. They do **not** prove startup persistence.

## What I still need to test

MLDv1, Neighbor Discovery, ICMPv6 troubleshooting, PMTUD, MP-BGP and IPv6 security are **not covered** by the completed multicast test.
