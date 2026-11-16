# LAB 10 — CLI observations supplied by the lab owner

**Provenance:** selected verbatim excerpts from R1/R3 console outputs posted by the lab owner during the interactive LAB 10 session on 2026-11-16. They were **not present in the final collector ZIP**. Omitted lines are not implied to have been recaptured. Keep observed operational state separate from the final configuration snapshots.

## Stage 1 — CSPF dynamic picks the lower metric (R1 via R2)

```text
R1#show mpls traffic-eng tunnels
Name: CSPF-DYNAMIC-R1-TO-R4 (Tunnel100) Destination: 4.4.4.4
Admin: up         Oper: up     Path: valid       Signalling: connected
path option 1, type dynamic (Basis for Setup, path weight 20)
Bandwidth: 1000 kbps (Global)  Priority: 7 7   Affinity: 0x0/0xFFFF
AutoRoute: enabled
OutLabel : FastEthernet0/0, 16
Next Hop : 10.0.12.2
Explicit Route: 10.0.12.2 10.0.24.2 4.4.4.4
R1#show ip route 4.4.4.4
Known via "isis", distance 115, metric 20, type level-2
* 4.4.4.4, from 4.4.4.4, via Tunnel100
R1#traceroute 4.4.4.4
1 10.0.12.2 [MPLS: Label 16 Exp 0] 44 msec 32 msec 56 msec
2 10.0.24.2 60 msec 36 msec *
```

## Stage 2 — Insufficient RSVP reservable bandwidth via R2

The owner reduced `ip rsvp bandwidth` on **R1 Fa0/0** from **10000/10000** to **500/500** kbps, and reoptimized the tunnel. The TED showed the R1→R2 link's reservable bandwidth was 500 kbps, less than Tunnel100's 1000 kbps reservation request.

```text
R1#show mpls traffic-eng tunnels
Name: CSPF-DYNAMIC-R1-TO-R4 (Tunnel100) Destination: 4.4.4.4
Admin: up         Oper: up     Path: valid       Signalling: connected
path option 1, type dynamic (Basis for Setup, path weight 40)
Bandwidth: 1000 kbps (Global) Priority: 7 7
OutLabel : FastEthernet1/0, 21
Next Hop : 10.0.13.2
Explicit Route: 10.0.13.2 10.0.34.2 4.4.4.4
R1#traceroute 4.4.4.4
1 10.0.13.2 [MPLS: Label 21 Exp 0] 60 msec 36 msec 52 msec
2 10.0.34.2 60 msec 40 msec *
```

After restoration of 10000/10000 and reoptimization, owner output again reported **weight 20**, **Fa0/0→10.0.12.2**, and **LSP ID 18**, with previous LSP 15 removed because `reoptimization completed`.

## Stage 3 — Affinity forces R1 via R3

Owner assigned `mpls traffic-eng attribute-flags 0x1` on **R1 Fa1/0**, **R3 Fa0/0 & Fa1/0**, **R4 Fa1/0**, and `tunnel mpls traffic-eng affinity 0x1 mask 0x1` to **R1 Tunnel100**.

```text
R1#show mpls traffic-eng tunnels
Name: CSPF-DYNAMIC-R1-TO-R4 (Tunnel100) Destination: 4.4.4.4
Admin: up         Oper: up     Path: valid       Signalling: connected
path option 1, type dynamic (Basis for Setup, path weight 40)
Bandwidth: 1000 kbps (Global) Priority: 7 7  Affinity: 0x1/0x1
OutLabel : FastEthernet1/0, 21
Next Hop : 10.0.13.2
Tun_Instance 19
Explicit Route: 10.0.13.2 10.0.34.2 4.4.4.4
Prior LSP: [ID: 18]  Removal Trigger: configuration changed
```

## Stage 4 — Low-priority reservation on R3→R4

R1 Tunnel100 bandwidth increased to 8000 kbps, priority remained 7/7, affinity 0x1/0x1.

