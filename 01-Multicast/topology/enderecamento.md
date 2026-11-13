# Multicast Topology and Addressing

Source: seven Cisco IOS configuration snapshots collected on 2026-11-12, with the IPv6 extension documented in LAB 05. The screenshot was supplied by the lab owner on 2026-11-13.

![EVE-NG multicast topology](multicast-eve-ng.png)

## IPv4 transit links

| Endpoint | Interface / address | Endpoint | Interface / address | Subnet |
|---|---|---|---|---|
| CE1 | Fa0/0 — 10.0.1.1/30 | PE1 | Fa1/0 — 10.0.1.2/30 | 10.0.1.0/30 |
| PE1 | Fa0/0 — 10.0.12.1/30 | RR-P | Et1/2 — 10.0.12.2/30 | 10.0.12.0/30 |
| RR-P | Et1/1 — 10.0.23.1/30 | PE2 | Fa0/0 — 10.0.23.2/30 | 10.0.23.0/30 |
| PE2 | Fa1/0 — 10.0.2.1/30 | CE2 | Fa0/0 — 10.0.2.2/30 | 10.0.2.0/30 |
| RR-P | Et1/0 — 10.0.34.1/30 | PE3 | Fa0/0 — 10.0.34.2/30 | 10.0.34.0/30 |
| PE3 | Fa1/0 — 10.0.3.1/30 | CE3 | Fa0/0 — 10.0.3.2/30 | 10.0.3.0/30 |

## Loopbacks and roles

| Node | Loopback0 / OSPF router ID | Role |
|---|---|---|
| CE1 | 10.255.0.11/32 | Source-side router |
| PE1 | 10.255.0.12/32 | Transit |
| RR-P | 10.255.0.1/32 | Central transit and static ASM RP |
| PE2 | 10.255.0.23/32 | Transit toward CE2 |
| CE2 | 10.255.0.22/32 | Local test receiver |
| PE3 | 10.255.0.33/32 | Transit; second Anycast RP in LAB 04 |
| CE3 | 10.255.0.32/32 | Local receiver; also a source in BIDIR tests |

RR-P uses Loopback1 10.255.0.2/32 for BIDIR. RR-P and PE3 share Loopback10 10.255.0.100/32 in the Anycast lab.

## Baseline and evolution

The initial ASM baseline uses Cisco IOS 15.2, ip multicast-routing, OSPF process 1/area 0 and PIM sparse mode on the transit interfaces. CE1 and RR-P also enable PIM on Loopback0. Initial CE2/CE3 membership is 239.1.1.1 on Fa0/0; their Loopback0 interfaces do not need to be mistaken for the receiver-facing interfaces.

Later snapshots contain SSM, BIDIR, Anycast and IPv6 additions. Group-scoped RP mappings supersede the simplest initial unscoped RP example. Consult the matching lab and date before reproducing a state.

The physical tree has no redundant links. RPF paths can be inspected, but changing a metric alone cannot create ECMP or a bypass around RR-P. Unused RR-P interfaces are administratively down.

[IPv6 address plan](../LAB05-IPv6-Multicast.md#addressing-and-prerequisites) · [Snapshot provenance](../configs/README.md)
