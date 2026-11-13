# Multicast Command Reference — Cisco IOS

Run these checks in order: unicast reachability → PIM/RP → membership → multicast state → traffic counters. A configuration check is not a delivery test.

| Question | Command | Interpretation |
|---|---|---|
| Is the IPv4 IGP established? | show ip ospf neighbor | Expected neighbors should reach the appropriate full adjacency state |
| Is the source reachable? | show ip route 10.255.0.11 | Inspect the source prefix and next hop |
| Which interface is expected for source traffic? | show ip rpf 10.255.0.11 | Compare RPF interface/neighbor with actual incoming traffic |
| Does PIM have neighbors? | show ip pim neighbor | Missing transit adjacency can prevent joins |
| Which RP serves the group? | show ip pim rp mapping | Match the group range to the intended RP |
| Which router is the BIDIR DF? | show ip pim interface df | Verify the elected forwarder on each participating link |
| Is there local membership? | show ip igmp groups | Inspect group, interface and source information |
| Which tree is installed? | show ip mroute 239.1.1.1 | Read (*,G)/(S,G), flags, IIF and OIL together |
| Is the SSM channel correct? | show ip mroute 232.1.1.1 | Source must match the receiver's requested source |
| Is BIDIR state installed? | show ip mroute 239.2.2.2 | Look for shared-tree/BIDIR state |
| Does Anycast traffic have state? | show ip mroute 239.3.3.3 | Compare before/after the controlled test |
| Is data advancing? | show ip mroute count | Compare counters over an interval and inspect RPF failures |
| Is the remote Anycast RP reachable? | show ip rpf 10.255.0.100 | RPF resolution should follow the selected RP route |
| Is MSDP established? | show ip msdp peer | Inspect state and reset count |
| Has source information arrived? | show ip msdp sa-cache | SA presence is source discovery, not proof of receiver delivery |

For IPv6, use the command matrix in [LAB 05](LAB05-IPv6-Multicast.md). The group addresses and sources above belong to this lab; substitute the correct values in another environment.

Local reception can legitimately show a null OIL. An (S,G) entry alone does not prove SPT switchover or traffic delivery. Preserve exact outputs and put interpretation outside the capture.
