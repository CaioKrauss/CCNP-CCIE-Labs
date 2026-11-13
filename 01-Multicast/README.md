# IPv4 and IPv6 Multicast — Labs 01–05

Seven Cisco IOS routers in EVE-NG, using OSPFv2 for IPv4 and OSPFv3 for IPv6. Labs 01–04 preserve user-supplied console evidence from 2026-11-12; LAB 05 preserves console excerpts from 2026-11-13. This documentation revision did not rerun those tests.

![Multicast topology supplied by the lab owner](topology/multicast-eve-ng.png)

The physical topology is a tree: CE1–PE1–RR-P, with branches through PE2 to CE2 and through PE3 to CE3. There is no PE2–PE3 link. Changing an OSPF cost cannot create an alternate physical path. RR-P is a device name, not evidence of BGP route reflection.

## Choose the forwarding model

| Lab | Receiver request | Group / RP | What was observed |
|---|---|---|---|
| [01 — PIM-SM ASM](LAB01-PIM-SM-ASM.md) | Group G | 239.1.1.1 / 10.255.0.1 | IGMP, (*,G), (S,G), T flag and RPF |
| [02 — SSM / IGMPv3](LAB02-PIM-SSM-IGMPv3.md) | Source S and group G | 232.1.1.1 / no RP | Distinct source trees; PE2 counters 26→28 |
| [03 — BIDIR](LAB03-PIM-BIDIR.md) | Group G | 239.2.2.2 / 10.255.0.2 | DF election; shared-tree counters 14→17 |
| [04 — Anycast RP / MSDP](LAB04-Anycast-RP-MSDP.md) | Group G | 239.3.3.3 / 10.255.0.100 | MSDP, SA cache, route failover; PE2 24→26 |
| [05 — IPv6 ASM / SSM](LAB05-IPv6-Multicast.md) | Group or source/group | FF1E::1234 and FF3E::1234 | MLDv2, two receivers and source filtering |

## Reading order

1. [Topology and addressing](topology/enderecamento.md).
2. One lab guide: objective → configuration → commands → result → explanation.
3. [Command reference](comandos.md) and [troubleshooting](troubleshooting.md).
4. [Evidence files](evidencias/) and the relevant configuration snapshot.

## Snapshot selection

- [2026-11-12](configs/snapshot-2026-11-12/): combined final IPv4 state after Labs 01–04.
- [2026-11-13](configs/snapshot-2026-11-13/): post-LAB05 state, including IPv6.
- [Configuration notes](configs/README.md): provenance and differences between snapshots.
- [IOS backup utility](../09-Automation/backup-show-run-eve.md): local collection, not automatic publication.

The later snapshot is not an exact replay of each earlier lab. For example, CE2 and CE3 request different IPv4 SSM sources for the same group. Match the source address in each test to that receiver's subscription.

## What the evidence does and does not establish

- SSM, BIDIR and Anycast captures show increasing forwarding counters.
- ASM captures show routing state and the IOS T flag, but not comparable end-receiver delivery counters.
- BIDIR traffic from CE1 and CE3 was reported by the user; no individual counter run was labeled for each source.
- Anycast failure testing covered an already-known source and a renewed join, not registration of a previously unseen source after failure.
- IPv6 ASM/SSM and MLDv2 were exercised. MLDv1 was not.
- The post-LAB05 snapshots show the temporary IPv6 source removed. They do not prove startup-config persistence.

## Shared baseline

OSPF process 1/area 0 provides IPv4 reachability. ASM_GROUPS maps to RP 10.255.0.1; BIDIR_GROUPS maps to RP 10.255.0.2; ANYCAST_GROUPS maps to 10.255.0.100. SSM uses the default IPv4 232.0.0.0/8 range. RR-P and PE3 exchange MSDP information through their unique loopbacks.

The snapshot review found no published passwords, tokens or private keys. Review each new capture independently before publication.
