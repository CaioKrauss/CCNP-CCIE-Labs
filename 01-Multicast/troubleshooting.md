# Multicast Troubleshooting — Configuration, State and Delivery

**Start with a precise source/group and receiver.** Record the source address, destination group, protocol model and expected path. For example, CE2's SSM request for 10.255.0.11 does not match traffic sourced from 10.0.1.1.

## 1. Verify unicast and RPF

```cisco
show ip ospf neighbor
show ip route 10.255.0.1
show ip route 10.255.0.11
show ip rpf 10.255.0.11
```

Check the route toward the source and, where applicable, toward the RP. Compare the expected incoming interface with the actual source-facing link. A unicast route can exist while multicast traffic arrives on an unacceptable interface.

## 2. Verify PIM and the group mapping

```cisco
show ip pim neighbor
show ip pim interface
show ip pim rp mapping
```

Missing PIM adjacency prevents the expected join path. An RP check applies to ASM/BIDIR/Anycast; do not require an RP for the SSM channel. Check the mapping for the exact group, not merely the presence of any RP.

## 3. Verify receiver interest

```cisco
show ip igmp groups
show ip mroute 239.1.1.1
```

On CE2/CE3, inspect the receiver-facing Fa0/0. Local test receivers may have null OIL. On transit routers, inspect downstream OIL entries toward the receiver. An empty downstream branch on a transit node needs a different explanation from local reception.

## 4. Verify the right tree and actual traffic

```cisco
show ip mroute 232.1.1.1
show ip mroute 239.2.2.2
show ip mroute count
```

| Model | State to examine | Frequent wrong inference |
|---|---|---|
| ASM | (*,G), (S,G), IOS T flag, RPF, IIF/OIL | Any (S,G) proves full SPT delivery |
| SSM | Correct (S,G), source selection, counter increments | Same group means any source is accepted |
| BIDIR | Shared state, DF roles, upstream direction | No per-source tree means no data |
| Anycast | Selected RP route, MSDP, SA, mroute counters | SA cache proves receiver delivery |

Send a bounded test from the intended source, compare before/after counters and record receiver replies where available. Counter changes need a time interval and a named device.

## 5. Controlled failures are a separate exercise

On this physical tree, losing a transit link may break service entirely. Do not expect a redundant path that does not exist. A future failure exercise should record the baseline, one deliberate fault, symptoms, diagnosis, restoration and a post-recovery test. Do not mark such a test complete merely because its commands are documented.

LAB 04 contains a historical loopback failure. It does not prove survival of a full RR-P outage.

## Evidence checklist

- [ ] Source/group and receiver explicitly identified
- [ ] Unicast reachability and RPF checked
- [ ] PIM and group mapping appropriate for the multicast model
- [ ] Membership and IIF/OIL captured
- [ ] Traffic generated and measured at named points
- [ ] Expected result separated from actual result
- [ ] Limitations and unresolved causes retained
- [ ] Any injected fault restored and recovery evidenced

See [command reference](comandos.md) and [IPv6-specific checks](LAB05-IPv6-Multicast.md).
