# My Multicast Troubleshooting Commands (Cisco IOS)

I check **unicast/RPF → PIM/RP → receiver membership → `(*,G)`/`(S,G)` → packet counters**.

| My question | Command |
|---|---|
| Is my unicast path ready? | `show ip ospf neighbor` |
| Which route reaches the source? | `show ip route 10.255.0.11` |
| What is the expected RPF interface? | `show ip rpf 10.255.0.11` |
| Do I have PIM neighbors? | `show ip pim neighbor` |
| Which RP serves my group? | `show ip pim rp mapping` |
| Who is the BIDIR DF? | `show ip pim interface df` |
| Did my receiver join? | `show ip igmp groups` |
| How is ASM state built? | `show ip mroute 239.1.1.1` |
| Is my exact SSM source selected? | `show ip mroute 232.1.1.1` |
| Is BIDIR using its shared tree? | `show ip mroute 239.2.2.2` |
| Did my Anycast RP learn the source? | `show ip msdp peer` / `show ip msdp sa-cache` |
| Did packets actually advance? | `show ip mroute count` |

**My reminder:** `(S,G)` by itself does not prove end-to-end delivery. A local receiver can have a null OIL. I compare counters **before and after** sending traffic.

For IPv6 I use the commands from [LAB 05](LAB05-IPv6-Multicast.md). For a fuller diagnostic sequence, see [my troubleshooting notes](troubleshooting.md).
