# LAB 01 — PIM-SM / ASM

**My goal:** understand how a receiver joins group **239.1.1.1** through a static RP (**RR-P, 10.255.0.1**).

![My multicast topology](topology/multicast-eve-ng.png)

## What I configured

I enabled multicast routing and PIM-SM on the relevant interfaces, mapped this ASM group to the RP and used CE2/CE3 as test receivers.

```cisco
ip multicast-routing
ip pim rp-address 10.255.0.1 ASM_GROUPS
ip access-list standard ASM_GROUPS
 permit 239.1.1.1
! On participating interfaces:
ip pim sparse-mode
! On the receiver:
ip igmp join-group 239.1.1.1
```

## What I observed

- **IGMP:** CE2 joined `239.1.1.1`.
- **Shared tree:** PE2 showed `(*,239.1.1.1)` pointing upstream to RR-P and downstream to CE2.
- **Source state:** I also saw `(10.255.0.11,239.1.1.1)` with the IOS **T** flag (SPT indication).
- **RPF:** I checked the path back toward CE1; CE1 used different source addresses in different captures.

## What I learned

**ASM starts from receiver interest in a group.** The last-hop router can build `(*,G)` toward the RP; source-specific state can appear afterward. The T flag is useful evidence, but a `(S,G)` entry alone does not prove packet delivery. A local receiver can have a null OIL.

```cisco
show ip pim rp mapping
show ip igmp groups
show ip mroute 239.1.1.1
show ip rpf 10.255.0.11
show ip mroute count
```

**Limit:** I recorded control-plane state, not comparable receiver delivery counters. My topology has only one physical path.

**Evidence:** [CLI capture](evidencias/LAB01_PIM_SM_ASM.txt) · [IPv4 configs](configs/snapshot-2026-11-12/) · [Addressing](topology/enderecamento.md).
