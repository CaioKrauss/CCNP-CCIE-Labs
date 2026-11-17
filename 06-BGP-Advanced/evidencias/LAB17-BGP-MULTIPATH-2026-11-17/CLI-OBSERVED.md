# LAB 17 — Original XR1 CLI

Source: [Próximo lab SR TE](https://chatgpt.com/c/6afbb8c6-3b30-83e8-ab14-6be459107b14), user message `7c1e3746-c438-44d9-8c94-63986b775a66`.

Captured on 2026-11-17 at 05:34:22 UTC (02:34:22 São Paulo). The user-supplied output below is preserved verbatim. The assistant described this as recovery after the failover test; the returned chat history did not include the failure-stage CLI or traffic measurements. It returned five recent turns, no older-page cursor and no attachments.

```text
RP/0/0/CPU0:XR1#show bgp summary
Tue Nov 17 05:34:22.255 UTC
BGP router identifier 1.1.1.1, local AS number 65000
BGP generic scan interval 60 secs
Non-stop routing is enabled
BGP table state: Active
Table ID: 0xe0000000   RD version: 22
BGP main routing table version 22
BGP NSR Initial initsync version 5 (Reached)
BGP NSR/ISSU Sync-Group versions 0/0
BGP scan interval 60 secs

BGP is operating in STANDALONE mode.


Process       RcvTblVer   bRIB/RIB   LabelVer  ImportVer  SendTblVer  StandbyVer
Speaker              22         22         22         22          22           0

Neighbor        Spk    AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down  St/PfxRcd
2.2.2.2           0 65000      50      52       22    0    0 00:37:52          2
10.0.13.1         0 65101      42      44       22    0    0 00:00:41          1

RP/0/0/CPU0:XR1#show bgp ipv4 unicast 198.51.100.0/24
Tue Nov 17 05:34:22.335 UTC
BGP routing table entry for 198.51.100.0/24
Versions:
  Process           bRIB/RIB  SendTblVer
  Speaker                 22          22
Last Modified: Nov 17 05:33:41.290 for 00:00:41
Paths: (2 available, best #2)
  Advertised to peers (in unique update groups):
    2.2.2.2         
  Path #1: Received by speaker 0
  Not advertised to any peer
  65102
    2.2.2.2 (metric 10) from 2.2.2.2 (2.2.2.2)
      Origin IGP, metric 0, localpref 200, valid, internal, multipath, backup, add-path
      Received Path ID 0, Local Path ID 2, version 22
  Path #2: Received by speaker 0
  Advertised to peers (in unique update groups):
    2.2.2.2         
  65101
    10.0.13.1 from 10.0.13.1 (3.3.3.3)
      Origin IGP, metric 0, localpref 200, valid, external, best, group-best, multipath
      Received Path ID 0, Local Path ID 0, version 22
      Community: 65101:200
      Origin-AS validity: not-found
RP/0/0/CPU0:XR1#show route 198.51.100.0/24
Tue Nov 17 05:34:22.885 UTC

Routing entry for 198.51.100.0/24
  Known via "bgp 65000", distance 20, metric 0
  Tag 65101
  Number of pic paths 1 , type internal and external
  Installed Nov 17 05:33:41.118 for 00:00:41
  Routing Descriptor Blocks
    2.2.2.2, from 2.2.2.2, BGP backup path, BGP multi path
      Route metric is 0
    10.0.13.1, from 10.0.13.1, BGP external, BGP multi path
      Route metric is 0
  No advertising protos. 
RP/0/0/CPU0:XR1#
```
