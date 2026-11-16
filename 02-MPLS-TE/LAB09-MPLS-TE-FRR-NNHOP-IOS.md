# LAB 09 — RSVP-TE Fast Reroute (NNHOP)

**My goal:** protect R1's primary RSVP-TE LSP through **R3** with a local backup through **R2**, then observe failure and recovery.

## My topology

```text
              R2 (backup) ------> R4
             /                   /
R1 (PLR) ---                    /
             \                 /
              R3 (primary) --->

Tunnel100: R1 → R3 → R4 (primary, metric 40)
Tunnel200: R1 → R2 → R4 (backup, metric 20)
```

I used four Cisco 7200 routers, IOS 15.2(4)S7, IS-IS and RSVP-TE. R1 was the **Point of Local Repair (PLR)**.

## What I configured on R1

```cisco
interface Tunnel100
 tunnel mpls traffic-eng path-option 1 explicit name VIA_R3
 tunnel mpls traffic-eng autoroute announce
 tunnel mpls traffic-eng fast-reroute
!
interface Tunnel200
 tunnel mpls traffic-eng path-option 1 explicit name VIA_R2_BACKUP
!
interface FastEthernet1/0
 mpls traffic-eng backup-path Tunnel200
```

The backup had **no Autoroute**. The path weights (40 primary, 20 backup) did not decide their roles: the explicit paths, primary tunnel and backup association did.

## What I observed (2026-11-16)

1. **Before failure:** Tunnel100 and Tunnel200 were UP; FRR showed **Ready**, NNHOP, `Active: 0`.
2. **An early failure attempt:** a long ping returned **122/154** while FRR still reported Ready. I did **not** count this as a verified switchover.
3. **Local failure:** I shut R1 Fa1/0, the protected egress. FRR changed to **Active** and Tunnel200 showed `Active: 1`.
4. **Backup forwarding:** traceroute followed **R1 → R2 → R4**; ping to R4 returned **5/5**.
5. **Recovery:** I restored the interface. Tunnel100 returned via **R3**; FRR went back to **Ready**, `Active: 0`.

My decisive FRR output:

```text
PRIMARY-RSVP-TE-VIA-R3  Fa1/0  1M:G  Tu200:3  Active  any-unl  N-Nhop
Protected LSPs/Sub-LSPs: 1, Active: 1
```

```cisco
show mpls traffic-eng tunnels
show mpls traffic-eng fast-reroute database
show ip rsvp fast-reroute
show mpls traffic-eng tunnels backup
show ip route 4.4.4.4
traceroute 4.4.4.4
```

## What I learned

**FRR repairs MPLS forwarding locally without necessarily changing the IP route shown in the RIB.** The R1 route could still resolve via Tunnel100 while the protected LSP used a bypass.

**Limit:** I demonstrated Ready → Active → Ready and backup traffic, **not** a measured sub-50-ms switchover. I did not prove hitless recovery. Running/startup snapshots matched; the pending config-register change was not reboot-tested.

**Evidence:** [Configs](configs/LAB09-FRR-2026-11-16/) · [Actual CLI timeline](evidencias/LAB09-FRR-2026-11-16/FRR-CLI-OBSERVED.md) · [Collection/persistence](evidencias/LAB09-FRR-2026-11-16/COLLECTION-AND-PERSISTENCE.md).
