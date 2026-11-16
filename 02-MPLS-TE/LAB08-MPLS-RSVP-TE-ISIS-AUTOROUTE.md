# LAB 08 — MPLS Traffic Engineering / RSVP-TE with IS-IS (Cisco 7200)

**Validated:** 16 November 2026 | **Topology:** four Cisco 7200 routers | **IOS:** 15.2(4)S7, Advanced Enterprise Services | **Status:** completed for the stated scope.

## Objective

Show that MPLS RSVP-TE can signal an LSP on an **explicit path** different from the ordinary IS-IS shortest path, inject that tunnel into the **local** route calculation using `autoroute announce`, account for RSVP bandwidth, change the reservation dynamically and restore a known-good baseline.

This is a TE and bandwidth-admission lab, **not** a QoS rate-guarantee test, an RSVP preemption test, a fast-reroute test, or a bidirectional TE setup.

## Physical and logical topology

```text
                    R2 (P) [2.2.2.2]
                   /               \
       10.0.12.0/30               10.0.24.0/30
                 /                   \
 R1 (head-end) [1.1.1.1]          R4 (tail-end) [4.4.4.4]
                 \                   /
       10.0.13.0/30               10.0.34.0/30
                   \               /
                    R3 (P) [3.3.3.3]
```

| Link | Node A | Node B | IS-IS metric on both ends |
|---|---|---|---|
| R1–R2 | R1 Fa0/0 `10.0.12.1/30` | R2 Fa0/0 `10.0.12.2/30` | 10 |
| R2–R4 | R2 Fa1/0 `10.0.24.1/30` | R4 Fa0/0 `10.0.24.2/30` | 10 |
| R1–R3 | R1 Fa1/0 `10.0.13.1/30` | R3 Fa0/0 `10.0.13.2/30` | 30 |
| R3–R4 | R3 Fa1/0 `10.0.34.1/30` | R4 Fa1/0 `10.0.34.2/30` | 10 |

Loopbacks: R1 `1.1.1.1/32`; R2 `2.2.2.2/32`; R3 `3.3.3.3/32`; R4 `4.4.4.4/32`. IS-IS process `CORE` (level 2, wide metric), MPLS/LDP and RSVP are enabled on the backbone. Each link was configured for RSVP reservation limits of `10000` kbps. Physical FastEthernet speed was reported in TED as `100000` kbps.

**Normal IGP path:** R1 → R2 → R4, metric **20**. **Explicit RSVP-TE path:** R1 → R3 → R4, metric **40**. Higher IGP metric does not prevent a specifically requested, feasible RSVP-TE LSP.

## Exact configuration captured from the devices

The following are **actual final running-config excerpts**, not proposed configuration:

### R1: head-end, explicit path and Autoroute

```cisco
mpls traffic-eng tunnels
!
ip explicit-path name VIA_R3 enable
 next-address 10.0.13.2
 next-address 10.0.34.2
!
interface Tunnel100
 description RSVP-TE-R1-TO-R4-VIA-R3
 ip unnumbered Loopback0
 tunnel mode mpls traffic-eng
 tunnel destination 4.4.4.4
 tunnel mpls traffic-eng autoroute announce
 tunnel mpls traffic-eng priority 7 7
 tunnel mpls traffic-eng bandwidth 1000
 tunnel mpls traffic-eng path-option 1 explicit name VIA_R3
!
router isis CORE
 net 49.0001.0000.0001.0001.00
 is-type level-2-only
 metric-style wide
 passive-interface Loopback0
 mpls traffic-eng router-id Loopback0
 mpls traffic-eng level-2
```

Each core-facing interface has `mpls ip`, `mpls traffic-eng tunnels` and `ip rsvp bandwidth 10000 10000`; each PE/P router uses its Loopback0 as the LDP router ID.

- [R1 final running-config](configs/LAB08-RSVPTE-2026-11-16/R1-running.cfg)
- [R2 final running-config](configs/LAB08-RSVPTE-2026-11-16/R2-running.cfg)
- [R3 final running-config](configs/LAB08-RSVPTE-2026-11-16/R3-running.cfg)
- [R4 final running-config](configs/LAB08-RSVPTE-2026-11-16/R4-running.cfg)

## Verification — actual observations

