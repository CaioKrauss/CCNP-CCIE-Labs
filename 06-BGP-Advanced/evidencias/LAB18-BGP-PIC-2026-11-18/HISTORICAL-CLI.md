# LAB 18 — Original CLI from the source conversation

Source: https://chatgpt.com/c/6afbb8c6-3b30-83e8-ab14-6be459107b14

These are user-supplied historical console outputs, not the new live collection. The retrieval returned recent turns only and no older cursor; earlier Edge failure-stage CLI was not returned.

## Message 2822c037-94aa-4118-ab33-2b8c834d6903

```text
RP/0/0/CPU0:XR1#show isis fast-reroute 2.2.2.2/32 detail
Wed Nov 18 19:03:53.133 UTC

L2 2.2.2.2/32 [10/115] medium priority
     via 10.0.12.2, GigabitEthernet0/0/0/0, XR2, SRGB Base: 16000, Weight: 0
       FRR backup via 10.0.12.6, GigabitEthernet0/0/0/2, XR2, SRGB Base: 16000, Weight: 0, Metric: 100
       P: No, TM: 100, LC: No, NP: No, D: Yes, SRLG: Yes
     src XR2.00-00, 2.2.2.2, prefix-SID index 2, R:0 N:1 P:0 E:0 V:0 L:0
RP/0/0/CPU0:XR1#show cef ipv4 2.2.2.2/32 detail
Wed Nov 18 19:03:53.183 UTC
2.2.2.2/32, version 13, labeled SR, internal 0x1000001 0x85 (ptr 0xa12dbecc) [3], 0x0 (0xa12c1614), 0xa20 (0xa17c9100)
 Updated Sep 21 14:38:49.033 
 local adjacency 10.0.12.2
 Prefix Len 32, traffic index 0, precedence n/a, priority 15
  gateway array (0xa121e574) reference count 3, flags 0x500068, source lsd (5), 2 backups
                [3 type 4 flags 0x8401 (0xa1541578) ext 0x0 (0x0)]
  LW-LDI[type=1, refc=1, ptr=0xa12c1614, sh-ldi=0xa1541578]
  gateway array update type-time 1 Sep 21 14:38:49.033
 LDI Update time Nov 18 18:52:53.249
 LW-LDI-TS Nov 18 18:52:53.249
   via 10.0.12.2/32, GigabitEthernet0/0/0/0, 10 dependencies, weight 0, class 0, protected [flags 0x400]
    path-idx 0 bkup-idx 1 NHID 0x0 [0xa171d0e4 0xa171d1fc]
    next hop 10.0.12.2/32
     local label 24007      labels imposed {ImplNull}
   via 10.0.12.6/32, GigabitEthernet0/0/0/2, 10 dependencies, weight 0, class 0, backup (Local-LFA) [flags 0x300]
    path-idx 1 NHID 0x0 [0xa1611504 0xa1611560]
    next hop 10.0.12.6/32
    local adjacency
     local label 24007      labels imposed {ImplNull}


    Load distribution: 0 (refcount 3)

    Hash  OK  Interface                 Address
    0     Y   GigabitEthernet0/0/0/0    10.0.12.2      
RP/0/0/CPU0:XR1#show isis interface GigabitEthernet0/0/0/0
Wed Nov 18 19:03:54.172 UTC

GigabitEthernet0/0/0/0      Enabled
  Adjacency Formation:      Enabled
  Prefix Advertisement:     Enabled
  IPv4 BFD:                 Disabled
  IPv6 BFD:                 Disabled
  BFD Min Interval:         150
  BFD Multiplier:           3
  RSI SRLG:                 Registered
  Bandwidth:                1000000
  
  Circuit Type:             level-2-only (Interface circuit type is level-1-2)
  Media Type:               P2P
  Circuit Number:           0
  Extended Circuit Number:  2
  Next P2P IIH in:          5 s
  LSP Rexmit Queue Size:    0
  
  Level-2                   
    Adjacency Count:        1
    LSP Pacing Interval:    33 ms
    PSNP Entry Queue Size:  0
    Hello Interval:         10 s
    Hello Multiplier:       3
  
  CLNS I/O
    Protocol State:         Up
    MTU:                    1497
    SNPA:                   5000.0009.0001
    Layer-2 MCast Groups Membership:
      All ISs:              Yes
  
  IPv4 Unicast Topology:    Enabled
    Adjacency Formation:    Running
    Prefix Advertisement:   Running
    Metric (L1/L2):         10/10
    Weight (L1/L2):         0/0
    MPLS Max Label Stack(PRI/BKP/SRTE):1/3/10
    MPLS LDP Sync (L1/L2):  Disabled/Disabled
    FRR (L1/L2):            L1 Enabled         L2 Enabled     
      FRR Type:             per-prefix         per-prefix     
      Direct LFA:           Enabled            Enabled        
      Remoter LFA:          Not Enabled        Not Enabled    
       Tie Breaker          Default            Default        
       Line-card disjoint   30                 30             
       Lowest backup metric 20                 20             
       Node protecting      40                 40             
       Primary path         10                 10             
      TI LFA:               Enabled            Enabled        
       Tie Breaker          Default            Default        
       Link Protecting      Enabled            Enabled        
       Node protecting      0                  0              
       SRLG disjoint        0                  0              
  
  IPv4 Address Family:      Enabled
    Protocol State:         Up
    Forwarding Address(es): 10.0.12.1
    Global Prefix(es):      10.0.12.0/30
  
  LSP transmit timer expires in 0 ms
  LSP transmission is idle
  Can send up to 9 back-to-back LSPs in the next 0 ms
  
RP/0/0/CPU0:XR1#
RP/0/0/CPU0:XR1#
```

