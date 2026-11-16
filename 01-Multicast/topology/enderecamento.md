# My Multicast Topology and Addressing

I built this seven-router EVE-NG tree and preserved the IOS IPv4 snapshots from **2026-11-12**. I added IPv6 in [LAB 05](../LAB05-IPv6-Multicast.md).

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

For BIDIR I used **RR-P Loopback1 10.255.0.2/32**. For Anycast RP I used **Loopback10 10.255.0.100/32** on RR-P and PE3.

## What I kept in mind

I used OSPF area 0 and PIM-SM on participating IPv4 interfaces. CE2 and CE3 joined on **Fa0/0**, not Loopback0. Later SSM/BIDIR/Anycast/IPv6 settings coexist in newer snapshots; I check the date and group before replaying an earlier test.

**This is a physical tree:** an OSPF metric change cannot create a second path around RR-P.

[IPv6 details](../LAB05-IPv6-Multicast.md) · [Config snapshots](../configs/README.md).
