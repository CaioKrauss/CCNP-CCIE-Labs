# Captured CLI evidence

Source: [Próximo lab SR TE](https://chatgpt.com/c/6afbb8c6-3b30-83e8-ab14-6be459107b14) (account access required). User-pasted router outputs, preserved below; these are historical captures, not new tests. Section labels are editorial. Router timestamps are UTC.

## Source message 2dbce5db-1613-47b1-842e-610304347dce

```text
RP/0/0/CPU0:XR1#show bgp ipv4 unicast 198.51.100.0/24
Tue Nov 17 05:16:32.558 UTC
BGP routing table entry for 198.51.100.0/24
Versions:
  Process           bRIB/RIB  SendTblVer
  Speaker                 15          15
Last Modified: Nov 17 05:16:27.290 for 00:00:05
Paths: (2 available, best #1)
  Advertised to peers (in unique update groups):
    10.0.13.1       
  Path #1: Received by speaker 0
  Advertised to peers (in unique update groups):
    10.0.13.1       
  65102
    2.2.2.2 (metric 10) from 2.2.2.2 (2.2.2.2)
      Origin IGP, metric 0, localpref 100, valid, internal, best, group-best
      Received Path ID 0, Local Path ID 0, version 15
  Path #2: Received by speaker 0
  Not advertised to any peer
  65101
    10.0.13.1 from 10.0.13.1 (3.3.3.3)
      Origin IGP, metric 500, localpref 100, valid, external, group-best
      Received Path ID 0, Local Path ID 0, version 0
      Origin-AS validity: not-found
RP/0/0/CPU0:XR1#show route 198.51.100.0/24
Tue Nov 17 05:16:33.668 UTC

Routing entry for 198.51.100.0/24
  Known via "bgp 65000", distance 200, metric 0
  Tag 65102, type internal
  Installed Nov 17 05:16:27.459 for 00:00:06
  Routing Descriptor Blocks
    2.2.2.2, from 2.2.2.2
      Route metric is 0
  No advertising protos. 
RP/0/0/CPU0:XR1#
```

## Source message 1a7292d2-693d-458e-ae3d-b5b5e6dce7e1

```text
RP/0/0/CPU0:XR1#
RP/0/0/CPU0:XR1#show bgp ipv4 unicast 198.51.100.0/24
Tue Nov 17 05:18:35.900 UTC
BGP routing table entry for 198.51.100.0/24
Versions:
  Process           bRIB/RIB  SendTblVer
  Speaker                 17          17
Last Modified: Nov 17 05:18:18.290 for 00:00:17
Paths: (2 available, best #2)
  Advertised to peers (in unique update groups):
    2.2.2.2         
  Path #1: Received by speaker 0
  Not advertised to any peer
  65102
    2.2.2.2 (metric 10) from 2.2.2.2 (2.2.2.2)
      Origin IGP, metric 0, localpref 100, valid, internal, group-best
      Received Path ID 0, Local Path ID 0, version 0
  Path #2: Received by speaker 0
  Advertised to peers (in unique update groups):
    2.2.2.2         
  65101
    10.0.13.1 from 10.0.13.1 (3.3.3.3)
      Origin IGP, metric 0, localpref 100, valid, external, best, group-best
      Received Path ID 0, Local Path ID 0, version 17
      Community: 65101:200
      Origin-AS validity: not-found
RP/0/0/CPU0:XR1#
```

## Source message 960dc032-78fe-4300-97e1-f4e53f7594c7

```text
RP/0/0/CPU0:XR1#show bgp ipv4 unicast 198.51.100.0/24
Tue Nov 17 05:19:57.724 UTC
BGP routing table entry for 198.51.100.0/24
Versions:
  Process           bRIB/RIB  SendTblVer
  Speaker                 18          18
Last Modified: Nov 17 05:19:38.290 for 00:00:19
Paths: (1 available, best #1)
  Advertised to peers (in unique update groups):
    2.2.2.2         
  Path #1: Received by speaker 0
  Advertised to peers (in unique update groups):
    2.2.2.2         
  65101
    10.0.13.1 from 10.0.13.1 (3.3.3.3)
      Origin IGP, metric 0, localpref 200, valid, external, best, group-best
      Received Path ID 0, Local Path ID 0, version 18
      Community: 65101:200
      Origin-AS validity: not-found
RP/0/0/CPU0:XR1#show route 198.51.100.0/24
Tue Nov 17 05:20:06.154 UTC

Routing entry for 198.51.100.0/24
  Known via "bgp 65000", distance 20, metric 0
  Tag 65101, type external
  Installed Nov 17 05:19:38.366 for 00:00:27
  Routing Descriptor Blocks
    10.0.13.1, from 10.0.13.1, BGP external
      Route metric is 0
  No advertising protos. 
RP/0/0/CPU0:XR1#
```

## Source message 5e71051f-7de6-4a4a-a192-8b06ffb50b3b

```text
RP/0/0/CPU0:XR2#show bgp ipv4 unicast 198.51.100.0/24
Tue Nov 17 05:21:11.649 UTC
BGP routing table entry for 198.51.100.0/24
Versions:
  Process           bRIB/RIB  SendTblVer
  Speaker                  9           9
Last Modified: Nov 17 05:19:38.303 for 00:01:33
Paths: (2 available, best #1)
  Advertised to peers (in unique update groups):
    10.0.24.2       
  Path #1: Received by speaker 0
  Advertised to peers (in unique update groups):
    10.0.24.2       
  65101
    1.1.1.1 (metric 10) from 1.1.1.1 (1.1.1.1)
      Origin IGP, metric 0, localpref 200, valid, internal, best, group-best
      Received Path ID 0, Local Path ID 0, version 9
      Community: 65101:200
  Path #2: Received by speaker 0
  Not advertised to any peer
  65102
    10.0.24.2 from 10.0.24.2 (4.4.4.4)
      Origin IGP, metric 0, localpref 100, valid, external, group-best
      Received Path ID 0, Local Path ID 0, version 0
      Origin-AS validity: not-found
RP/0/0/CPU0:XR2#show route 198.51.100.0/24
Tue Nov 17 05:21:13.599 UTC

Routing entry for 198.51.100.0/24
  Known via "bgp 65000", distance 200, metric 0
  Tag 65101, type internal
  Installed Nov 17 05:19:38.446 for 00:01:35
  Routing Descriptor Blocks
    1.1.1.1, from 1.1.1.1
      Route metric is 0
  No advertising protos. 
RP/0/0/CPU0:XR2#
```
