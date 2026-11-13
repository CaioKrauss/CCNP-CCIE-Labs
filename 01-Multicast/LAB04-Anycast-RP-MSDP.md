# LAB 04 — Anycast RP, MSDP and a Controlled RP Failure

## Objective and scope

Use **10.255.0.100/32** as the Anycast RP address on **RR-P and PE3** for group **239.3.3.3**. Observe what happens when RR-P's Anycast loopback is shut down. Source: **10.255.0.11**.

This is a historical controlled lab test. The English documentation revision did not repeat the shutdown.

![Anycast RP lab topology](topology/multicast-eve-ng.png)

## Mechanism

Both RPs advertise the same address through OSPF. Unicast routing selects the reachable RP instance. MSDP exchanges Source-Active information between the RPs using their **unique** addresses, allowing discovery of sources registered at the other RP. See [RFC 3618](https://www.rfc-editor.org/rfc/rfc3618.html).

A known source can remain reachable through established multicast state. That does not by itself demonstrate successful registration of a brand-new source after the failure.

## Configuration and purpose

```cisco
! On RR-P and PE3:
interface Loopback10
 ip address 10.255.0.100 255.255.255.255
 ip pim sparse-mode
!
ip pim rp-address 10.255.0.100 ANYCAST_GROUPS
ip access-list standard ANYCAST_GROUPS
 permit 239.3.3.3
! RR-P:
ip msdp peer 10.255.0.33 connect-source Loopback0
ip msdp originator-id Loopback0
ip msdp cache-sa-state
! PE3:
ip msdp peer 10.255.0.1 connect-source Loopback0
ip msdp originator-id Loopback0
ip msdp cache-sa-state
```

Loopback10 supplies the shared RP address. Loopback0 supplies distinct MSDP endpoints/originator identities. The existing OSPF configuration advertises the loopbacks. The cache preserves SA information for inspection.

## Test sequence

1. Inspect the local Anycast route and MSDP peer on each RP.
2. Confirm PE3 has SA information for (10.255.0.11,239.3.3.3).
3. In the isolated lab, shut down **only RR-P Loopback10**.
4. Inspect OSPF and RPF resolution for 10.255.0.100.
5. Renew CE2's join and compare group counters.
6. Restore Loopback10 and verify recovery before concluding a new test run.

Historical failure action and intended restoration:

```cisco
! RR-P — disruptive lab action, not a read-only check:
configure terminal
interface Loopback10
 shutdown
end
! Inspect the resulting state:
show ip route 10.255.0.100
show ip rpf 10.255.0.100
show ip msdp peer
show ip mroute 239.3.3.3
show ip mroute count
! Restore after the experiment:
configure terminal
interface Loopback10
 no shutdown
end
```

## Observed results and why they matter

| Evidence | Interpretation |
|---|---|
| MSDP Up at both RPs; 0 resets | The unique-address MSDP session was established |
| PE3 SA cache contains (10.255.0.11,239.3.3.3), originated by 10.255.0.1 | Source information reached the other RP |
| PE3 (S,G) flags MT, later MTA/TA; OIL Fa1/0 | Captured state includes a receiver-facing branch |
| RR-P learns 10.255.0.100/32 through OSPF, next hop 10.0.34.2, metric 11 | Removing the local RP address makes the remote RP instance the routed destination |
| RPF for the RP uses Ethernet1/0 | The RP-facing direction changed consistently with the route |
| After CE2 rejoined, PE2 had (*,G)/(S,G), OIL Fa1/0 and source counters 24→26 | Known-source forwarding continued in the captured failure condition |

The failed component was one RP **loopback**, not the entire RR-P router. RR-P remained a transit node. This topology does not demonstrate survival of a complete central-router outage.

## Limits and troubleshooting

The capture does not show registration of a previously unseen source after the failure or a measured convergence interval. The historical evidence file says restoration was recommended but contains no separate confirmation log; do not treat that instruction as proof of execution.

If the remote RP is not selected, inspect its /32 advertisement and OSPF route. If MSDP is down, check reachability between the unique endpoints. If SA exists but receivers see no traffic, inspect RPF, PIM joins and OIL rather than treating SA cache presence as delivery proof.

[Full output and failure sequence](evidencias/LAB04_ANYCAST_RP_MSDP.txt)
