# Captured CLI evidence

Source: [Ideias para lab Multicast](https://chatgpt.com/c/6af4c0c1-7098-83e9-99c1-7f13b5e1cb49) (account access required). User-pasted router outputs, preserved below; these are historical captures, not new tests. Section labels are editorial. Router timestamps are UTC.

## Source message 79291396-809d-461c-bcec-59bf70db52fe

```text
RP/0/0/CPU0:XR1#show segment-routing mapping-server prefix-sid-map ipv4
Tue Nov 17 02:02:43.743 UTC
Prefix               SID Index    Range        Flags
3.3.3.3/32           3            1            
4.4.4.4/32           4            1            

Number of mapping entries: 2
RP/0/0/CPU0:XR1#show isis database verbose
Tue Nov 17 02:02:45.303 UTC

IS-IS CORE (Level-2) Link State Database
LSPID                 LSP Seq Num  LSP Checksum  LSP Holdtime  ATT/P/OL
XR1.00-00           * 0x0000000a   0x904a        1194            0/0/0
  Area Address:   49.0001
  NLPID:          0xcc
  IP Address:     1.1.1.1
  Router ID:      1.1.1.1
  Metric: 0          IP-Extended 1.1.1.1/32
    Prefix-SID Index: 1, Algorithm:0, R:0 N:1 P:0 E:0 V:0 L:0
    Prefix Attribute Flags: X:0 R:0 N:1
    Source Router ID: 1.1.1.1
  Metric: 10         IP-Extended 10.0.12.0/30
    Prefix Attribute Flags: X:0 R:0 N:0
  Metric: 10         IP-Extended 10.0.13.0/30
    Prefix Attribute Flags: X:0 R:0 N:0
  Hostname:       XR1
  Router Cap:     1.1.1.1, D:0, S:0
    Segment Routing: I:1 V:0, SRGB Base: 16000 Range: 8000
    SR Algorithm: 
      Algorithm: 0
      Algorithm: 1
    Node Maximum SID Depth: 
      Subtype: 1, Value: 10
  Metric: 10         IS-Extended XR2.00
    Affinity: 0x00000000
    Interface IP Address: 10.0.12.1
    Neighbor IP Address: 10.0.12.2
    Physical BW: 1000000 kbits/sec
    Reservable Global pool BW: 0 kbits/sec
    Global Pool BW Unreserved: 
      [0]: 0        kbits/sec          [1]: 0        kbits/sec
      [2]: 0        kbits/sec          [3]: 0        kbits/sec
      [4]: 0        kbits/sec          [5]: 0        kbits/sec
      [6]: 0        kbits/sec          [7]: 0        kbits/sec
    Admin. Weight: 10
    Ext Admin Group: Length: 32
      0x00000000   0x00000000
      0x00000000   0x00000000
      0x00000000   0x00000000
      0x00000000   0x00000000
    Link Maximum SID Depth: 
      Subtype: 1, Value: 10
    ADJ-SID: F:0 B:0 V:1 L:1 S:0 P:0 weight:0 Adjacency-sid:24003
  Metric: 10         IS-Extended R1.00
    Affinity: 0x00000000
    Interface IP Address: 10.0.13.2
    Neighbor IP Address: 10.0.13.1
    Physical BW: 1000000 kbits/sec
    Reservable Global pool BW: 0 kbits/sec
    Global Pool BW Unreserved: 
      [0]: 0        kbits/sec          [1]: 0        kbits/sec
      [2]: 0        kbits/sec          [3]: 0        kbits/sec
      [4]: 0        kbits/sec          [5]: 0        kbits/sec
      [6]: 0        kbits/sec          [7]: 0        kbits/sec
    Admin. Weight: 10
    Ext Admin Group: Length: 32
      0x00000000   0x00000000
      0x00000000   0x00000000
      0x00000000   0x00000000
      0x00000000   0x00000000
    Link Maximum SID Depth: 
      Subtype: 1, Value: 10
    ADJ-SID: F:0 B:0 V:1 L:1 S:0 P:0 weight:0 Adjacency-sid:24001
  SID Binding:    3.3.3.3/32 F:0 M:0 S:0 D:0 A:0 Weight:0 Range:1
    SID: Start:3, Algorithm:0, R:0 N:0 P:0 E:0 V:0 L:0
  SID Binding:    4.4.4.4/32 F:0 M:0 S:0 D:0 A:0 Weight:0 Range:1
    SID: Start:4, Algorithm:0, R:0 N:0 P:0 E:0 V:0 L:0
XR2.00-00             0x00000008   0x6008        1194            0/0/0
  Area Address:   49.0001
  Metric: 10         IS-Extended XR1.00
    Affinity: 0x00000000
    Interface IP Address: 10.0.12.2
    Neighbor IP Address: 10.0.12.1
    Physical BW: 1000000 kbits/sec
    Reservable Global pool BW: 0 kbits/sec
    Global Pool BW Unreserved: 
      [0]: 0        kbits/sec          [1]: 0        kbits/sec
      [2]: 0        kbits/sec          [3]: 0        kbits/sec
      [4]: 0        kbits/sec          [5]: 0        kbits/sec
      [6]: 0        kbits/sec          [7]: 0        kbits/sec
    Admin. Weight: 10
    Ext Admin Group: Length: 32
      0x00000000   0x00000000
      0x00000000   0x00000000
      0x00000000   0x00000000
      0x00000000   0x00000000
    Link Maximum SID Depth: 
      Subtype: 1, Value: 10
    ADJ-SID: F:0 B:0 V:1 L:1 S:0 P:0 weight:0 Adjacency-sid:24001
  Metric: 10         IS-Extended R2.00
    Affinity: 0x00000000
    Interface IP Address: 10.0.24.1
    Neighbor IP Address: 10.0.24.2
    Physical BW: 1000000 kbits/sec
    Reservable Global pool BW: 0 kbits/sec
    Global Pool BW Unreserved: 
      [0]: 0        kbits/sec          [1]: 0        kbits/sec
      [2]: 0        kbits/sec          [3]: 0        kbits/sec
      [4]: 0        kbits/sec          [5]: 0        kbits/sec
      [6]: 0        kbits/sec          [7]: 0        kbits/sec
    Admin. Weight: 10
    Ext Admin Group: Length: 32
      0x00000000   0x00000000
      0x00000000   0x00000000
      0x00000000   0x00000000
      0x00000000   0x00000000
    Link Maximum SID Depth: 
      Subtype: 1, Value: 10
    ADJ-SID: F:0 B:0 V:1 L:1 S:0 P:0 weight:0 Adjacency-sid:24003
  NLPID:          0xcc
  IP Address:     2.2.2.2
  Router ID:      2.2.2.2
  Metric: 0          IP-Extended 2.2.2.2/32
    Prefix-SID Index: 2, Algorithm:0, R:0 N:1 P:0 E:0 V:0 L:0
    Prefix Attribute Flags: X:0 R:0 N:1
    Source Router ID: 2.2.2.2
  Metric: 10         IP-Extended 10.0.12.0/30
    Prefix Attribute Flags: X:0 R:0 N:0
  Metric: 10         IP-Extended 10.0.24.0/30
    Prefix Attribute Flags: X:0 R:0 N:0
  Hostname:       XR2
  Router Cap:     2.2.2.2, D:0, S:0
    Segment Routing: I:1 V:0, SRGB Base: 16000 Range: 8000
    SR Algorithm: 
      Algorithm: 0
      Algorithm: 1
    Node Maximum SID Depth: 
      Subtype: 1, Value: 10
R1.00-00              0x00000004   0x2655        273             0/0/0
  Area Address:   49.0001
  NLPID:          0xcc
  Hostname:       R1
  IP Address:     3.3.3.3
  Metric: 10         IS-Extended XR1.00
  Metric: 0          IP-Extended 3.3.3.3/32
  Metric: 10         IP-Extended 10.0.13.0/30
R2.00-00              0x00000004   0x8bd7        357             0/0/0
  Area Address:   49.0001
  NLPID:          0xcc
  Hostname:       R2
  IP Address:     4.4.4.4
  Metric: 10         IS-Extended XR2.00
  Metric: 0          IP-Extended 4.4.4.4/32
  Metric: 10         IP-Extended 10.0.24.0/30

 Total Level-2 LSP count: 4     Local Level-2 LSP count: 1
RP/0/0/CPU0:XR1#  

RP/0/0/CPU0:XR2#show isis segment-routing label table
Tue Nov 17 02:03:15.031 UTC

IS-IS CORE IS Label Table
Label         Prefix/Interface
----------    ----------------
16001         1.1.1.1/32
16002         Loopback0
16003         3.3.3.3/32
16004         4.4.4.4/32
RP/0/0/CPU0:XR2#show mpls forwarding
Tue Nov 17 02:03:15.741 UTC
Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
Label  Label       or ID              Interface                    Switched    
------ ----------- ------------------ ------------ --------------- ------------
16001  Pop         SR Pfx (idx 1)     Gi0/0/0/0    10.0.12.1       0           
16003  16003       SR Pfx (idx 3)     Gi0/0/0/0    10.0.12.1       0           
16004  Pop         SR Pfx (idx 4)     Gi0/0/0/1    10.0.24.2       0           
24000  Pop         SR Adj (idx 1)     Gi0/0/0/0    10.0.12.1       0           
24001  Pop         SR Adj (idx 3)     Gi0/0/0/0    10.0.12.1       0           
24002  Pop         SR Adj (idx 1)     Gi0/0/0/1    10.0.24.2       0           
24003  Pop         SR Adj (idx 3)     Gi0/0/0/1    10.0.24.2       0           
24004  16003       3.3.3.3/32         Gi0/0/0/0    10.0.12.1       0           
24005  Pop         1.1.1.1/32         Gi0/0/0/0    10.0.12.1       0           
24006  Unlabelled  10.0.13.0/30       Gi0/0/0/0    10.0.12.1       0           
24007  Pop         4.4.4.4/32         Gi0/0/0/1    10.0.24.2       98          
RP/0/0/CPU0:XR2#
```

## Source message 22613293-3d4b-43a6-ba7b-fcfa83284acf

```text
RP/0/0/CPU0:XR2#show mpls forwarding
Tue Nov 17 02:05:19.582 UTC
Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
Label  Label       or ID              Interface                    Switched    
------ ----------- ------------------ ------------ --------------- ------------
16001  Pop         SR Pfx (idx 1)     Gi0/0/0/0    10.0.12.1       0           
16003  16003       SR Pfx (idx 3)     Gi0/0/0/0    10.0.12.1       0           
16004  Pop         SR Pfx (idx 4)     Gi0/0/0/1    10.0.24.2       396000      
24000  Pop         SR Adj (idx 1)     Gi0/0/0/0    10.0.12.1       0           
24001  Pop         SR Adj (idx 3)     Gi0/0/0/0    10.0.12.1       0           
24002  Pop         SR Adj (idx 1)     Gi0/0/0/1    10.0.24.2       0           
24003  Pop         SR Adj (idx 3)     Gi0/0/0/1    10.0.24.2       0           
24004  16003       3.3.3.3/32         Gi0/0/0/0    10.0.12.1       4160        
24005  Pop         1.1.1.1/32         Gi0/0/0/0    10.0.12.1       0           
24006  Unlabelled  10.0.13.0/30       Gi0/0/0/0    10.0.12.1       0           
24007  Pop         4.4.4.4/32         Gi0/0/0/1    10.0.24.2       294         
RP/0/0/CPU0:XR2#

RP/0/0/CPU0:XR1#show mpls forwarding
Tue Nov 17 02:05:15.652 UTC
Local  Outgoing    Prefix             Outgoing     Next Hop        Bytes       
Label  Label       or ID              Interface                    Switched    
------ ----------- ------------------ ------------ --------------- ------------
16002  Pop         SR Pfx (idx 2)     Gi0/0/0/0    10.0.12.2       0           
16003  Pop         SR Pfx (idx 3)     Gi0/0/0/1    10.0.13.1       4000        
16004  16004       SR Pfx (idx 4)     Gi0/0/0/0    10.0.12.2       0           
24000  Pop         SR Adj (idx 1)     Gi0/0/0/1    10.0.13.1       0           
24001  Pop         SR Adj (idx 3)     Gi0/0/0/1    10.0.13.1       0           
24002  Pop         SR Adj (idx 1)     Gi0/0/0/0    10.0.12.2       0           
24003  Pop         SR Adj (idx 3)     Gi0/0/0/0    10.0.12.2       0           
24004  Pop         3.3.3.3/32         Gi0/0/0/1    10.0.13.1       254         
24005  Pop         2.2.2.2/32         Gi0/0/0/0    10.0.12.2       0           
24006  Unlabelled  10.0.24.0/30       Gi0/0/0/0    10.0.12.2       0           
24007  16004       4.4.4.4/32         Gi0/0/0/0    10.0.12.2       4160        
RP/0/0/CPU0:XR1

R1#show mpls forwarding-table
Local      Outgoing   Prefix           Bytes Label   Outgoing   Next Hop    
Label      Label      or Tunnel Id     Switched      interface              
16         Pop Label  1.1.1.1/32       0             Fa0/0      10.0.13.2   
17         Pop Label  10.0.12.0/30     0             Fa0/0      10.0.13.2   
18         24005      2.2.2.2/32       0             Fa0/0      10.0.13.2   
19         24006      10.0.24.0/30     0             Fa0/0      10.0.13.2   
20         24007      4.4.4.4/32       0             Fa0/0      10.0.13.2   
R1#ping 4.4.4.4 source 3.3.3.3 repeat 20
Type escape sequence to abort.
Sending 20, 100-byte ICMP Echos to 4.4.4.4, timeout is 2 seconds:
Packet sent with a source address of 3.3.3.3 
!!!!!!!!!!!!!!!!!!!!
Success rate is 100 percent (20/20), round-trip min/avg/max = 48/53/64 ms
R1#

R2#show mpls forwarding-table
Local      Outgoing   Prefix           Bytes Label   Outgoing   Next Hop    
Label      Label      or Tunnel Id     Switched      interface              
16         Pop Label  2.2.2.2/32       0             Fa0/0      10.0.24.1   
17         24005      1.1.1.1/32       0             Fa0/0      10.0.24.1   
18         24004      3.3.3.3/32       0             Fa0/0      10.0.24.1   
19         Pop Label  10.0.12.0/30     0             Fa0/0      10.0.24.1   
20         24006      10.0.13.0/30     0             Fa0/0      10.0.24.1   
R2#ping 3.3.3.3 source 4.4.4.4 repeat 20
Type escape sequence to abort.
Sending 20, 100-byte ICMP Echos to 3.3.3.3, timeout is 2 seconds:
Packet sent with a source address of 4.4.4.4 
!!!!!!!!!!!!!!!!!!!!
Success rate is 100 percent (20/20), round-trip min/avg/max = 32/53/68 ms
R2#
```
