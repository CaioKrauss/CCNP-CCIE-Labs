# LAB 08 — Observed CLI evidence from the guided session

> Provenance: console output pasted by the lab owner in the conversation during 16 November 2026. These excerpts are **not** part of the 01:21:50–01:21:52 -03:00 RAR capture. The archive independently contains four running/startup configs and their console transcripts. Command output below is verbatim where shown; some long outputs are intentionally excerpted and marked.

## 1. IS-IS and IGP best path — before autoroute

**R1 — `show isis neighbors`:**

```text
Tag CORE:
System Id      Type Interface   IP Address      State Holdtime Circuit Id
R2             L2   Fa0/0       10.0.12.2       UP    24       01
R3             L2   Fa1/0       10.0.13.2       UP    27       01
```

**R1 — `show ip route 4.4.4.4` before autoroute:**

```text
Routing entry for 4.4.4.4/32
  Known via "isis", distance 115, metric 20, type level-2
  Redistributing via isis CORE
  Routing Descriptor Blocks:
  * 10.0.12.2, from 4.4.4.4, via FastEthernet0/0
      Route metric is 20, traffic share count is 1
```

R1 also displayed R2 (`2.2.2.2:0`) and R3 (`3.3.3.3:0`) in `show mpls ldp neighbor`, each with state `Oper`.

## 2. RSVP-TE explicit path established — original 1 Mbps

**R1 — `show mpls traffic-eng tunnels` (selected fields):**

```text
Name: RSVP-TE-R1-TO-R4-VIA-R3             (Tunnel100) Destination: 4.4.4.4
  Status:
    Admin: up         Oper: up     Path: valid       Signalling: connected
    path option 1, type explicit VIA_R3 (Basis for Setup, path weight 40)
  Config Parameters:
    Bandwidth: 1000     kbps (Global)  Priority: 7  7
    AutoRoute: disabled
  OutLabel : FastEthernet1/0, 20
  Next Hop : 10.0.13.2
    RSVP Path Info:
      Explicit Route: 10.0.13.2 10.0.34.2 4.4.4.4
```

## 3. Route installed via Tunnel100 — autoroute enabled

**R1 — `show ip route 4.4.4.4`:**

```text
Routing entry for 4.4.4.4/32
  Known via "isis", distance 115, metric 20, type level-2
  Redistributing via isis CORE
  Last update from 4.4.4.4 on Tunnel100, 00:00:37 ago
  Routing Descriptor Blocks:
  * 4.4.4.4, from 4.4.4.4, 00:00:37 ago, via Tunnel100
      Route metric is 20, traffic share count is 1
```

**R1 — `show ip cef 4.4.4.4 detail`:**

```text
4.4.4.4/32, epoch 0
  local label info: global/20
  nexthop 4.4.4.4 Tunnel100
```

**R1 — `show mpls traffic-eng tunnels` after autoroute:** `Admin: up`, `Oper: up`, `Signalling: connected`, `AutoRoute: enabled`, `OutLabel: FastEthernet1/0, 20`, next hop `10.0.13.2`.

## 4. RSVP transit label/PHP and original 1 Mbps reservation

**R3 — `show mpls traffic-eng tunnels`:**

```text
LSP Tunnel RSVP-TE-R1-TO-R4-VIA-R3 is signalled, connection is up
  InLabel  : FastEthernet0/0, 20
  Prev Hop : 10.0.13.1
  OutLabel : FastEthernet1/0, implicit-null
  Next Hop : 10.0.34.2
  RSVP Signalling Info:
       Src 1.1.1.1, Dst 4.4.4.4, Tun_Id 100, Tun_Instance 13
```

**R1 — `show ip rsvp reservation`:**

```text
To              From            Pro DPort Sport Next Hop        I/F      Fi Serv BPS
4.4.4.4         1.1.1.1         0   100   13    10.0.13.2       Fa1/0    SE LOAD 1M
```

**R3 — `show ip rsvp reservation`:**

