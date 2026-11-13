# LAB 05 — IPv6 Multicast: OSPFv3, PIM-SM, MLDv2 and SSM

**Test date:** 2026-11-13. **Platform:** seven Cisco IOS routers in EVE-NG. **Result:** IPv6 ASM and SSM exercised with MLDv2. **MLDv1 was not tested.**

Operational evidence comes from user-supplied console excerpts. The seven post-test configuration files were separately supplied and reviewed. This editorial revision did not rerun the multicast tests.

![IPv6 multicast uses the same seven-router topology](topology/multicast-eve-ng.png)

## Objectives

1. Establish IPv6 unicast reachability through OSPFv3 while retaining IPv4.
2. Test ASM group FF1E::1234 with a static RP and two receivers.
3. Test SSM group FF3E::1234 with a selected source.
4. Compare permitted and non-selected source addresses without overstating where a packet was dropped.

## Addressing and prerequisites

| Node or link | IPv6 address/prefix |
|---|---|
| CE1 / PE1 Loopback0 | 2001:DB8:100::11/128 / ::12/128 |
| RR-P Loopback0 / ASM RP | 2001:DB8:100::1/128 |
| PE2 / CE2 Loopback0 | 2001:DB8:100::23/128 / ::22/128 |
| PE3 / CE3 Loopback0 | 2001:DB8:100::33/128 / ::32/128 |
| CE1–PE1 | 2001:DB8:1::/64; CE1 ::1, PE1 ::2 |
| PE1–RR-P | 2001:DB8:12::/64 |
| RR-P–PE2 | 2001:DB8:23::/64 |
| PE2–CE2 | 2001:DB8:2::/64; CE2 ::2 |
| RR-P–PE3 | 2001:DB8:34::/64 |
| PE3–CE3 | 2001:DB8:3::/64; CE3 ::2 |

The baseline uses ipv6 unicast-routing, ipv6 cef, OSPFv3 process 10/area 0 and interface-level ipv6 ospf 10 area 0. Router IDs are distinct IPv4-format identifiers; they are not IPv6 next-hop addresses.

## 1. Verify unicast before multicast

```cisco
show ipv6 ospf neighbor
show ipv6 route ospf
```

RR-P showed PE3 FULL/BDR on Ethernet1/0, PE2 FULL/DR on Ethernet1/1 and PE1 FULL/DR on Ethernet1/2. Routes to the remote loopbacks and transit prefixes used link-local FE80:: next hops. CE1-loopback to PE1-loopback and CE3-loopback to CE2-loopback pings each returned 5/5.

**Why:** unicast routing supplies reachability and RPF information. An OSPFv3 adjacency alone is not proof of multicast reception.

## 2. ASM: membership, RP and source state

Group: **FF1E::1234**. RP: **2001:DB8:100::1**. Successful source: **2001:DB8:1::1** on CE1 Fa0/0. Receivers: CE2 and CE3.

Observed configuration excerpts:

```cisco
! On the IPv6-configured routers:
ipv6 multicast-routing
ipv6 pim rp-address 2001:DB8:100::1
! CE2 and CE3:
interface FastEthernet0/0
 ipv6 mld join-group FF1E::1234
```

The first command enables IPv6 multicast forwarding; the second supplies the static ASM RP. The join makes each CE a local test receiver.

| Evidence | Interpretation |
|---|---|
| RR-P has three IPv6 PIM neighbors | The central PIM adjacencies exist |
| Group-map reports SM and static RP 2001:DB8:100::1 | The group selects the intended RP |
| CE3 reports current MLD version 2 and (*,G) SCLJ with null OIL | Local membership is present |
| RR-P (*,G) OIL includes Ethernet1/0 and Ethernet1/1; IIF Tunnel6 | The captured RP state has branches toward PE3 and PE2 |
| PE3 (*,G) SC, then (2001:DB8:1::1,G) ST; Fa0/0 IIF and Fa1/0 OIL | Captured source state connects upstream traffic to CE3 |
| PE1 (S,G) SFT; RR-P (S,G) ST | Source/Register-related and SPT state was observed |
| RR-P: 3 Data Registers received, 1 Null Register received, 2 Register-Stops sent | Register exchange occurred; PE1 also reported 2 Register-Stops received |

