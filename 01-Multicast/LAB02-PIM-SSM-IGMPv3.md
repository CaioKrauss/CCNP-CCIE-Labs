# LAB 02 — Source-Specific Multicast and IGMPv3

## Objective and setup

Deliver **232.1.1.1** only from the source requested by each receiver. CE2 requests **10.255.0.11**; CE3 requests **10.0.1.1**. Both addresses belong to CE1, but they identify different SSM channels.

![SSM lab topology](topology/multicast-eve-ng.png)

## Mechanism

An SSM receiver selects (S,G), not just G. IGMPv3 source selection allows the last-hop router to join directly toward S. No RP discovery, PIM Register or transition from an RP shared tree is required for this SSM group. See [RFC 4607](https://www.rfc-editor.org/rfc/rfc4607.html).

This explains why changing the packet's source address changes which receiver subscription it matches, even if the multicast destination stays the same.

## Configuration and purpose

```cisco
! All participating routers:
ip pim ssm default
! CE2, receiver-facing interface:
interface FastEthernet0/0
 ip igmp version 3
 ip igmp join-group 232.1.1.1 source 10.255.0.11
! CE3, receiver-facing interface:
interface FastEthernet0/0
 ip igmp version 3
 ip igmp join-group 232.1.1.1 source 10.0.1.1
```

The default SSM range is 232.0.0.0/8. IGMPv3 enables source-aware membership. The source in the join must match the source of the generated traffic. Keep the existing unicast routing and PIM-enabled transit interfaces.

## Evidence and interpretation

| Observation | Meaning |
|---|---|
| PE2 (10.255.0.11,232.1.1.1), sTI, IIF Fa0/0, OIL Fa1/0 | Source-specific state connects the upstream core to CE2 |
| PE2 RPF neighbor 10.0.23.1, learned through OSPF | The expected source direction is toward RR-P |
| CE2 sPLTXI with null OIL | CE2 is the local receiver; null OIL alone does not mean failure |
| PE3 (10.0.1.1,232.1.1.1), sTI, RPF 10.0.34.1, OIL Fa1/0 | CE3's different source selection produces a different channel |
| PE2 packet counters 26→28; RPF failed 0 | Captured packets traversed the forwarding path without an observed RPF failure |

```cisco
show ip igmp groups
show ip mroute 232.1.1.1
show ip rpf 10.255.0.11
show ip mroute count
```

Read the source on every (S,G) line before comparing counters. A T flag in SSM does not imply an earlier RP-tree switchover; the channel is source-specific from the start.

## Troubleshooting and limits

If the wrong source is selected, a healthy unicast path does not make the SSM subscription match. First compare the sender's actual source address with the receiver's requested source. Then verify RPF, PIM adjacency and OIL.

The evidence establishes distinct source state and PE2 counter growth. A separate source-B counter sequence was not supplied; do not assign it an invented delivery count.

[Command evidence](evidencias/LAB02_PIM_SSM_IGMPv3.txt) · [Addressing](topology/enderecamento.md)
