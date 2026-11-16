# LAB 09 — MPLS Traffic Engineering Fast Reroute (FRR), NNHOP Node Protection

**Executed:** 2026-11-16 (Brazil). **Environment:** four Cisco 7200 routers, Cisco IOS 15.2(4)S7, EVE-NG. **Status:** FRR backup association and activation directly observed; backup forwarding, restoration and final Ready state verified. Recovery time was **not measured**.

## Objective

Build an RSVP-TE primary LSP over R1 → R3 → R4 and protect its first hop/node R3 with a distinct backup LSP over R1 → R2 → R4. Capture the transition from FRR **Ready** to **Active**, verify packets can reach R4 on the backup, then restore the primary and see **Ready** and **Active: 0**. This is the separate follow-up to [LAB 08 — RSVP-TE and Autoroute](LAB08-MPLS-RSVP-TE-ISIS-AUTOROUTE.md).

## Topology and addressing

```text
                        R2 (2.2.2.2)
                    10.0.12.2 / 10.0.24.1
                       /           \
              metric 10             metric 10
                     /               \
  R1 (1.1.1.1)                           R4 (4.4.4.4)
                     \               /
              metric 30             metric 10
                       \           /
                    10.0.13.2 / 10.0.34.1
                        R3 (3.3.3.3)

Primary Tunnel100: R1 -> R3 -> R4 (strict path, weight 40)
Backup  Tunnel200: R1 -> R2 -> R4 (strict path, weight 20)
```

| Link | Endpoint A | Endpoint B | IGP/TE metric |
|---|---|---|---|
| R1–R2 | R1 Fa0/0 10.0.12.1/30 | R2 Fa0/0 10.0.12.2/30 | 10 |
| R2–R4 | R2 Fa1/0 10.0.24.1/30 | R4 Fa0/0 10.0.24.2/30 | 10 |
| R1–R3 | R1 Fa1/0 10.0.13.1/30 | R3 Fa0/0 10.0.13.2/30 | 30 |
| R3–R4 | R3 Fa1/0 10.0.34.1/30 | R4 Fa1/0 10.0.34.2/30 | 10 |

Router Loopback0 addresses are `1.1.1.1/32` through `4.4.4.4/32`. IS-IS `CORE` is L2-only with wide metrics and TE extensions. LDP is enabled as in LAB 08. Every core physical link enables MPLS, RSVP and MPLS TE; the configured RSVP interface reservable bandwidth is `10000 10000` kbps.

## Configuration that matters

**On R1 (PLR / head-end):**

```cisco
ip explicit-path name VIA_R3 enable
 next-address 10.0.13.2
 next-address 10.0.34.2
!
ip explicit-path name VIA_R2_BACKUP enable
 next-address 10.0.12.2
 next-address 10.0.24.2
!
interface Tunnel100
 description PRIMARY-RSVP-TE-VIA-R3
 ip unnumbered Loopback0
 tunnel mode mpls traffic-eng
 tunnel destination 4.4.4.4
 tunnel mpls traffic-eng autoroute announce
 tunnel mpls traffic-eng priority 7 7
 tunnel mpls traffic-eng bandwidth 1000
 tunnel mpls traffic-eng path-option 1 explicit name VIA_R3
 tunnel mpls traffic-eng fast-reroute
!
interface Tunnel200
 description FRR-BACKUP-VIA-R2
 ip unnumbered Loopback0
 tunnel mode mpls traffic-eng
 tunnel destination 4.4.4.4
 tunnel mpls traffic-eng priority 7 7
 tunnel mpls traffic-eng bandwidth 1000
 tunnel mpls traffic-eng path-option 1 explicit name VIA_R2_BACKUP
!
interface FastEthernet1/0
 description LINK-TO-R3-PRIMARY
 mpls ip
 mpls traffic-eng tunnels
 mpls traffic-eng backup-path Tunnel200
 ip rsvp bandwidth 10000 10000
```

