# LAB 06 — VPWS / Ethernet-over-MPLS (L2VPN) with Cisco IOS and IOS XRv

**Date:** 14 November 2026 · **Platform:** EVE-NG; R1/R3 Cisco IOS 15.2; R2 Cisco IOS 12.4; XR1 IOS XRv classic 6.3.1; two IOS L2 CEs.

**Outcome:** LDP-signaled VPWS between R2 and R1 **passed bidirectional Ethernet/IP forwarding**. The earlier XRv-to-R1 attempt signaled PW UP but did not carry CE-to-CE traffic. The XRv cross-connect was removed from the collected final config; original L3VPN remained.

## Topology used

```text
                         XR1 (IOS XRv 6.3.1, L3VPN PE)
                           |
L2_CE1 --Fa0/1-- R2 --Fa0/0-- R3 --Fa0/0-- R1 --Fa1/0-- L2_CE2
  .1/24            2.2.2.2         3.3.3.3       1.1.1.1        .2/24
                    PE              P            PE

        <-------------- targeted-LDP pseudowire VC ID 100 ---------->
```

The graph is logical; consult the interface descriptions/configs for each physical interface. The original XR1–R3–R1 L3VPN CUST-A path remains configured. The local CE interface is `Fa0/0` on both L2 CEs. XR1 does **not** participate in the final VPWS.

## Address and service plan

| Function | Device / interface | Address |
|---|---|---|
| PE 1 loopback / PW endpoint | R2 Lo0 | `2.2.2.2/32` |
| PE 1 → core P | R2 Fa0/0 | `10.0.0.9/30` |
| P → PE 1 | R3 Fa2/0 | `10.0.0.10/30` |
| PE 2 loopback / PW endpoint | R1 Lo0 | `1.1.1.1/32` |
| PE 2 → P | R1 Fa2/0 | `10.0.0.6/30` |
| P → PE 2 | R3 Fa0/0 | `10.0.0.5/30` |
| Customer Ethernet site 1 | L2_CE1 Fa0/0 | `192.168.100.1/24` |
| Customer Ethernet site 2 | L2_CE2 Fa0/0 | `192.168.100.2/24` |
| Pseudowire | R2 → R1 | LDP VC ID `100`, PW type Ethernet, MTU 1500 |

## Configuration highlights (verified from final show run)

**R2 (new IOS PE):**

```cisco
mpls label protocol ldp
mpls ldp router-id Loopback0 force
!
interface Loopback0
 ip address 2.2.2.2 255.255.255.255
!
interface FastEthernet0/0
 ip address 10.0.0.9 255.255.255.252
 ip router isis CORE
 speed 100
 full-duplex
 mpls ip
!
interface FastEthernet0/1
 no ip address
 speed 100
 full-duplex
 xconnect 1.1.1.1 100 encapsulation mpls
!
router isis CORE
 net 49.0001.0000.0002.0002.00
 is-type level-2-only
 metric-style wide
 passive-interface Loopback0
```

**R3 (P), added R2-facing port:**

```cisco
interface FastEthernet2/0
 description LINK-TO-R2
 ip address 10.0.0.10 255.255.255.252
 ip router isis CORE
 duplex full
 mpls ip
```

R3 also has `mpls ldp autoconfig` under IS-IS. **R1 (existing IOS PE):**

```cisco
interface FastEthernet1/0
 description L2VPN-VPWS-TO-L2_CE2
 no ip address
 duplex full
 no keepalive
 xconnect 2.2.2.2 100 encapsulation mpls
```

The CEs have only their interface IPs; they do not need MPLS, LDP or an L3 routing adjacency for this VPWS.

## Control-plane / dataplane validation