## Message 0e228f04-1673-4697-b461-443283ba5c86

```text
RP/0/0/CPU0:XR1#show isis adjacency
Wed Nov 18 19:06:01.114 UTC

IS-IS CORE Level-2 adjacencies:
System Id      Interface        SNPA           State Hold Changed  NSF IPv4 IPv6
                                                                       BFD  BFD 
XR2            Gi0/0/0/2        *PtoP*         Up    29   00:16:27 Yes None None
R1             Gi0/0/0/1        *PtoP*         Up    23   00:16:18 Yes None None

Total adjacency count: 2
RP/0/0/CPU0:XR1#show cef ipv4 2.2.2.2/32 detail
Wed Nov 18 19:06:01.164 UTC
2.2.2.2/32, version 26, labeled SR, internal 0x1000001 0x85 (ptr 0xa12dbecc) [3], 0x0 (0xa12c1614), 0xa20 (0xa1527320)
 Updated Sep 21 14:38:49.032 
 local adjacency 10.0.12.6
 Prefix Len 32, traffic index 0, precedence n/a, priority 15
  gateway array (0xa121ea9c) reference count 3, flags 0x68, source lsd (5), 2 backups
                [3 type 4 flags 0x8401 (0xa1541938) ext 0x0 (0x0)]
  LW-LDI[type=1, refc=1, ptr=0xa12c1614, sh-ldi=0xa1541938]
  gateway array update type-time 1 Sep 21 14:38:49.032
 LDI Update time Nov 18 19:05:48.734
 LW-LDI-TS Nov 18 19:05:48.734
   via 10.0.12.6/32, GigabitEthernet0/0/0/2, 14 dependencies, weight 0, class 0 [flags 0x0]
    path-idx 0 NHID 0x0 [0xa1611504 0xa1611560]
    next hop 10.0.12.6/32
    local adjacency
     local label 24007      labels imposed {ImplNull}


    Load distribution: 0 (refcount 3)

    Hash  OK  Interface                 Address
    0     Y   GigabitEthernet0/0/0/2    10.0.12.6      
RP/0/0/CPU0:XR1#show bgp ipv4 unicast 198.51.100.0/24
Wed Nov 18 19:06:01.224 UTC
BGP routing table entry for 198.51.100.0/24
Versions:
  Process           bRIB/RIB  SendTblVer
  Speaker                 10          10
Last Modified: Nov 18 19:02:37.256 for 00:03:23
Paths: (2 available, best #2)
  Advertised to peers (in unique update groups):
    2.2.2.2         
  Path #1: Received by speaker 0
  Not advertised to any peer
  65102
    2.2.2.2 (metric 100) from 2.2.2.2 (2.2.2.2)
      Origin IGP, metric 0, localpref 200, valid, internal, backup, add-path
      Received Path ID 0, Local Path ID 1, version 10
  Path #2: Received by speaker 0
  Advertised to peers (in unique update groups):
    2.2.2.2         
  65101
    10.0.13.1 from 10.0.13.1 (3.3.3.3)
      Origin IGP, metric 0, localpref 200, valid, external, best, group-best
      Received Path ID 0, Local Path ID 0, version 10
      Community: 65101:200
      Origin-AS validity: not-found
RP/0/0/CPU0:XR1#show route 198.51.100.0/24
Wed Nov 18 19:06:01.284 UTC

Routing entry for 198.51.100.0/24
  Known via "bgp 65000", distance 20, metric 0
  Tag 65101
  Number of pic paths 1 , type internal and external
  Installed Nov 18 19:02:36.888 for 00:03:24
  Routing Descriptor Blocks
    2.2.2.2, from 2.2.2.2, BGP backup path
      Route metric is 0
    10.0.13.1, from 10.0.13.1, BGP external
      Route metric is 0
  No advertising protos. 
RP/0/0/CPU0:XR1#show cef ipv4 198.51.100.0/24 detail
Wed Nov 18 19:06:02.304 UTC
198.51.100.0/24, version 48, internal 0x5000001 0x0 (ptr 0xa12dc0ec) [1], 0x0 (0x0), 0x0 (0x0)
 Updated Nov 18 19:02:36.909 
 local adjacency 10.0.13.1
 Prefix Len 24, traffic index 0, precedence n/a, priority 4
  gateway array (0xa121e910) reference count 1, flags 0x102810, source rib (7), 0 backups
                [1 type 3 flags 0x40501 (0xa12736a4) ext 0x0 (0x0)]
  LW-LDI[type=0, refc=0, ptr=0x0, sh-ldi=0x0]
  gateway array update type-time 1 Nov 18 19:02:36.909
 LDI Update time Nov 18 19:05:48.735
   via 2.2.2.2/32, 3 dependencies, recursive, backup [flags 0x6100]
    path-idx 0 NHID 0x0 [0xa12dbecc 0x0]
    next hop 2.2.2.2/32 via 2.2.2.2/32
   via 10.0.13.1/32, 2 dependencies, recursive, bgp-ext [flags 0x6020]
    path-idx 1 NHID 0x0 [0xa12dbcac 0x0]
    next hop 10.0.13.1/32 via 10.0.13.1/32


    Load distribution: 0 (refcount 1)

    Hash  OK  Interface                 Address
    0     Y   GigabitEthernet0/0/0/1    10.0.13.1      
RP/0/0/CPU0:XR1#
```

