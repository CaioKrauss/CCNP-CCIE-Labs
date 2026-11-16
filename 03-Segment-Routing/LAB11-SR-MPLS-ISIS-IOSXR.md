# LAB 11 — SR-MPLS Fundamentals with IS-IS (IOS XRv 6.3.1)

**Platform:** 2 Cisco IOS XRv classic 6.3.1 instances in EVE-NG.  
**Observed:** 2026-11-16.  
**Status:** IS-IS L2 adjacency, SR advertisements, prefix/adjacency SID visibility, SR-programmed forwarding entries and bidirectional loopback reachability verified. **Complete XR1/XR2 running configurations collected, checked against the ZIP and published; post-reboot persistence not tested.**

## Objective and topology

Validate SR-MPLS on the lightweight IOS XRv classic image without assuming that the ability to advertise SIDs alone implies functioning label forwarding.

```text
XR1                                              XR2
Lo0: 1.1.1.1/32                                  Lo0: 2.2.2.2/32
Node-SID index: 1 (16001)                        Node-SID index: 2 (16002)
Gi0/0/0/0: 10.0.12.1/30 ---- IS-IS L2 ---- Gi0/0/0/0: 10.0.12.2/30
                         metric 10
```

| Parameter | XR1 | XR2 |
|---|---|---|
| Router ID / Loopback0 | 1.1.1.1/32 | 2.2.2.2/32 |
| Link | 10.0.12.1/30 | 10.0.12.2/30 |
| IS-IS level | Level 2 | Level 2 |
| SRGB | base 16000, range 8000 | base 16000, range 8000 |
| Prefix-SID index | 1 | 2 |
| Derived Node-SID label | 16001 | 16002 |

The local SRGB label range is **16000–23999** and the Node-SIDs are `16000 + index`. This lab has one point-to-point link and therefore no alternative path for SR-TE path steering.

## Configuration scope

The interactive setup in this exercise used IS-IS process `CORE`, Loopback0 as a passive IS-IS interface, level-2-only operation and SR-MPLS enabled under the IS-IS IPv4 unicast address family. Prefix-SID indexes were configured per Loopback0.

## Captured configuration backups and provenance

The user supplied full `show running-config` outputs and the collector ZIP `20261116-180310.zip` for EVE-NG lab `SR-MPLS.unl`. The separate `XR1.cfg` and `XR2.cfg` match the archive's router files byte for byte. No passwords, secrets, or keys were found in these lab configs.

- [XR1 — captured running-config](configs/LAB11-SR-MPLS-2026-11-16/XR1-running.cfg)
- [XR2 — captured running-config](configs/LAB11-SR-MPLS-2026-11-16/XR2-running.cfg)

The collection manifest states **2026-11-16 18:03:12 -03:00**, both routers **complete**, and an IOS XR commit-history entry on each router. The original files use CRLF; LF normalization produces 885 bytes per config and these hashes match the manifest:

| Router | SHA-256 after LF normalization |
|---|---|
| XR1 | `9f68ec5fb3376042b3325d4d6123090c201d79fb18e84eaab276895dcf1a4136` |
| XR2 | `6a83ebb7e333eb6688b14041957e9f48ea765ccff03765976534f` |

**Configuration audit:** both backups have `router isis CORE`, `is-type level-2-only`, `segment-routing mpls` in the IS-IS IPv4 unicast address-family, passive Loopback0, `prefix-sid index 1/2`, and metric 10 on Gi0/0/0/0. A global `mpls traffic-eng` stanza is present but is **not** an SR-TE policy. No SR-TE segment-list or TI-LFA configuration was captured.

Captured IOS XR running configuration and commit metadata are not a post-reboot persistence test. These are point-in-time snapshots only.

## Owner-observed evidence

### IS-IS and route installation

XR1:

```text
RP/0/0/CPU0:XR1#show isis neighbors
System Id      Interface        SNPA           State Holdtime Type IETF-NSF
XR2            Gi0/0/0/0        *PtoP*         Up    25       L2   Capable

RP/0/0/CPU0:XR1#show route 2.2.2.2/32
Routing entry for 2.2.2.2/32
  Known via "isis CORE", distance 115, metric 10, labeled SR, type level-2
  Routing Descriptor Blocks
    10.0.12.2, from 2.2.2.2, via GigabitEthernet0/0/0/0
      Route metric is 10
```

XR2:

```text
RP/0/0/CPU0:XR2#show route 1.1.1.1/32
Routing entry for 1.1.1.1/32
  Known via "isis CORE", distance 115, metric 10, labeled SR, type level-2
  Routing Descriptor Blocks
    10.0.12.1, from 1.1.1.1, via GigabitEthernet0/0/0/0
      Route metric is 10
```

A previous `show route isis 2.2.2.2` returned `No matching routes found`, but the targeted `show route 2.2.2.2/32` immediately established that the route **was installed**. The initial result must not be described as an IS-IS outage.

### Prefix-SIDs and SRGB in the IS-IS LSDB

