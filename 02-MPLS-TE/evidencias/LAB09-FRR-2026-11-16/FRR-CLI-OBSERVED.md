# LAB 09 — Observed CLI (lab-owner pasted outputs, 2026-11-16)

This document contains **selected faithful excerpts** of CLI output sent in the conversation. These are not new commands run by the publisher, and not derived from the `routers.zip` baseline config collection. Text is shortened for clarity; results and status transitions are preserved verbatim.

## Baseline: R1 IGP/LDP and TE LSP

```text
R1#show isis neighbors
Tag CORE:
System Id      Type Interface   IP Address      State Holdtime Circuit Id
R2             L2   Fa0/0       10.0.12.2       UP    23       00
R3             L2   Fa1/0       10.0.13.2       UP    28       00

R1#show mpls ldp neighbor
Peer LDP Ident: 2.2.2.2:0; Local LDP Ident 1.1.1.1:0
 State: Oper
Peer LDP Ident: 3.3.3.3:0; Local LDP Ident 1.1.1.1:0
 State: Oper
```

```text
R1#show mpls traffic-eng tunnels
Name: PRIMARY-RSVP-TE-VIA-R3 (Tunnel100) Destination: 4.4.4.4
Admin: up         Oper: up     Path: valid       Signalling: connected
path option 1, type explicit VIA_R3 (Basis for Setup, path weight 40)
Bandwidth: 1000 kbps  Priority: 7 7
AutoRoute: enabled
OutLabel : FastEthernet1/0, 20
Next Hop : 10.0.13.2
FRR OutLabel : Tunnel200, implicit-null

Name: FRR-BACKUP-VIA-R2 (Tunnel200) Destination: 4.4.4.4
Admin: up         Oper: up     Path: valid       Signalling: connected
path option 1, type explicit VIA_R2_BACKUP (Basis for Setup, path weight 20)
AutoRoute: disabled
OutLabel : FastEthernet0/0, 20
Next Hop : 10.0.12.2
```

```text
R1#show mpls traffic-eng fast-reroute database
P2P Headend FRR information:
Protected tunnel               In-label Out intf/label   FRR intf/label   Status
Tunnel100                      Tun hd   Fa1/0:20         Tu200:implicit-n ready

R1#show ip rsvp fast-reroute
PRIMARY-RSVP-TE-VIA-R3    Fa1/0   1M:G       Tu200:3       Ready  any-unl N-Nhop

R1#show mpls traffic-eng tunnels backup
FRR-BACKUP-VIA-R2
  LSP Head, Admin: up, Oper: up
  Protected i/fs: Fa1/0
  Protected LSPs/Sub-LSPs: 1, Active: 0
```

```text
R1#show ip route 4.4.4.4
Routing entry for 4.4.4.4/32
  Known via "isis", distance 115, metric 20, type level-2
  * 4.4.4.4, from 4.4.4.4, via Tunnel100

R1#show ip cef 4.4.4.4 detail
4.4.4.4/32, epoch 0
  local label info: global/20
  nexthop 4.4.4.4 Tunnel100

R1#ping 4.4.4.4 source 1.1.1.1 repeat 10
!!!!!!!!!!
Success rate is 100 percent (10/10), round-trip min/avg/max = 52/58/72 ms
```

## First failure attempt: disrupted connectivity, FRR not yet shown Active

```text
R1#ping 4.4.4.4 source 1.1.1.1 repeat 200
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!....
*Nov 16 04:42:48.275: %LDP-5-NBRCHG: LDP Neighbor 3.3.3.3:0 (2) is DOWN (TCP connection closed by peer)..............
..............
Success rate is 79 percent (122/154), round-trip min/avg/max = 8/37/92 ms
```

After this sequence the user-pasted output still showed:

```text
R1#show mpls traffic-eng fast-reroute database
Tunnel100  Tun hd  Fa1/0:20  Tu200:implicit-n  ready

R1#show ip rsvp fast-reroute
PRIMARY-RSVP-TE-VIA-R3  Fa1/0  1M:G  Tu200:3  Ready  any-unl N-Nhop

R1#show mpls traffic-eng tunnels backup
Protected LSPs/Sub-LSPs: 1, Active: 0
```