The above is a **focused excerpt**, not a complete paste-ready config. Refer to the four complete running/startup snapshots in [`configs/LAB09-FRR-2026-11-16/`](configs/LAB09-FRR-2026-11-16/).

### Why does the backup work, despite its lower path weight?

1. `tunnel mpls traffic-eng fast-reroute` makes the **Tunnel100** LSP request local protection.
2. `mpls traffic-eng backup-path Tunnel200` on **R1 Fa1/0** designates the Tunnel200 bypass as a backup for eligible LSPs leaving that interface.
3. Tunnel200 is established with an explicit RSVP path **via R2**, and intentionally does **not** have `autoroute announce`. This keeps regular IP forwarding on Tunnel100 while making Tunnel200 available to the local repair mechanism.
4. RSVP-TE shows path weight **40** for Tunnel100 (30+10) and **20** for Tunnel200 (10+10); neither weight by itself elects which is the primary versus backup. Roles come from the explicit path, Autoroute, FRR request and backup association.

The IOS device reported `Type: N-Nhop` in `show ip rsvp fast-reroute`, consistent with a node-protection bypass around R3. Here the Point of Local Repair (PLR) is the **head-end R1**, and the bypass merges at **R4**.

## Results and evidence timeline

### 1 — Baseline: primary LSP and backup ready

- IS-IS L2 adjacency UP from R1 to R2 (`Fa0/0`) and R3 (`Fa1/0`); both LDP peers `Oper`.
- `show mpls traffic-eng tunnels`: Tunnel100 up/signalling connected via Fa1/0 → `10.0.13.2`, out-label **20**. Tunnel200 up/signalling connected via Fa0/0 → `10.0.12.2`, out-label **20** (labels are local and can coincide on different links).
- Tunnel100 **AutoRoute enabled**, Tunnel200 **AutoRoute disabled**.
- `show ip route 4.4.4.4`: IS-IS L2 metric **20** but route via **Tunnel100**. `show ip cef 4.4.4.4 detail`: `nexthop 4.4.4.4 Tunnel100`.
- FRR database: `Tunnel100 ... Fa1/0:20 ... Tu200:implicit-n ... ready`. RSVP FRR: `Ready`, `N-Nhop`. Tunnel200: `Protected LSPs/Sub-LSPs: 1, Active: 0`.
- Pre-failure sourced ping R1 → R4: **10/10**, RTT min/avg/max **52/58/72 ms**.

### 2 — Remote end and locally detected link failures were not identical

An early long ping was interrupted during failure testing: the pasted output records **122/154 replies (79%)**, with an LDP peer-down message for R3. In the contemporaneous post-test `show`, FRR was still **Ready** and Tunnel200 `Active: 0` — therefore this early sequence **does not prove that FRR switched traffic**. It demonstrates how peer-protocol failure/route convergence and data-plane protection can differ, particularly in a virtual emulator.

The later test explicitly shut **R1 FastEthernet1/0** (the locally protected egress). The R1 console reported the interface administratively down. Immediately afterward the verification showed:

```text
P2P Headend FRR information:
Tunnel100  Tun hd  Fa1/0:20  Tu200:implicit-n  active

P2P LSP:
PRIMARY-RSVP-TE-VIA-R3  Fa1/0  1M:G  Tu200:3  Active  any-unl  N-Nhop

Tunnel200 Fast Reroute Backup Provided:
Protected i/fs: Fa1/0
Protected LSPs/Sub-LSPs: 1, Active: 1
```

**This is the direct evidence of FRR activation**. The IP route continued to display `4.4.4.4/32 ... via Tunnel100` while local MPLS repair redirected forwarding to the backup LSP. Seeing the same RIB route after failure is not evidence that FRR did nothing.

### 3 — Backup data plane observed

With the primary interface unavailable, the owner reported:

```text
R1#traceroute 4.4.4.4
  1 10.0.12.2 [MPLS: Label 20 Exp 0] 48 msec 60 msec 60 msec
  2 10.0.24.2 56 msec
R1#ping 4.4.4.4
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 52/57/64 ms
```