```text
To              From            Pro DPort Sport Next Hop        I/F      Fi Serv BPS
4.4.4.4         1.1.1.1         0   100   13    10.0.34.2       Fa1/0    SE LOAD 1M
```

## 5. RSVP bandwidth changed from 1 Mbps to 5 Mbps

**R1 — `show mpls traffic-eng tunnels` (selected fields):**

```text
Name: RSVP-TE-R1-TO-R4-VIA-R3             (Tunnel100) Destination: 4.4.4.4
    Admin: up         Oper: up     Path: valid       Signalling: connected
    path option 1, type explicit VIA_R3 (Basis for Setup, path weight 40)
    Bandwidth: 5000     kbps (Global)  Priority: 7  7
    AutoRoute: enabled
  OutLabel : FastEthernet1/0, 22
  Next Hop : 10.0.13.2
       Src 1.1.1.1, Dst 4.4.4.4, Tun_Id 100, Tun_Instance 14
```

**R1 — `show ip rsvp reservation`:**

```text
To              From            Pro DPort Sport Next Hop        I/F      Fi Serv BPS
4.4.4.4         1.1.1.1         0   100   14    10.0.13.2       Fa1/0    SE LOAD 5M
```

**R3 — `show ip rsvp reservation`:**

```text
To              From            Pro DPort Sport Next Hop        I/F      Fi Serv BPS
4.4.4.4         1.1.1.1         0   100   14    10.0.34.2       Fa1/0    SE LOAD 5M
```

**R3 — `show mpls traffic-eng topology`, directional link R3 → R4:**

```text
      link[1]: Point-to-Point, Nbr IGP Id: 0000.0004.0004.00, nbr_node_id:4, gen:11
      frag_id: 0, Intf Address: 10.0.34.1, Nbr Intf Address: 10.0.34.2
      TE metric: 10, IGP metric: 10
      physical_bw: 100000 (kbps), max_reservable_bw_global: 10000 (kbps)
                             Global Pool       Sub Pool
           Total Allocated   Reservable        Reservable
           BW (kbps)         BW (kbps)         BW (kbps)
           ---------------   -----------       ----------
    bw[7]:         5000             5000                0
```

This is **priority 7 and directional** resource accounting on the R3 → R4 link. The reverse-direction link R3 → R1 had zero allocation in the R3 TED, which does not contradict a forward R1 → R3 reservation. RSVP is control-plane admission/accounting, not packet shaping.

## 6. Final baseline: restored 1 Mbps and traffic delivery

**R1 — `ping 4.4.4.4 source 1.1.1.1 repeat 10`:**

```text
Sending 10, 100-byte ICMP Echos to 4.4.4.4, timeout is 2 seconds:
Packet sent with a source address of 1.1.1.1
!!!!!!!!!!
Success rate is 100 percent (10/10), round-trip min/avg/max = 48/54/60 ms
```

**R1 — `show mpls traffic-eng tunnels` (selected fields):**

```text
Name: RSVP-TE-R1-TO-R4-VIA-R3             (Tunnel100) Destination: 4.4.4.4
    Admin: up         Oper: up     Path: valid       Signalling: connected
    path option 1, type explicit VIA_R3 (Basis for Setup, path weight 40)
    Bandwidth: 1000     kbps (Global)  Priority: 7  7
    AutoRoute: enabled
  OutLabel : FastEthernet1/0, 20
  Next Hop : 10.0.13.2
       Src 1.1.1.1, Dst 4.4.4.4, Tun_Id 100, Tun_Instance 15
```

**R1 — `show ip rsvp reservation`:**

```text
To              From            Pro DPort Sport Next Hop        I/F      Fi Serv BPS
4.4.4.4         1.1.1.1         0   100   15    10.0.13.2       Fa1/0    SE LOAD 1M
```

The 10/10 ICMP success corroborates end-to-end reachability; alongside the R1 CEF/autoroute and tunnel signaling outputs it supports the intended TE forwarding. A final traceroute was **not** provided. No load/capacity benchmark was performed.
