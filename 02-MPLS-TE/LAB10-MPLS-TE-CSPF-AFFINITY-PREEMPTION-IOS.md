# LAB 10 — Dynamic CSPF, Affinity and RSVP-TE Preemption

**My goal:** see how RSVP-TE chooses a path using cost, available bandwidth, administrative groups and LSP priority.

## My topology

```text
               R2 (cost 20)
              /            \
R1 1.1.1.1                    R4 4.4.4.4
              \            /
               R3 (cost 40)
```

I used four Cisco 7200 routers with IS-IS Level 2 and 10 Mbps RSVP-reservable bandwidth on the final links.

## What I tested (2026-11-16)

| Step | What I changed | What I observed |
|---|---|---|
| 1. **Dynamic CSPF** | Tunnel100 with `path-option 1 dynamic` | R1 chose **R2**, path weight **20** |
| 2. **Bandwidth** | R1→R2 reservable bandwidth **10 Mbps → 500 kbps** while tunnel needed 1 Mbps | R1 switched to **R3**, weight **40**; reverted when I restored bandwidth |
| 3. **Affinity** | Set `0x1` on R3-path links and tunnel `affinity 0x1 mask 0x1` | R1 selected **R3** by policy, even though its path cost more |
| 4. **Preemption** | R1 Tunnel100: 8 Mbps, priority **7/7**; R3 Tunnel200: 5 Mbps, priority **0/0** | High-priority Tunnel200 preempted Tunnel100 on R3→R4 |
| 5. **Recovery** | Shut R3 Tunnel200 | R1 Tunnel100 came back **UP**, with **8 Mbps** reserved |

Main commands I changed:

```cisco
! R1 Tunnel100:
tunnel mpls traffic-eng path-option 1 dynamic
tunnel mpls traffic-eng affinity 0x1 mask 0x1
! On links used by the R3 path:
mpls traffic-eng attribute-flags 0x1
! R3 Tunnel200 after I corrected its affinity:
tunnel mpls traffic-eng affinity 0x1 mask 0x1
```

R3 generated direct proof of preemption:

```text
%MPLS_TE-5-LSP: LSP 1.1.1.1 100_34: DOWN:
preempted on Fa1/0 Reason: insufficient resources
```

**Priority 0 is highest; 7 is lowest.** I initially had an affinity mismatch on Tunnel200, corrected it and then repeated the preemption to capture the syslog.

## What I learned

- **CSPF:** picks a feasible path, not simply the shortest IGP path.
- **Bandwidth:** RSVP admission uses reservable capacity, not physical link speed.
- **Affinity:** acts as a path constraint; in this test `(link_flags & mask) == (tunnel_affinity & mask)`.
- **Preemption:** a new higher-priority LSP can displace an established lower-priority reservation.

```cisco
show mpls traffic-eng topology
show mpls traffic-eng tunnels
show ip rsvp reservation
show ip route 4.4.4.4
show logging
```

**Final safe state:** I left **R3 Tunnel200 administratively shut**, allowing R1 Tunnel100 to remain UP with 8 Mbps. All four running/startup snapshots matched.

**Limit:** the syslog and RSVP state prove reservation preemption, **not** zero packet loss or measured recovery time. The pending configuration-register change was not tested after reboot.

**Evidence:** [Final configs](configs/LAB10-CSPF-2026-11-16/) · [Full CLI evidence](evidencias/LAB10-CSPF-2026-11-16/CLI-OBSERVATIONS.md) · [Collector manifest](evidencias/LAB10-CSPF-2026-11-16/COLLECTION-MANIFEST.md).
