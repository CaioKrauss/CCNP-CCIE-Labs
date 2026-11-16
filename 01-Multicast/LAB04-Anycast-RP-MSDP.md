# LAB 04 — Anycast RP and MSDP

**My goal:** observe how multicast behaves when one Anycast RP address disappears. I used **239.3.3.3** and shared RP IP **10.255.0.100/32** on RR-P and PE3.

![My multicast topology](topology/multicast-eve-ng.png)

## What I configured

Both RPs used the same RP loopback but **different MSDP peer addresses**:

```cisco
! Both RPs:
interface Loopback10
 ip address 10.255.0.100 255.255.255.255
 ip pim sparse-mode
!
ip pim rp-address 10.255.0.100 ANYCAST_GROUPS
ip access-list standard ANYCAST_GROUPS
 permit 239.3.3.3
! RR-P peers with 10.255.0.33; PE3 peers with 10.255.0.1.
```

The actual MSDP commands and snapshots are in the linked evidence/configs.

## What I tested

1. I checked MSDP peers and the Source-Active (SA) cache for source `10.255.0.11`.
2. I shut **RR-P Loopback10**, not the entire router.
3. I inspected the new OSPF route/RPF path to the shared RP address and repeated CE2's join.

## What I observed

- Both MSDP sessions were **Up**; PE3 learned the source through SA information.
- RR-P routed `10.255.0.100/32` through PE3 (`10.0.34.2`, metric 11).
- PE2 still showed receiver-facing multicast state, and the source packet count rose **24 → 26**.

## What I learned

**Anycast RP provides another reachable RP address; MSDP shares source discovery between RPs.** I demonstrated continuity for an **already-known source**, not registration of a new source after failure. The recorded session did **not** separately prove that I restored Loopback10.

```cisco
show ip route 10.255.0.100
show ip rpf 10.255.0.100
show ip msdp peer
show ip msdp sa-cache
show ip mroute 239.3.3.3
```

**Evidence:** [Failure sequence and CLI](evidencias/LAB04_ANYCAST_RP_MSDP.txt) · [IPv4 configs](configs/snapshot-2026-11-12/). Only run shutdown/recovery in an isolated lab.