1. **R2–R3 access link:** initial `show interfaces Fa0/0` displayed **10 Mb/s half-duplex**, despite the running configuration showing a duplex directive. A CDP duplex mismatch was logged. Changing R2 to fixed `speed 100` and full duplex led to an operational **100 Mb/s full-duplex**, zero interface input/output errors in the captured output. R3 had `duplex full`.
2. **Underlay:** R2 `show isis neighbors` reported R3 Level-2 UP. R2 LDP session to `3.3.3.3:0` was Oper; targeted LDP session to `1.1.1.1:0` was Oper. R2 learned `1.1.1.1/32` via IS-IS from `10.0.0.10`.
3. **MPLS:** R2 LFIB contained label `19` for `1.1.1.1/32`, outgoing transport label `17` toward R3. A separate local label `16` identified `l2ckt(100)`.
4. **VPWS PW:** R2 `show mpls l2transport vc detail`: `Fa0/1` up/up; neighbor `1.1.1.1`, VC 100 UP; locally allocated service label `16`, remote service label `23`; stack imposed toward remote PE `{17 23}` (transport label + service label). MTU 1500/1500. Targeted LDP up.
5. **Data-plane proof:** `L2_CE1 → L2_CE2` ICMP 9/10 after clearing ARP; reverse `L2_CE2 → L2_CE1` ICMP 10/10. Each CE resolved the other CE's MAC. R2 VC stats receive `65`, send `77`, with drops `0`.

### Earlier unsuccessful XRv attempt (historical observation)

Initially, XR1 `GigabitEthernet0/0/0/1 l2transport` was joined to R1 through an LDP-signaled PW 100. Both displayed PW `UP`, MTU matched and CW was disabled, yet CE ping was **0/10**. The XRv showed **85 physical Ethernet input packets** but the L2VPN AC/PW service counters remained zero in `show l2vpn xconnect detail`. R1 registered `send 84`, `receive 0` on that PW. This is consistent with a known **XRv classic virtual data-plane limitation**, but no packet capture isolated a definitive defect. The final archived XR1 config no longer has that xconnect and Gi0/0/0/1 is shutdown.

### Why this matters for CCNP/CCIE SP

- A pseudowire marked **UP** validates control-plane signaling; it **does not prove** Ethernet delivery.
- The **outer label** transports toward the egress PE; the **inner VC/service label** identifies the pseudowire on that PE.
- LDP adjacencies to the core are hop-by-hop; **targeted LDP** between the two PEs signals the PW without direct physical adjacency.
- An L2VPN point-to-point circuit extends the Ethernet segment across MPLS. CE-to-CE ARP plus two-way ping and changing VC counters are stronger evidence than `show xconnect` alone.
- The 10 Mb half-duplex operational condition on R2 was distinct from the XRv forwarding failure and was corrected before final validation.

## Fast verification commands

```cisco
! Cisco IOS (R1/R2/R3)
show isis neighbors
show mpls ldp neighbor
show mpls forwarding-table
show mpls l2transport vc
show mpls l2transport vc detail
show interfaces FastEthernet0/0
show ip arp
ping 192.168.100.2 repeat 10
```

```cisco
! Cisco IOS XR (XR1) — historical troubleshooting
show l2vpn xconnect
show l2vpn xconnect detail
show interfaces GigabitEthernet0/0/0/1
show mpls forwarding
show configuration commit list
```

## Evidence, backups and boundaries

- [Six collected running-config snapshots](configs/LAB06-VPWS-2026-11-14/): R1, R2, R3, XR1, L2_CE1, L2_CE2.
- [Exact CLI excerpts from the study session](evidencias/LAB06-VPWS-2026-11-14/CLI-observed-2026-11-14.txt).
- [Collection results and persistence verification](evidencias/LAB06-VPWS-2026-11-14/COLLECTION-AND-PERSISTENCE.md).
- **Confirmed startup persistence:** R1, R2 and R3 (`write memory`, startup equals running in user-supplied archive).
- **XR1:** IOS XR committed running configuration, including preserved L3VPN; no new changes requested at final collection.
- **L2_CE1 and L2_CE2:** only running-config captured, persistence **not confirmed**; saving them was not part of the recorded read-only operation.
- **L3VPN CE1_A/CE2_A:** intentionally excluded; they belong to the preceding L3VPN lab. CE1_B/CE2_B were unresponsive in the archive and were not used in this VPWS validation.

Review every new backup before uploading to a public repository. Avoid posting secrets or production/customer configurations.