## Message 5967e087-b628-498b-8165-fe3f540747d0

```text
RP/0/0/CPU0:XR1#show bgp ipv4 unicast 198.51.100.0/24
Wed Nov 18 19:07:51.946 UTC
BGP routing table entry for 198.51.100.0/24
Versions:
  Process           bRIB/RIB  SendTblVer
  Speaker                 11          11
Last Modified: Nov 18 19:07:33.256 for 00:00:18
Paths: (2 available, best #1)
  Advertised to peers (in unique update groups):
    10.0.13.1       
  Path #1: Received by speaker 0
  Advertised to peers (in unique update groups):
    10.0.13.1       
  65102
    2.2.2.2 (metric 10) from 2.2.2.2 (2.2.2.2)
      Origin IGP, metric 0, localpref 200, valid, internal, best, group-best
      Received Path ID 0, Local Path ID 0, version 11
  Path #2: Received by speaker 0
  Not advertised to any peer
  65101
    10.0.13.1 from 10.0.13.1 (3.3.3.3)
      Origin IGP, metric 0, localpref 100, valid, external, backup, add-path
      Received Path ID 0, Local Path ID 1, version 11
      Community: 65101:200
      Origin-AS validity: not-found
RP/0/0/CPU0:XR1#show cef ipv4 198.51.100.0/24 detail
Wed Nov 18 19:07:51.996 UTC
198.51.100.0/24, version 87, internal 0x5000001 0x0 (ptr 0xa12dc0ec) [1], 0x0 (0x0), 0x0 (0x0)
 Updated Nov 18 19:07:33.677 
 local adjacency 10.0.12.2
 Prefix Len 24, traffic index 0, precedence n/a, priority 4
  gateway array (0xa121d914) reference count 1, flags 0x102810, source rib (7), 0 backups
                [1 type 3 flags 0x68501 (0xa127362c) ext 0x210 (0xa1527438)]
  LW-LDI[type=0, refc=0, ptr=0x0, sh-ldi=0x0]
  gateway array update type-time 1 Nov 18 19:07:33.677
 LDI Update time Nov 18 19:07:33.677
   via 2.2.2.2/32, 3 dependencies, recursive [flags 0x6000]
    path-idx 0 NHID 0x0 [0xa12dbecc 0x0]
    next hop 2.2.2.2/32 via 2.2.2.2/32
   via 10.0.13.1/32, 2 dependencies, recursive, bgp-ext, backup [flags 0x6120]
    path-idx 1 NHID 0x0 [0xa12dbcac 0x0]
    next hop 10.0.13.1/32 via 10.0.13.1/32


    Load distribution: 0 (refcount 1)

    Hash  OK  Interface                 Address
    0     Y   GigabitEthernet0/0/0/0    10.0.12.2      
RP/0/0/CPU0:XR1#show cef ipv4 2.2.2.2/32 detail
Wed Nov 18 19:07:52.416 UTC
2.2.2.2/32, version 59, labeled SR, internal 0x1000001 0x85 (ptr 0xa12dbecc) [3], 0x0 (0xa12c1614), 0xa20 (0xa17c912c)
 Updated Sep 21 14:38:49.032 
 local adjacency 10.0.12.2
 Prefix Len 32, traffic index 0, precedence n/a, priority 15
  gateway array (0xa121ee38) reference count 3, flags 0x500068, source lsd (5), 2 backups
                [3 type 4 flags 0x8401 (0xa1541bcc) ext 0x0 (0x0)]
  LW-LDI[type=1, refc=1, ptr=0xa12c1614, sh-ldi=0xa1541bcc]
  gateway array update type-time 1 Sep 21 14:38:49.032
 LDI Update time Nov 18 19:06:21.262
 LW-LDI-TS Nov 18 19:06:21.262
   via 10.0.12.2/32, GigabitEthernet0/0/0/0, 10 dependencies, weight 0, class 0, protected [flags 0x400]
    path-idx 0 bkup-idx 1 NHID 0x0 [0xa171d42c 0xa171d314]
    next hop 10.0.12.2/32
     local label 24007      labels imposed {ImplNull}
   via 10.0.12.6/32, GigabitEthernet0/0/0/2, 10 dependencies, weight 0, class 0, backup (Local-LFA) [flags 0x300]
    path-idx 1 NHID 0x0 [0xa1611504 0xa1611560]
    next hop 10.0.12.6/32
    local adjacency
     local label 24007      labels imposed {ImplNull}


    Load distribution: 0 (refcount 3)

    Hash  OK  Interface                 Address
    0     Y   GigabitEthernet0/0/0/0    10.0.12.2      
RP/0/0/CPU0:XR1#
```

