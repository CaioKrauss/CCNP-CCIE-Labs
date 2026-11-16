# LAB 02 — PIM-SSM and IGMPv3

**My goal:** let each receiver choose **both a source and a group** instead of joining any source for the same group.

![My multicast topology](topology/multicast-eve-ng.png)

## What I configured

For group **232.1.1.1**, CE2 requested source **10.255.0.11** and CE3 requested **10.0.1.1**. Both are CE1 addresses, but they define different `(S,G)` channels.

```cisco
! On participating routers:
ip pim ssm default
! CE2, Fa0/0:
ip igmp version 3
ip igmp join-group 232.1.1.1 source 10.255.0.11
! CE3, Fa0/0:
ip igmp version 3
ip igmp join-group 232.1.1.1 source 10.0.1.1
```

## What I observed

- PE2 installed `(10.255.0.11,232.1.1.1)` toward CE2.
- PE3 installed `(10.0.1.1,232.1.1.1)` toward CE3.
- PE2's packet counter increased **26 → 28**, with **0 RPF failures**.
- CE2 showed a null OIL because it was the local test receiver.

## What I learned

**SSM joins the source directly; it does not need an RP or a PIM Register.** The source IP must match the receiver's IGMPv3 request. A T flag here does not mean ASM switched from an RP tree.

```cisco
show ip igmp groups
show ip mroute 232.1.1.1
show ip rpf 10.255.0.11
show ip mroute count
```

**Limit:** I have a PE2 counter increase, but no separate measured packet-count series for CE3's source.

**Evidence:** [CLI capture](evidencias/LAB02_PIM_SSM_IGMPv3.txt) · [Addressing](topology/enderecamento.md).
