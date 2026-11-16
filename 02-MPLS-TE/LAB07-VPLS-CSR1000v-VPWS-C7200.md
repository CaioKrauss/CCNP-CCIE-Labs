# LAB 07 — VPLS Bridge with a VPWS Spoke

**My goal:** bridge **four CEs** in `192.168.100.0/24` using a CSR1000v and a remote Cisco 7200 pseudowire.

## My topology

```text
CE2 (.2) -- Gi3
CE3 (.3) -- Gi2  R1 CSR1000v (BD 100 + VFI VPLS100)
CE4 (.4) -- Gi1       |
                        Gi4 -- MPLS/LDP -- R2 Cisco 7200 -- CE1 (.1)
                             PW VC 100
```

R1 connects three local Ethernet service instances and one VFI to **bridge-domain 100**. R2 uses a **point-to-point xconnect**, not a multipoint VFI. The R1–R2 underlay has static loopback routes; I did **not** use LAB06's IS-IS transit core.

## What I configured

```cisco
! R1 CSR1000v:
l2vpn vfi context VPLS100
 vpn id 100
 member 2.2.2.2 encapsulation mpls
!
bridge-domain 100
 member GigabitEthernet1 service-instance 100
 member GigabitEthernet2 service-instance 100
 member GigabitEthernet3 service-instance 100
 member vfi VPLS100
!
! R2 Cisco 7200, CE-facing:
interface FastEthernet0/0
 xconnect 1.1.1.1 100 encapsulation mpls
```

## What I observed (2026-11-14)

- Bridge-domain **UP**, VFI/PW **UP** and LDP **Oper**.
- R1 learned CE1's MAC via the remote PW and CE2/CE3/CE4 on their local EFPs.
- **All 12 directed CE pairs reached 10/10 replies.** Three pairs first returned 9/10 and succeeded on a repeat; I did not capture the reason.
- R2 PW counters increased: receive **49 → 112**, send **122 → 191**; no observed drops.
- Running/startup service configurations matched on all six nodes; CSR1000v certificates used different storage representations.

## What I learned

**VPLS bridges MAC addresses across local Ethernet ports and pseudowires.** The remote CE1 is reached through the VPWS spoke, while the other CEs are directly attached to R1's bridge-domain.

```cisco
! R1:
show bridge-domain 100
show l2vpn vfi
show mpls ldp neighbor
! R2:
show mpls l2transport vc detail
! CEs:
show ip arp
ping 192.168.100.1 repeat 10
```

**Limit:** one PW does **not** test VPLS mesh split-horizon, flooding rules, MTU extremes, failure recovery or performance. R2/CEs showed a pending configuration-register change, not tested by a reboot.

**Evidence:** [Running configs](configs/LAB07-VPLS-2026-11-14/) · [Console and startup evidence](evidencias/LAB07-VPLS-2026-11-14/) · [Collector manifest](evidencias/LAB07-VPLS-2026-11-14/manifest.json).