## Message 66aa200d-2b53-44dc-9ef2-0dfcee8a3ae9

```text
RP/0/0/CPU0:XR1#show bgp summary
Wed Nov 18 19:08:34.153 UTC
BGP router identifier 1.1.1.1, local AS number 65000
BGP generic scan interval 60 secs
Non-stop routing is enabled
BGP table state: Active
Table ID: 0xe0000000   RD version: 11
BGP main routing table version 11
BGP NSR Initial initsync version 2 (Reached)
BGP NSR/ISSU Sync-Group versions 0/0
BGP scan interval 60 secs

BGP is operating in STANDALONE mode.


Process       RcvTblVer   bRIB/RIB   LabelVer  ImportVer  SendTblVer  StandbyVer
Speaker              11         11         11         11          11           0

Neighbor        Spk    AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down  St/PfxRcd
2.2.2.2           0 65000      25      28       11    0    0 00:18:49          2
10.0.13.1         0 65101      28      32       11    0    0 00:05:57          1

RP/0/0/CPU0:XR1#show bgp ipv4 unicast 198.51.100.0/24
Wed Nov 18 19:08:34.213 UTC
BGP routing table entry for 198.51.100.0/24
Versions:
  Process           bRIB/RIB  SendTblVer
  Speaker                 11          11
Last Modified: Nov 18 19:07:33.256 for 00:01:00
Paths: (2 available, best #1)
  Advertised to peers (in unique update groups):
    10.0.13.1       
  Path #1: Received by speaker 0
  Advertised to peers (in unique update groups):
    10.0.13.1       
  65102
    2.2.2.2 (metric 10) from 2.2.2.2 (2.2.2.2)
      Origin IGP, metric 0, localpref 200, valid, internal, best, group-best
      Received Path ID 0, Local Path ID 0, version 11
  Path #2: Received by speaker 0
  Not advertised to any peer
  65101
    10.0.13.1 from 10.0.13.1 (3.3.3.3)
      Origin IGP, metric 0, localpref 100, valid, external, backup, add-path
      Received Path ID 0, Local Path ID 1, version 11
      Community: 65101:200
      Origin-AS validity: not-found
RP/0/0/CPU0:XR1#show cef ipv4 2.2.2.2/32 detail
Wed Nov 18 19:08:34.263 UTC
2.2.2.2/32, version 62, labeled SR, internal 0x1000001 0x85 (ptr 0xa12dbecc) [3], 0x0 (0xa12c1614), 0xa20 (0xa15274b0)
 Updated Sep 21 14:38:49.032 
 local adjacency 10.0.12.6
 Prefix Len 32, traffic index 0, precedence n/a, priority 15
  gateway array (0xa121e04c) reference count 3, flags 0x68, source lsd (5), 2 backups
                [3 type 4 flags 0x8401 (0xa154135c) ext 0x0 (0x0)]
  LW-LDI[type=1, refc=1, ptr=0xa12c1614, sh-ldi=0xa154135c]
  gateway array update type-time 1 Sep 21 14:38:49.032
 LDI Update time Nov 18 19:08:26.854
 LW-LDI-TS Nov 18 19:08:26.854
   via 10.0.12.6/32, GigabitEthernet0/0/0/2, 15 dependencies, weight 0, class 0 [flags 0x0]
    path-idx 0 NHID 0x0 [0xa1611504 0xa1611560]
    next hop 10.0.12.6/32
    local adjacency
     local label 24007      labels imposed {ImplNull}


    Load distribution: 0 (refcount 3)

    Hash  OK  Interface                 Address
    0     Y   GigabitEthernet0/0/0/2    10.0.12.6      
RP/0/0/CPU0:XR1#show cef ipv4 198.51.100.0/24 detail
Wed Nov 18 19:08:34.863 UTC
198.51.100.0/24, version 87, internal 0x5000001 0x0 (ptr 0xa12dc0ec) [1], 0x0 (0x0), 0x0 (0x0)
 Updated Nov 18 19:07:33.677 
 local adjacency 10.0.12.6
 Prefix Len 24, traffic index 0, precedence n/a, priority 4
  gateway array (0xa121d914) reference count 1, flags 0x102810, source rib (7), 0 backups
                [1 type 3 flags 0x60501 (0xa127362c) ext 0x210 (0xa1527410)]
  LW-LDI[type=0, refc=0, ptr=0x0, sh-ldi=0x0]
  gateway array update type-time 1 Nov 18 19:07:33.677
 LDI Update time Nov 18 19:08:26.854
   via 2.2.2.2/32, 3 dependencies, recursive [flags 0x6000]
    path-idx 0 NHID 0x0 [0xa12dbecc 0x0]
    next hop 2.2.2.2/32 via 2.2.2.2/32
   via 10.0.13.1/32, 2 dependencies, recursive, bgp-ext, backup [flags 0x6120]
    path-idx 1 NHID 0x0 [0xa12dbcac 0x0]
    next hop 10.0.13.1/32 via 10.0.13.1/32


    Load distribution: 0 (refcount 1)

    Hash  OK  Interface                 Address
    0     Y   GigabitEthernet0/0/0/2    10.0.12.6      
RP/0/0/CPU0:XR1#
```
