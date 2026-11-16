# LAB 11 — SR-MPLS Fundamentals with Two IOS XRv

**My goal:** verify whether **IOS XRv classic 6.3.1** can distribute Segment Routing SIDs and install MPLS forwarding entries, using just two routers.

## My topology

```text
XR1  Lo0 1.1.1.1/32                XR2  Lo0 2.2.2.2/32
     Gi0/0/0/0 10.0.12.1/30 -------- Gi0/0/0/0 10.0.12.2/30
                         IS-IS L2, metric 10
```

| Setting | XR1 | XR2 |
|---|---|---|
| Prefix-SID index | **1** | **2** |
| Node-SID | **16001** | **16002** |
| SRGB | 16000–23999 | 16000–23999 |

## What I configured

I enabled SR-MPLS under the IS-IS IPv4 unicast address-family, kept Loopback0 passive and assigned a Prefix-SID index to each loopback.

```cisco
router isis CORE
 is-type level-2-only
 address-family ipv4 unicast
  segment-routing mpls
 interface Loopback0
  passive
  address-family ipv4 unicast
   prefix-sid index 1
```

That excerpt is from **XR1**; XR2 uses index **2**. Both complete running configurations are linked below.

## What I observed (2026-11-16)

| Test | XR1 | XR2 |
|---|---|---|
| IS-IS Level-2 | Neighbor XR2 **UP** | Route to XR1 via IS-IS |
| Remote route | `2.2.2.2/32 labeled SR` | `1.1.1.1/32 labeled SR` |
| Remote Prefix-SID | **16002** | **16001** |
| MPLS LFIB | `16002 Pop` | `16001 Pop` |
| Local Adj-SIDs in LFIB | `24000 / 24001` | `24000 / 24001` |
| Loopback ping | **5/5** | **5/5** |

In the IS-IS database, both nodes advertised an **SRGB base 16000, range 8000** and their respective Prefix-SID indexes. Both also advertised **Adj-SID 24001** for their *own* outgoing adjacency. An Adj-SID is **locally significant**, so reusing 24001 on both routers is valid.

I saw the Prefix-SID LFIB counter on XR1 rise **520 → 1560 bytes**. The two Adj-SID LFIB counters stayed at zero. `Pop` is consistent with **PHP** on this directly connected path.

```cisco
show isis neighbors
show isis database verbose
show isis segment-routing label table
show route 2.2.2.2/32
show mpls forwarding
ping 2.2.2.2 source 1.1.1.1
```

## What I learned

**I confirmed both SID advertisement and LFIB programming on classic XRv.** I did not confuse that with a multi-hop SR-TE test: two routers on one link cannot show alternative path steering. The pings prove IP connectivity, not that those ICMP packets carried a particular SR label.

**Limit:** no tested SR-TE policy, segment stack, TI-LFA, explicit Adj-SID packet forwarding or reboot persistence.

**Evidence:** [XR1 running-config](configs/LAB11-SR-MPLS-2026-11-16/XR1-running.cfg) · [XR2 running-config](configs/LAB11-SR-MPLS-2026-11-16/XR2-running.cfg) · [Full CLI excerpts, provenance and hashes](evidencias/LAB11-SR-MPLS-2026-11-16/DETAILED-ORIGINAL-REPORT.md).
