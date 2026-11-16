# LAB 08 — RSVP-TE, Explicit Path and Autoroute

**My goal:** build an RSVP-TE tunnel over a path different from the normal IS-IS shortest path, then verify local Autoroute and RSVP bandwidth reservation.

## My topology

```text
               R2 (metric 10+10 = 20)
             /                     \
R1 1.1.1.1                           R4 4.4.4.4
             \                     /
               R3 (metric 30+10 = 40)

Normal IS-IS path: R1 → R2 → R4
My explicit TE path: R1 → R3 → R4
```

I used four Cisco 7200 routers with IOS 15.2(4)S7, IS-IS Level 2, MPLS/LDP and RSVP bandwidth of 10 Mbps per participating interface.

## What I configured on R1

```cisco
ip explicit-path name VIA_R3 enable
 next-address 10.0.13.2
 next-address 10.0.34.2
!
interface Tunnel100
 ip unnumbered Loopback0
 tunnel mode mpls traffic-eng
 tunnel destination 4.4.4.4
 tunnel mpls traffic-eng autoroute announce
 tunnel mpls traffic-eng priority 7 7
 tunnel mpls traffic-eng bandwidth 1000
 tunnel mpls traffic-eng path-option 1 explicit name VIA_R3
```

The **explicit path** selects R3. `autoroute announce` makes **R1** resolve the destination through Tunnel100; it does not change the advertised IS-IS topology.

## What I observed (2026-11-16)

| Test | My result |
|---|---|
| Normal IGP path | R1 → R2 → R4, metric **20** |
| Tunnel100 | RSVP signaling **UP**, via R3 with ERO `10.0.13.2 → 10.0.34.2` |
| Autoroute | RIB/CEF on R1 used **Tunnel100**, despite the lower-cost IGP path |
| RSVP reservation | **1 → 5 → 1 Mbps**, with updated LSP instances/labels |
| R3 transit | In-label **20**, outgoing `implicit-null` (PHP) |
| Final R1 → R4 ping | **10/10** replies |

The reservation is **directional**. On R3→R4, the TED showed **5 Mbps allocated / 5 Mbps free** during the 5 Mbps test.

```cisco
show mpls traffic-eng tunnels
show mpls traffic-eng topology
show ip rsvp reservation
show ip route 4.4.4.4
show ip cef 4.4.4.4 detail
```

## What I learned

**RSVP-TE can choose a longer explicit path while IS-IS still prefers the shorter one.** Autoroute determines the head-end's local forwarding resolution. RSVP reserves signaling resources; it does **not** rate-limit packets or guarantee throughput by itself.

**Limit:** I did not test a reverse LSP, QoS, failures or FRR here. All four running/startup configs matched; a pending `0x2142 → 0x2102` config-register correction was not tested after reboot.

**Evidence:** [Complete configs](configs/LAB08-RSVPTE-2026-11-16/) · [CLI and persistence](evidencias/LAB08-RSVPTE-2026-11-16/) · [Next: LAB 09 FRR](LAB09-MPLS-TE-FRR-NNHOP-IOS.md).
