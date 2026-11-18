# LAB 18 — BGP PIC Edge / Core

## What I learned

I separated two recovery layers: selecting a different BGP exit (Edge) and protecting transport to the same BGP next-hop (Core). The historical Core test shows a CEF path change while the BGP best path remains unchanged. The fresh collection confirms installed backups and restored links; it does not measure convergence speed or packet loss.

## Topology and scope

```text
R1 (AS 65101) — XR1 (AS 65000) == two IS-IS links == XR2 (AS 65000) — R2 (AS 65102)
3.3.3.3         1.1.1.1                              2.2.2.2         4.4.4.4
```

- XR1–R1: 10.0.13.2/30 ↔ 10.0.13.1/30.
- XR2–R2: 10.0.24.1/30 ↔ 10.0.24.2/30.
- Primary XR1–XR2: Gi0/0/0/0, 10.0.12.1/30 ↔ 10.0.12.2/30, IS-IS metric 10.
- Alternate XR1–XR2: Gi0/0/0/2, 10.0.12.5/30 ↔ 10.0.12.6/30, IS-IS metric 100.
- Prefix: 198.51.100.0/24, originated by both IOS edges using static Null0 routes and BGP network statements.
- XR configurations identify IOS XR 6.3.1; IOS configuration version is 15.2. Prior SR-TE and VPN configuration is retained in the full snapshots.

## Configuration actually collected

XR1 selects and installs one backup using:

```cisco
route-policy PIC-EDGE-TEST
  set path-selection backup 1 install
end-policy
!
router bgp 65000
 address-family ipv4 unicast
  additional-paths selection route-policy PIC-EDGE-TEST
```

XR1 retains `bgp bestpath as-path multipath-relax`, but the LAB 17 `maximum-paths eibgp 2` statement is absent. The observed state is primary/backup, not two active ECMP exits.

XR2 applies `EBGP-R2-ECMP-IN` inbound from R2 and sets LOCAL_PREF 200 for the test prefix. XR1 uses `IBGP-XR2-BASE` inbound from XR2 and `PASS-ALL` inbound from R1. Therefore the current preferred route is the iBGP path via XR2 (LOCAL_PREF 200); R1 is the eBGP backup (LOCAL_PREF 100). Defined but unattached policies must not be mistaken for active policy.

XR1 has `fast-reroute per-prefix` and `fast-reroute per-prefix ti-lfa` under the primary IS-IS interface. Operational CEF explicitly identifies the backup as **Local-LFA**. Configuration of TI-LFA does not prove that this repair uses TI-LFA.

[Complete current configurations and persistence record](configs/LAB18-BGP-PIC-2026-11-18/README.md).

## Tests and evidence

Historical timestamps below are UTC on 2026-11-18. [Original user CLI](evidencias/LAB18-BGP-PIC-2026-11-18/HISTORICAL-CLI.md) is preserved separately from the new live collection.

| Stage | Evidence | Interpretation |
|---|---|---|
| 19:03:53 — transport backup ready | IS-IS FRR via 10.0.12.6; CEF primary protected and alternate Local-LFA | Backup preinstalled for 2.2.2.2/32 |
| 19:06:01 — preliminary transport failure | CEF to 2.2.2.2 uses Gi0/0/0/2, but BGP still prefers R1 | Transport failover alone does not demonstrate protection of a prefix actively using XR2 |
| 19:07:51 — corrected baseline | AS 65102, next-hop 2.2.2.2, LOCAL_PREF 200, best; prefix CEF Gi0/0/0/0 → 10.0.12.2 | Test prefix now uses remote next-hop |
| 19:08:34 — Core failure stage | Same BGP best/next-hop, iBGP established; both next-hop CEF and prefix CEF use Gi0/0/0/2 → 10.0.12.6 | Functional transport recovery while retaining BGP exit |
| 19:13–19:14 — new live collection | Primary restored; interfaces Up/Up; prefix CEF Gi0/0/0/0; Local-LFA backup via Gi0/0/0/2 | Current restored state confirmed |

The source conversation describes an earlier **Edge failover from R1 toward XR2/R2**, but the available history does not return that stage's raw CLI. I retain it as a reported test, not a newly verified failure-stage result. The current live BGP and CEF outputs directly confirm the alternate BGP path is selected and represented as backup.

### Core procedure recorded in the conversation

With XR2 already selected as best for the prefix, the lab disabled XR1 Gi0/0/0/0, checked BGP and CEF, and restored the interface with `no shutdown` and `commit`. This collection did **not** repeat the failure or alter routing policies.

The CLI at 19:08:34 shows BGP version 11 and last modification 19:07:33, while CEF LDI changed at 19:08:26. This supports a transport resolution change without a new best path. These timestamps are not a packet-loss or convergence-time measurement.

## Validation commands

IOS XR:

```cisco
show bgp summary
show bgp ipv4 unicast 198.51.100.0/24
show cef ipv4 198.51.100.0/24 detail
show cef ipv4 2.2.2.2/32 detail
show isis adjacency
show isis fast-reroute 2.2.2.2/32 detail
show ipv4 interface brief
show running-config
show configuration commit list
```

IOS:

```cisco
show ip bgp summary
show ip bgp 198.51.100.0
show ip route 198.51.100.0
show ip interface brief
show running-config
write memory
show startup-config
```

Read the recursive next-hop and its resolved adjacency together. A top-level CEF “0 backups” counter does not negate the explicitly displayed recursive backup or the Local-LFA at the underlying next-hop. Likewise, `backup, add-path` is not evidence of negotiated ADD-PATH advertisement to a peer.

## Live collection and persistence

Collected directly through EVE-NG Telnet consoles on **2026-11-18, 16:13–16:14 America/Sao_Paulo (19:13–19:14 UTC)**, before LAB 19.

- XR1 and XR2: entered configuration mode, checked an empty candidate, executed `commit`; both returned `No configuration changes to commit.` Their running configurations were already committed. No new commit ID was created.
- R1 and R2: `write memory` returned `[OK]`; extracted startup configurations matched running configurations exactly.
- All four complete configurations include their final `end`; hostnames were checked. Before/after running configurations matched.
- No reboot, failure injection, traffic generation or routing-policy change was performed.
- [XR1 live CLI](evidencias/LAB18-BGP-PIC-2026-11-18/XR1-live-cli.txt), [XR2 live CLI](evidencias/LAB18-BGP-PIC-2026-11-18/XR2-live-cli.txt), [R1 live CLI](evidencias/LAB18-BGP-PIC-2026-11-18/R1-live-cli.txt), [R2 live CLI](evidencias/LAB18-BGP-PIC-2026-11-18/R2-live-cli.txt).

## Limits and next step

The evidence establishes backup state, functional Core forwarding-table recovery and current persistence. It does not establish subsecond convergence, prefix-count independence, uninterrupted packet delivery, hardware forwarding performance or recovery after reboot. The prefix is originated toward Null0 on both edges; successful control-plane selection is not an end-to-end service test.

Before making a stronger PIC performance claim, capture continuous traffic, loss and recovery timing across multiple prefix counts. Recover the original Edge before/failure/restored CLI if available. LAB 19 can use these actual saved configurations as its starting point.

Concept reference: [Cisco — BGP Prefix Independent Convergence](https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/bgp/bgp-config-cisco8000/r-wrapper-bgp-routing-optimisation-and-convergence-techniques/c-bgp-prefix-independent-convergence.html). PIC preinstalls alternate paths to accelerate recovery. This newer platform guide is conceptual context, not proof of feature or performance parity with XRv 6.3.1.