The next hops are R2 and R4, not R3, supporting successful delivery through R1 → R2 → R4 during the observed protection state. `Label 20` is local to the R1–R2 outgoing link and does not identify a tunnel by itself.

### 4 — Restore: primary path and FRR Ready again

After restoration the R1 output showed:

```text
Tunnel100: Admin up, Oper up, Path valid, Signalling connected
OutLabel : FastEthernet1/0, 20
Next Hop : 10.0.13.2
Current LSP [ID: 29]: Selection: reoptimization
Prior LSP [ID: 11]: Removal Trigger: re-route path verification failed

Tunnel200: Admin up, Oper up, Signalling connected
OutLabel : FastEthernet0/0, 20
Next Hop : 10.0.12.2
```

The restored traceroute again followed R3:

```text
R1#traceroute 4.4.4.4
  1 10.0.13.2 [MPLS: Label 20 Exp 0] 40 msec 52 msec 56 msec
  2 10.0.34.2 52 msec 64 msec *
```

Final confirmation:

```text
show mpls traffic-eng fast-reroute database:
Tunnel100  Tun hd  Fa1/0:20  Tu200:implicit-n  ready

show mpls traffic-eng tunnels backup:
FRR-BACKUP-VIA-R2
LSP Head, Admin: up, Oper: up
Protected i/fs: Fa1/0
Protected LSPs/Sub-LSPs: 1, Active: 0
```

A `*` for one traceroute probe does not negate the other two successful R4 replies; the final state was established by multiple independent commands.

## Data plane vs routing control plane

The IP RIB/CEF uses **Tunnel100** while its LSP is active. The FRR mechanism can modify the **MPLS forwarding disposition** locally when the protected interface/LSP fails, forwarding over the backup bypass. Consequently, the IP route may keep `via Tunnel100` during repair. The original explicit route and RSVP signaling can later be re-established; the reported LSP instance changed from **11** to **29** on restoration. This is distinct from immediate local repair.

A normal `ping 4.4.4.4` or `traceroute 4.4.4.4` is useful for reachability and path evidence, but is **not** a sub-50-ms convergence benchmark. The earlier partial long ping experienced 32 unanswered probes. No timed packet-capture test or guaranteed hitless switchover was performed.

## Verification commands

On R1:

```cisco
show isis neighbors
show mpls ldp neighbor
show mpls traffic-eng tunnels
show mpls traffic-eng fast-reroute database
show ip rsvp fast-reroute
show mpls traffic-eng tunnels backup
show ip route 4.4.4.4
show ip cef 4.4.4.4 detail
traceroute 4.4.4.4
ping 4.4.4.4 source 1.1.1.1 repeat 10
```

The documented failure was performed only in the isolated EVE-NG lab. Shut/re-enable the protected link **only** in a controlled environment and preserve a separate console path.

## Collected files and limits

- [Complete running/startup configs R1–R4](configs/LAB09-FRR-2026-11-16/)
- [FRR CLI extracts and collection manifests](evidencias/LAB09-FRR-2026-11-16/)
- [Collection/persistence details](evidencias/LAB09-FRR-2026-11-16/COLLECTION-AND-PERSISTENCE.md)
- [Observed CLI excerpts](evidencias/LAB09-FRR-2026-11-16/FRR-CLI-OBSERVED.md)

The four collected running-configs matched their startup-configs on 2026-11-16. However `show version` still reported `Configuration register is 0x2142 (will be 0x2102 at next reload)` on every router. The target register has not been validated after reboot. Collected configuration snapshots are proof of configuration, not independently proof of packet delivery; the packet and FRR tests are separately evidenced in the shared CLI.

**Not tested:** FRR switchover latency, guaranteed sub-50 ms, bandwidth admission behavior with multiple backups, node failures other than the observed link shutdowns, MPLS TE preemption, restoration hysteresis, BFD and throughput/QoS. The distinct LAB 08 demonstrated bandwidth variation; this LAB 09 focuses on local RSVP-TE FRR.