A ping sourced from CE1 Loopback0 initially timed out; the cause was not isolated. A ping sourced from CE1 Fa0/0 returned **5/5 with 11 multicast replies**, including CE2 2001:DB8:2::2 and CE3 2001:DB8:3::2. Preserve this recorded count rather than replacing it with an assumed ten.

The PIM Packet Sent on Loopback Errors counter reached 33 on PE1/RR-P, but no causal link to traffic loss was demonstrated. RR-P's captured (S,G) listed only Ethernet1/1 although its (*,G) listed both branches; PE3 separately showed source state toward CE3. These are time-specific observations, not a synchronized packet trace.

## 3. SSM: request a source/group channel

Group: **FF3E::1234**. Selected source: **2001:DB8:1::1**. SSM does not require an RP or PIM Register for this channel.

```cisco
! CE2 and CE3:
interface FastEthernet0/0
 ipv6 mld join-group FF3E::1234 2001:DB8:1::1
```

This is the syntax actually serialized in the snapshots. The word INCLUDE describes the source-selection behavior; the IOS running-config did not include that keyword.

```cisco
show ipv6 mld interface FastEthernet0/0
show ipv6 mld groups
show ipv6 mroute FF3E::1234
show ipv6 mroute FF3E::1234 count
show ipv6 rpf 2001:DB8:1::1
```

PE2 and PE3 showed (2001:DB8:1::1,FF3E::1234), flags sTI, IIF Fa0/0 and OIL Fa1/0. RPF pointed toward RR-P. CE2 showed sPLTI with null OIL. The permitted-source ping returned **5/5 with 10 multicast replies**, five from each receiver.

CE2 reported SW Forwarding 0, Other drops 3→4→5 and RPF failed 0. Because CE2 is a local receiver, a forwarding counter alone cannot quantify local delivery; the reply evidence is more direct. PE2 later showed SW Forwarding 8 and Other 0/0/0 for the selected source.

## 4. Positive/negative source-selection test

A second address was temporarily added to CE1 Fa0/0 during the historical test:

```cisco
interface FastEthernet0/0
 ipv6 address 2001:DB8:1::99/64
```

| Command | Recorded outcome | Interpretation |
|---|---|---|
| ping ipv6 FF3E::1234 source 2001:DB8:1::99 repeat 5 | 0/5; no receiver replies | Consistent with excluding a non-selected source |
| ping ipv6 FF3E::1234 source 2001:DB8:1::1 repeat 5 | 5/5; 10 replies | Selected source reaches both test receivers |

The comparison supports source filtering. No simultaneous capture located the exact discard point for ::99; do not attribute the timeout to a specific interface without additional evidence.

## Command-to-question reference

| Question | Command |
|---|---|
| Are IPv6 PIM adjacencies present? | show ipv6 pim neighbor |
| Which RP serves the ASM group? | show ipv6 pim group-map FF1E::1234 |
| Which MLD version is active? | show ipv6 mld interface FastEthernet0/0 |
| Is receiver membership installed? | show ipv6 mld groups |
| Which input/output interfaces are used? | show ipv6 mroute FF1E::1234 |
| Is source-specific state present? | show ipv6 mroute FF3E::1234 |
| Are packets/counter failures changing? | show ipv6 mroute FF3E::1234 count |
| Does RPF point toward the real source? | show ipv6 rpf 2001:DB8:1::1 |
| Was Register exchange observed? | show ipv6 pim traffic |

## Snapshot review and unresolved points

The [2026-11-13 snapshot](configs/snapshot-2026-11-13/) has seven expected hostnames, complete end markers, IPv6 routing/CEF/multicast, OSPFv3 process 10/area 0, passive Loopback0 and the static RP. Six transit links have matching /64 subnets. CE2/CE3 retain ASM and SSM joins.

CE1 retains 2001:DB8:1::1/64 and no longer contains ::99. This later snapshot resolves the earlier evidence file's cleanup question, but does not prove startup-config persistence.

MLDv1 remains untested: the image reported MLDv2 and did not expose the expected version choice under ipv6 mld ?. The original Loopback0-source timeout and PIM loopback counter remain unexplained. No new network execution was performed as part of the snapshot review or English rewrite.

[Historical evidence](evidencias/LAB05-IPv6-PIM-MLDv2.txt) · [Pre-IPv6 snapshot](configs/snapshot-2026-11-12/) · [Post-test snapshot](configs/snapshot-2026-11-13/)