| Layer / feature | Evidence observed | Interpretation |
|---|---|---|
| IS-IS | R1 adjacent to R2 and R3 at L2, both `UP` | IGP adjacency healthy |
| LDP | R1 neighbors R2 and R3 `Oper` | MPLS LDP transport established |
| IGP route before Autoroute | `4.4.4.4/32` via `10.0.12.2` Fa0/0, metric 20 | Normal path goes via R2 |
| RSVP-TE tunnel | R1 Tunnel100 `Admin up / Oper up`, `Signalling connected` | Explicit LSP successfully signalled |
| Explicit ERO | `10.0.13.2 → 10.0.34.2 → 4.4.4.4` | Path deliberately goes via R3 |
| Autoroute on R1 | RIB next hop `4.4.4.4` via `Tunnel100`; CEF `Tunnel100` | Local R1 forwarding installed via TE despite IS-IS metric 20 |
| RSVP at transit | R3 inbound label `20`, outbound `implicit-null` to R4 | Penultimate hop popping on this RSVP LSP |
| RSVP reservation | `1M`, changed to `5M` and restored to `1M` | Dynamic RSVP signalling/admission state updated |
| TED (during 5 Mbps test) | R3 → R4 priority-7 allocated `5000`, reservable `5000` (kbps) | 5 Mbps of 10 Mbps reserved for the chosen direction |
| Final reachability | R1 source `1.1.1.1` ping R4 `4.4.4.4`, `10/10`, 48/54/60 ms | End-to-end IP traffic reached the tail-end |

All quoted test outputs are preserved in [CLI evidence from the lab conversation](evidencias/LAB08-RSVPTE-2026-11-16/CLI-observed-during-lab.md). They are **not** new tests performed by the publisher.

### RSVP bandwidth adjustment and LSP instance changes

| State | Reserved bandwidth | R1 outgoing label | RSVP Tunnel Instance | Status |
|---|---:|---:|---:|---|
| Original | 1,000 kbps | 20 | 13 | UP |
| Increased | 5,000 kbps | 22 | 14 | UP |
| Restored final baseline | 1,000 kbps | 20 | 15 | UP |

The changes of tunnel instance and outgoing label reflect new RSVP signalling state during this lab; the specific label numbers are dynamic and should not be relied upon as permanent values.

### IGP routing vs. RSVP explicit routing

- IS-IS's best path is R1 → R2 → R4 (20), while the selected TE ERO goes R1 → R3 → R4 (40).
- `tunnel mpls traffic-eng autoroute announce` changes the **head-end's local forwarding calculation**. It does not advertise a new IS-IS tunnel link to all routers.
- The R1 route for `4.4.4.4/32` still reports IS-IS distance 115/metric 20, yet the next hop/CEF points to `Tunnel100`. Routing protocol ownership and forwarding adjacency are distinct concepts.
- The explicit path references downstream **neighbor interface addresses**, ensuring strict next hops. A loose hop to a router loopback would let path computation resolve intermediate hops; loose hops were discussed but **not configured or tested**.

### Reservation is directional, not QoS shaping

R3's `show mpls traffic-eng topology` displayed `bw[7]` on **R3 → R4** with 5,000 kbps allocated and 5,000 kbps still reservable. It separately showed zero allocation on R3 → R1: that is the **opposite direction**, not a contradiction of RSVP's 5 Mbps reservation on **R1 → R3 → R4**. RSVP-TE performs admission/resource reservation. It does **not** rate-limit a CE or independently guarantee throughput without appropriate queuing/QoS.

### RSVP label behavior

On R3, the transit LSP had incoming label `20` from R1 and outgoing `implicit-null` toward R4. R3 performs PHP before delivery to R4. The observed labels may change if RSVP re-signals the tunnel.

## Diagnostic commands and expected checks

On R1:

```cisco
show isis neighbors
show ip route 4.4.4.4
show ip cef 4.4.4.4 detail
show mpls ldp neighbor
show mpls traffic-eng topology
show mpls traffic-eng tunnels
show ip rsvp reservation
ping 4.4.4.4 source 1.1.1.1 repeat 10
```

On R3:

```cisco
show ip rsvp reservation
show mpls traffic-eng tunnels
show mpls traffic-eng topology
```

If the TE tunnel is UP but the route does not use it, check whether `AutoRoute: enabled` and the RIB/CEF for the target prefix point to the tunnel. If the TE tunnel stays DOWN, verify IGP TE extensions, RSVP bandwidth, path hop reachability, and available reservable bandwidth. No fault-injection or FRR test was performed in this lab.

## Configuration snapshots, startup state and caveats

- [R1–R4 complete final running/startup configuration files](configs/LAB08-RSVPTE-2026-11-16/)
- [Collection manifest and original show-command transcripts](evidencias/LAB08-RSVPTE-2026-11-16/)
- Collector metadata reports all four running-configs complete and already saved; all four final running-configs **exactly match their saved startup-config snapshots** (ignoring CRLF normalization).
- On each router, `show version` reported `Configuration register is 0x2142 (will be 0x2102 at next reload)`. The correction to `0x2102` was **pending next reload**. No restart was performed or verified as part of this publication.
- Tested: one unidirectional TE LSP, explicit strict path, local Autoroute, RSVP reservation changes, label/PHP observation and reachable tail-end. **Not tested**: a reverse TE LSP, traceroute at the final baseline, QoS enforcement, ECMP, loose-hop configuration, CSPF reoptimization, SRLG/affinity, preemption, FRR or failure recovery.

## Next step

**LAB 09 — RSVP-TE Fast Reroute (FRR)** will use a related backbone but will be documented separately; LAB 08 does **not** claim any FRR protection result.