The ping output ended at **154** responses/probes despite the `repeat 200` command; do not invent results for the unreported remainder. This did not demonstrate an Active FRR transition.

## Local protected-link shutdown: FRR Active

```text
R1(config)#int fa1/0
R1(config-if)#shut
R1(config-if)#end
*Nov 16 04:44:40.347: %LINK-5-CHANGED: Interface FastEthernet1/0, changed state to administratively down
*Nov 16 04:44:41.347: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet1/0, changed state to down
```

```text
R1#show mpls traffic-eng fast-reroute database
P2P Headend FRR information:
Protected tunnel               In-label Out intf/label   FRR intf/label   Status
Tunnel100                      Tun hd   Fa1/0:20         Tu200:implicit-n active

R1#show ip rsvp fast-reroute
PRIMARY-RSVP-TE-VIA-R3    Fa1/0   1M:G       Tu200:3       Active any-unl N-Nhop

R1#show mpls traffic-eng tunnels backup
FRR-BACKUP-VIA-R2
  LSP Head, Admin: up, Oper: up
  Protected i/fs: Fa1/0
  Protected LSPs/Sub-LSPs: 1, Active: 1
```

Even in this Active state, `show ip route 4.4.4.4` retained the `via Tunnel100` line (IS-IS metric 20). The change was to protected LSP forwarding, not necessarily to the IP RIB entry.

## Backup: path R1 → R2 → R4 and ICMP delivery

```text
R1#traceroute 4.4.4.4
Tracing the route to 4.4.4.4
  1 10.0.12.2 [MPLS: Label 20 Exp 0] 48 msec 60 msec 60 msec
  2 10.0.24.2 56 msec

R1#ping 4.4.4.4
Sending 5, 100-byte ICMP Echos to 4.4.4.4, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 52/57/64 ms
```

## Restored: primary R1 → R3 → R4, FRR Ready

```text
R1#show mpls traffic-eng tunnels
Name: PRIMARY-RSVP-TE-VIA-R3 (Tunnel100) Destination: 4.4.4.4
Admin: up         Oper: up     Path: valid       Signalling: connected
OutLabel : FastEthernet1/0, 20
Next Hop : 10.0.13.2
FRR OutLabel : Tunnel200, implicit-null
RSVP Signalling Info:
Src 1.1.1.1, Dst 4.4.4.4, Tun_Id 100, Tun_Instance 29
Current LSP: [ID: 29]
  Selection: reoptimization
Prior LSP: [ID: 11]
  Removal Trigger: re-route path verification failed

Name: FRR-BACKUP-VIA-R2 (Tunnel200) Destination: 4.4.4.4
Admin: up         Oper: up     Path: valid       Signalling: connected
OutLabel : FastEthernet0/0, 20
Next Hop : 10.0.12.2
```

```text
R1#traceroute 4.4.4.4
  1 10.0.13.2 [MPLS: Label 20 Exp 0] 40 msec 52 msec 56 msec
  2 10.0.34.2 52 msec 64 msec *

R1#show mpls traffic-eng fast-reroute database
Tunnel100                      Tun hd   Fa1/0:20         Tu200:implicit-n ready

R1#show mpls traffic-eng tunnels backup
FRR-BACKUP-VIA-R2
  LSP Head, Admin: up, Oper: up
  Protected i/fs: Fa1/0
  Protected LSPs/Sub-LSPs: 1, Active: 0
  Backup BW: any pool unlimited; inuse: 1000 kbps
  Backup flags: 0x0
```

## Limits and provenance

All excerpts above are from user-supplied console output, with some nonessential fields abbreviated. `show running-config` and `show startup-config` are independently preserved as reviewed snapshots in the companion `configs/` directory; the ZIP's collection transcripts are stored separately. There is **no measured FRR convergence time**, no lossless guarantee, and no end-to-end sustained throughput measurement.
