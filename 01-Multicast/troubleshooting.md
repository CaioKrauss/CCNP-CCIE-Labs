# My Multicast Troubleshooting Checklist

When multicast does not work, I start with the exact **source S, group G and receiver**. In SSM, `(10.255.0.11,232.1.1.1)` and `(10.0.1.1,232.1.1.1)` are different channels.

## 1. Unicast and RPF

```cisco
show ip ospf neighbor
show ip route 10.255.0.11
show ip rpf 10.255.0.11
```

I first confirm the path **back to the actual source**. A correct unicast route does not help if multicast arrives on the wrong RPF interface.

## 2. PIM, RP and membership

```cisco
show ip pim neighbor
show ip pim rp mapping
show ip igmp groups
```

I check PIM on the transit path, the correct RP mapping for **ASM/BIDIR/Anycast**, and the receiver's exact group/source join. **SSM does not need an RP.**

## 3. Tree state and traffic

```cisco
show ip mroute 239.1.1.1
show ip mroute 232.1.1.1
show ip mroute count
```

- **ASM:** I compare `(*,G)`, `(S,G)`, the IOS T flag and IIF/OIL.
- **SSM:** I check the precise source in `(S,G)`.
- **BIDIR:** I inspect the DF and shared tree, not a per-source SPT.
- **Anycast:** I verify the selected RP, MSDP/SA and receiver-facing forwarding state.

I send a bounded test, compare counters on **named routers**, and check receiver replies. An entry in the table is not the same as proven delivery.

## 4. Failure testing

My physical multicast lab is a **tree**, with no alternate transit path. I do not expect OSPF metrics to create redundancy. When I inject a fault, I record the baseline, the single change, symptoms, restoration and post-recovery test.

**My reminder:** in LAB 04 I shut an **RP loopback**, not the central router. I did not demonstrate full-node failover.

[Command reference](comandos.md) · [IPv6 lab](LAB05-IPv6-Multicast.md).
