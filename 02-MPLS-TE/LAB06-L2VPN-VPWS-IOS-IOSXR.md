# LAB 06 — VPWS over MPLS (Ethernet Pseudowire)

**My goal:** connect two CEs on the same Ethernet subnet using an LDP-signaled pseudowire (VC **100**).

## My topology

```text
L2_CE1 (.1/24) -- R2 (PE) -- R3 (P) -- R1 (PE) -- L2_CE2 (.2/24)
                  2.2.2.2    3.3.3.3   1.1.1.1
                 <--------- PW VC 100 --------->
                       192.168.100.0/24
```

The working PEs were **Cisco IOS R2 and R1**, with IS-IS/LDP through R3. XR1 remained in the older L3VPN topology, but I excluded it from the final VPWS.

## What I configured

On R2's CE-facing Ethernet port:

```cisco
interface FastEthernet0/1
 no ip address
 xconnect 1.1.1.1 100 encapsulation mpls
```

On R1:

```cisco
interface FastEthernet1/0
 no ip address
 no keepalive
 xconnect 2.2.2.2 100 encapsulation mpls
```

The core used IS-IS and LDP. **Targeted LDP** signaled the PW between the PEs, which were not directly connected.

## What I observed (2026-11-14)

| Check | My result |
|---|---|
| Underlay | R2–R3 IS-IS L2 UP; LDP peers operational |
| PW on R2 | VC 100 **UP**, Ethernet MTU 1500/1500 |
| MPLS label stack | Transport **17**, service/PW **23** toward R1 |
| CE1 → CE2 | **9/10** after ARP clear |
| CE2 → CE1 | **10/10** |
| ARP / VC counters | Remote MAC resolved; R2 recv 65 / send 77, drops 0 |

I also found an operational **10 Mb/s half-duplex** condition on R2's core interface. I corrected it to 100 Mb/s full-duplex before the final test.

### The XRv attempt that did not forward traffic

Before using R2, I tried XR1 ↔ R1. The PW was **UP**, but CE-to-CE ping was **0/10**. XR1's L2VPN service counters remained at zero even though its physical port received frames.

This **suggested a limitation of the classic XRv virtual dataplane**; I did not prove the cause with a packet capture. I removed the experimental XR1 cross-connect from the final config.

```cisco
show isis neighbors
show mpls ldp neighbor
show mpls l2transport vc detail
show mpls forwarding-table
show ip arp
```

## What I learned

**PW UP means signaling is up, not necessarily that Ethernet frames pass.** I only considered the service validated after ARP resolution, bidirectional ping and VC counter changes.

**Limit:** R1/R2/R3 startup snapshots were verified; CE running configs were collected without startup persistence checks. XRv's cause remains unproven.

**Evidence:** [Device configs](configs/LAB06-VPWS-2026-11-14/) · [CLI observations](evidencias/LAB06-VPWS-2026-11-14/CLI-observed-2026-11-14.txt) · [Persistence notes](evidencias/LAB06-VPWS-2026-11-14/COLLECTION-AND-PERSISTENCE.md).
