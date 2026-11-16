# LAB 05 — IPv6 Multicast: ASM, SSM and MLDv2

**My goal:** extend the seven-router lab to IPv6 using OSPFv3, PIM-SM, a static ASM RP and source-specific MLDv2 joins. I tested this on **2026-11-13**.

![My seven-router topology](topology/multicast-eve-ng.png)

## My setup

- **Unicast:** OSPFv3 process 10, area 0; IPv6 loopbacks in `2001:DB8:100::/64`.
- **ASM:** group `FF1E::1234`; RP `2001:DB8:100::1` on RR-P.
- **SSM:** group `FF3E::1234`; selected source `2001:DB8:1::1` on CE1.
- **Receivers:** CE2 and CE3.

## What I configured

```cisco
ipv6 unicast-routing
ipv6 multicast-routing
ipv6 pim rp-address 2001:DB8:100::1
! On CE2/CE3 receiver-facing interfaces:
ipv6 mld join-group FF1E::1234
ipv6 mld join-group FF3E::1234 2001:DB8:1::1
```

I used the MLD SSM syntax captured in my running configs; IOS did not save an `include` keyword.

## What I observed

| Test | My result |
|---|---|
| OSPFv3 and IPv6 unicast | RR-P formed expected adjacencies; two loopback tests returned **5/5** each |
| ASM with CE1 source `2001:DB8:1::1` | **5/5** pings and **11 multicast replies**, including both CEs |
| ASM control plane | RR-P showed `(*,G)`, `(S,G)` and PIM Register activity |
| SSM with selected source `::1` | **5/5** pings, **10 multicast replies** (five per receiver) |
| SSM with unselected source `2001:DB8:1::99` | **0/5** pings, no receiver replies |

## What I learned

**ASM uses an RP; SSM uses an explicit source/group subscription.** MLDv2 carries IPv6 receiver membership. The positive/negative SSM tests support source filtering, but I did not capture the exact interface where unwanted traffic was discarded.

I initially saw a timeout when using CE1's Loopback0 as an ASM source; I did not isolate its cause. **MLDv1 was not tested.** The later configuration snapshot confirms the temporary `::99` address was removed, but not startup persistence.

```cisco
show ipv6 ospf neighbor
show ipv6 pim neighbor
show ipv6 pim group-map FF1E::1234
show ipv6 mld groups
show ipv6 mroute FF1E::1234
show ipv6 mroute FF3E::1234
show ipv6 rpf 2001:DB8:1::1
```

**Evidence:** [CLI capture](evidencias/LAB05-IPv6-PIM-MLDv2.txt) · [Post-test configs](configs/snapshot-2026-11-13/) · [Addressing](topology/enderecamento.md).