The user captured both routers' Level-2 LSPs in `show isis database verbose` on XR1. Relevant excerpts:

```text
XR1.00-00
  Metric: 0          IP-Extended 1.1.1.1/32
    Prefix-SID Index: 1, Algorithm:0, R:0 N:1 P:0 E:0 V:0 L:0
  Router Cap:     1.1.1.1, D:0, S:0
    Segment Routing: I:1 V:0, SRGB Base: 16000 Range: 8000
    SR Algorithm:
      Algorithm: 0
      Algorithm: 1

XR2.00-00
  Metric: 0          IP-Extended 2.2.2.2/32
    Prefix-SID Index: 2, Algorithm:0, R:0 N:1 P:0 E:0 V:0 L:0
  Router Cap:     2.2.2.2, D:0, S:0
    Segment Routing: I:1 V:0, SRGB Base: 16000 Range: 8000
    SR Algorithm:
      Algorithm: 0
      Algorithm: 1
```

Algorithm 0/1 capability advertisements are **not** evidence of a configured SR policy or traffic steering.

### Prefix label table (both directions)

```text
XR1#show isis segment-routing label table
Label         Prefix/Interface
16001         Loopback0
16002         2.2.2.2/32

XR2#show isis segment-routing label table
Label         Prefix/Interface
16001         1.1.1.1/32
16002         Loopback0
```

### Adjacency SID advertisements

Each router advertised an Adj-SID of 24001 for its own local outgoing direction on the same inter-router link:

```text
XR1.00-00: IS-Extended XR2.00
  Interface IP Address: 10.0.12.1
  Neighbor IP Address: 10.0.12.2
  ADJ-SID: F:0 B:0 V:1 L:1 S:0 P:0 weight:0 Adjacency-sid:24001

XR2.00-00: IS-Extended XR1.00
  Interface IP Address: 10.0.12.2
  Neighbor IP Address: 10.0.12.1
  ADJ-SID: F:0 B:0 V:1 L:1 S:0 P:0 weight:0 Adjacency-sid:24001
```

Adj-SIDs are **locally significant**; the same numeric label at XR1 and XR2 does not identify a shared global segment. The LFIB also contains label 24000, but the supplied verbose IS-IS excerpt explicitly identifies only 24001 for the advertised point-to-point adjacency. No adjacency-directed traffic was generated.

### MPLS LFIB on XR1

```text
XR1#show mpls forwarding
Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes
Label  Label       or ID              Interface                    Switched
16002  Pop         SR Pfx (idx 2)     Gi0/0/0/0    10.0.12.2       1560
24000  Pop         SR Adj (idx 1)     Gi0/0/0/0    10.0.12.2       0
24001  Pop         SR Adj (idx 3)     Gi0/0/0/0    10.0.12.2       0
```

The SR Prefix-SID counter rose from **520 to 1560 bytes** across two observations.

### MPLS LFIB on XR2

```text
XR2#show mpls forwarding
Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes
Label  Label       or ID              Interface                    Switched
16001  Pop         SR Pfx (idx 1)     Gi0/0/0/0    10.0.12.1       520
24000  Pop         SR Adj (idx 1)     Gi0/0/0/0    10.0.12.1       0
24001  Pop         SR Adj (idx 3)     Gi0/0/0/0    10.0.12.1       0
```

`Pop` is consistent with penultimate-hop popping for the directly connected destination. The LFIB proves SR-labeled entries are programmed; the counters show traffic on the prefix-label entries. They do not identify which test packets incremented them or independently establish end-to-end label imposition for a multi-hop transport path.

### Bidirectional reachability

```text
XR1#ping 2.2.2.2 source 1.1.1.1
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 1/2/9 ms

XR2#ping 1.1.1.1 source 2.2.2.2
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 1/1/1 ms
```

These tests establish **IP reachability**, not that ICMP packets used a given SR label.

## Verification commands

```cisco
show isis neighbors
show isis interface
show isis database verbose
show isis segment-routing label table
show route 2.2.2.2/32
show route 1.1.1.1/32
show mpls forwarding
ping 2.2.2.2 source 1.1.1.1
ping 1.1.1.1 source 2.2.2.2
show running-config
```

## Result and limitations

**Validated:** IS-IS L2 UP, IPv4 Loopbacks installed as SR-labeled IS-IS routes, advertised SRGB/prefix SIDs/Adj-SIDs, installed MPLS LFIB entries, MPLS label counters nonzero, IP ping 5/5 in each direction.

**Not validated:** persistence after reboot, SR-TE policy, imposed multi-segment stack, alternative-path steering, TI-LFA, convergence, latency under failure, explicit Adj-SID packet forwarding, service traffic over SR-MPLS, or physical packet capture.

The lab demonstrates working **SR-MPLS fundamentals on two IOS XRv classic instances** within these evidence limits.

**Related:** [LAB 10 — RSVP-TE CSPF, Affinity and Preemption](../02-MPLS-TE/LAB10-MPLS-TE-CSPF-AFFINITY-PREEMPTION-IOS.md).
