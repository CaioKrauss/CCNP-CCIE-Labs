# LAB 03 — Bidirectional PIM (BIDIR)

**My goal:** send traffic from multiple sources over a shared multicast tree for **239.2.2.2**, using RP address **10.255.0.2** on RR-P.

![My multicast topology](topology/multicast-eve-ng.png)

## What I configured

```cisco
ip pim bidir-enable
ip pim rp-address 10.255.0.2 BIDIR_GROUPS bidir
ip access-list standard BIDIR_GROUPS
 permit 239.2.2.2
! On CE2/CE3 receiver interfaces:
ip igmp join-group 239.2.2.2
```

I kept PIM and unicast reachability on the participating interfaces. I tested sources on CE1 and CE3.

## What I observed

- PE2 installed `(*,239.2.2.2)` with BIDIR flags and upstream direction toward RR-P.
- **Designated Forwarder (DF):** RR-P won on the PE2–RR-P link; PE2 won on the CE-facing link.
- The RP-tree packet counter rose **14 → 15 → 17**.
- The display showed **source count 0** while shared-tree counters increased.

## What I learned

**BIDIR uses one shared `(*,G)` tree for multiple senders.** DF election controls who forwards toward the RP on each link. Unlike ASM's source-specific behavior, BIDIR does not rely on per-source SPT state or PIM Register.

```cisco
show ip pim interface df
show ip mroute 239.2.2.2
show ip mroute count
```

**Limit:** I did not preserve independent counter runs for each sender. This test did not measure RP failover.

**Evidence:** [CLI and counter captures](evidencias/LAB03_PIM_BIDIR.txt).