```text
R1#show mpls traffic-eng tunnels
Name: CSPF-DYNAMIC-R1-TO-R4 (Tunnel100)
Admin: up         Oper: up     Path: valid       Signalling: connected
Bandwidth: 8000 kbps (Global) Priority: 7 7 Affinity: 0x1/0x1
path option 1, type dynamic (Basis for Setup, path weight 40)
OutLabel : FastEthernet1/0, 22
Next Hop : 10.0.13.2
Tun_Instance 21
R3#show mpls traffic-eng topology
Intf Address: 10.0.34.1, Nbr Intf Address: 10.0.34.2
bw[0]: 0 10000
bw[7]: 8000 2000
```

Note: the TED priority-indexed `Reservable` column is a function of priority/preemptibility; it is not physical line bandwidth. The directional reservation on R3→R4 is 8 Mbps, leaving 2 Mbps non-reserved for the priority-7 tunnel class.

## Stage 5 — High-priority setup and RSVP-TE preemption

R3 Tunnel200 at priority 0/0, 5000 kbps initially had `Affinity: 0x0/0xFFFF` and remained `Oper: down / Path: not valid` because R3→R4 carried flags 0x1. Owner corrected Tunnel200 to `affinity 0x1 mask 0x1` and it established via **R3 Fa1/0 → 10.0.34.2**.

```text
R3#show mpls traffic-eng tunnels
Name: HIGH-PRIORITY-PREEMPTION-TO-R4 (Tunnel200) Destination: 4.4.4.4
Admin: up         Oper: up     Path: valid       Signalling: connected
path option 1, type dynamic (Basis for Setup, path weight 10)
Bandwidth: 5000 kbps (Global) Priority: 0 0 Affinity: 0x1/0x1
OutLabel : FastEthernet1/0, implicit-null
Next Hop : 10.0.34.2
Tun_Instance 5
R3#show ip rsvp reservation
4.4.4.4 3.3.3.3 0 200 5 10.0.34.2 Fa1/0 SE LOAD 5M
R3#show mpls traffic-eng topology
Intf Address: 10.0.34.1, Nbr Intf Address: 10.0.34.2
bw[0]: 5000 5000
bw[7]: 0 5000
R1#show mpls traffic-eng tunnels
Name: CSPF-DYNAMIC-R1-TO-R4 (Tunnel100) Destination: 4.4.4.4
Admin: up         Oper: down   Path: not valid   Signalling: Down
Bandwidth: 8000 kbps (Global) Priority: 7 7 Affinity: 0x1/0x1
Last Error: CTRL:: No path to destination, 0000.0004.0004.00
R1#show ip rsvp reservation
To From Pro DPort Sport Next Hop I/F Fi Serv BPS
```

When the owner re-enabled R3 Tunnel200 after an earlier shutdown, R3 logged the decisive proof of *preemption* (this is from the owner-posted syslog, not from the final collector ZIP):

```text
*Nov 16 05:41:43.259: %MPLS_TE-5-LSP: LSP 1.1.1.1 100_34: DOWN: preempted on Fa1/0  Reason: insufficient resources
*Nov 16 05:41:43.271: %LINEPROTO-5-UPDOWN: Line protocol on Interface Tunnel200, changed state to up
```

## Stage 6 — Resource release and recovery

The owner finally shut down R3 Tunnel200 and verified R1 Tunnel100 recovery:

```text
R1#show mpls traffic-eng tunnels
Name: CSPF-DYNAMIC-R1-TO-R4 (Tunnel100) Destination: 4.4.4.4
Admin: up         Oper: up     Path: valid       Signalling: connected
path option 1, type dynamic (Basis for Setup, path weight 40)
Bandwidth: 8000 kbps (Global) Priority: 7 7 Affinity: 0x1/0x1
OutLabel : FastEthernet1/0, 22
Next Hop : 10.0.13.2
Tun_Instance 44
Explicit Route: 10.0.13.2 10.0.34.2 4.4.4.4
R1#show ip rsvp reservation
4.4.4.4 1.1.1.1 0 100 44 10.0.13.2 Fa1/0 SE LOAD 8M
```

The **final collector running-config on R3 retains `shutdown` under Tunnel200**, exactly matching this stable post-test configuration. The collector did not capture new full traffic probes or a reload. No claim of zero packet loss, throughput, deterministic repair time or observed data-plane preemption is made.
