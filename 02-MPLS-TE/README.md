# MPLS, L3VPN and Traffic Engineering

## Documented lab

| Lab | Scope | Recorded result |
|---|---|---|
| [LAB 01 — IOS / IOS XR L3VPN](LAB01-L3VPN-ISIS-LDP-IOS-XR.md) | IS-IS, LDP, VPNv4, VRF, eBGP PE–CE | CUST-A: 20/20 replies in each direction on 2026-11-13 |
| [LAB 06 — L2VPN VPWS / EoMPLS](LAB06-L2VPN-VPWS-IOS-IOSXR.md) | IS-IS + LDP transport, targeted LDP PW 100, Ethernet between CEs | R2/R1 IOS PW UP; CE pings 9/10 and 10/10; 65 received/77 sent, no drops on R2; XRv classic limitation observed |
| [LAB 07 — VPLS + VPWS spoke](LAB07-VPLS-CSR1000v-VPWS-C7200.md) | CSR1000v BD100/VFI with three local CEs and a Cisco 7200 remote CE | Six fresh configs; 12 directed CE pairs reached 10/10 (three on repeat); service startup verified |
| [LAB 08 — MPLS RSVP-TE and Autoroute](LAB08-MPLS-RSVP-TE-ISIS-AUTOROUTE.md) | IS-IS TE extensions, strict explicit ERO, RSVP bandwidth, local Autoroute | Tunnel100 UP via R3, RSVP 1/5/1 Mbps, CEF via Tunnel100, ping 10/10; four saved configs collected |
| [LAB 09 — MPLS TE Fast Reroute / NNHOP](LAB09-MPLS-TE-FRR-NNHOP-IOS.md) | PLR at R1, protected Tunnel100 via R3 and bypass Tunnel200 via R2 | FRR Ready→Active→Ready; R2 backup path traceroute, 5/5 ping, return to R3; all four startup=running |

![Complete MPLS canvas supplied by the lab owner](topology/mpls-eve-ng.png)

**L3VPN validated:** CE1_A–XR1–R3–R1–CE2_A. **L2VPN LAB06 validated:** L2_CE1–R2–R3–R1–L2_CE2. **Not verified:** CE1_B/CE2_B. The screenshot reflects an earlier topology before R2 was added.

## Read the forwarding chain

IS-IS provides PE-loopback reachability. LDP builds label-switched transport. MP-BGP carries customer VPN routes between PEs. The RT controls VRF import. CEF/LFIB and source-specific pings test whether those layers combine into an actual data path.

The lab guide maps each command to the question it answers, explains the observed label stack, and links the snapshots and raw output.

## LAB 06 — VPWS evidence and configuration

- [Complete step-by-step VPWS guide](LAB06-L2VPN-VPWS-IOS-IOSXR.md)
- [Six real running-config snapshots (14 Nov 2026)](configs/LAB06-VPWS-2026-11-14/)
- [Observed CLI and startup-state evidence](evidencias/LAB06-VPWS-2026-11-14/)
- The L2_CE1/L2_CE2 running configs were captured, but persistence to startup was **not** verified. R1/R2/R3 startup matches running. XR1 final config no longer contains the early experimental xconnect.

## LAB 07 — Separate VPLS topology

The `VPLS.unl` lab uses R1 CSR1000v directly connected to R2 Cisco 7200, plus four CEs. The preceding screenshot belongs to the older MPLS topology, not LAB07.

- [Topology, guide, ping matrix and persistence findings](LAB07-VPLS-CSR1000v-VPWS-C7200.md)
- [Six reviewed running-config snapshots](configs/LAB07-VPLS-2026-11-14/)
- [Startup snapshots, live CLI evidence and manifest](evidencias/LAB07-VPLS-2026-11-14/)

## LAB 08 — RSVP-TE, explicit path and Autoroute

- [Full lab report, topology and observations](LAB08-MPLS-RSVP-TE-ISIS-AUTOROUTE.md)
- [R1–R4 complete running/startup configurations](configs/LAB08-RSVPTE-2026-11-16/)
- [Live observed test outputs and collection/persistence manifest](evidencias/LAB08-RSVPTE-2026-11-16/)
- IS-IS normally sends R1→R2→R4 (metric 20), but RSVP-TE Tunnel100 directs R1→R3→R4 (explicit metric 40). The local route/CEF uses Tunnel100 after `autoroute announce`. RSVP reservation was validated at 1, 5 and restored 1 Mbps; end-to-end ping 10/10.
- All four running/startup snapshots match, but the register correction `0x2102` takes effect only on next reload; no reboot validation was performed.

## LAB 09 — MPLS RSVP-TE FRR / NNHOP node protection

- [Step-by-step lab, observed FRR switching and restoration](LAB09-MPLS-TE-FRR-NNHOP-IOS.md)
- [Four router complete running/startup configurations](configs/LAB09-FRR-2026-11-16/)
- [Lab-owner CLI evidence, collector transcripts and persistence manifest](evidencias/LAB09-FRR-2026-11-16/)
- R1 locally protected its Tunnel100 via R3 using Tunnel200 via R2. The FRR database moved **Ready → Active → Ready** with `Active: 1` at failure, `Active: 0` after restoration. An ICMP ping during the bypass returned 5/5 and a traceroute followed R1→R2→R4; after restoration the traceroute followed R1→R3→R4.
- All four `running-config` snapshots exactly match their respective `startup-config`. The pending `0x2142`→`0x2102` configuration-register transition was **not** verified after reload.
- No quantified fast-reroute switching time or hitless forwarding claim is made. The earlier remote shutdown exhibited 122/154 ping responses with FRR remaining Ready; this is recorded separately.

## Planned scope

LDP-IGP synchronization, dynamic CSPF constraints/affinity, RSVP-TE preemption, FRR repair-time measurement and alternate failure types are future topics.

- [x] First lab documented with direct command evidence
- [x] Configuration and control/data-plane review for CUST-A
- [x] L2VPN VPWS on IOS: control plane, bidirectional CE forwarding and saved R1/R2/R3 configurations
- [x] Controlled RSVP-TE local protection failure and recovery exercise (LAB 09)
- [x] RSVP-TE explicit path / Autoroute and bandwidth reservation validation (LAB 08)
- [x] RSVP-TE FRR NNHOP local repair and recovery validation (LAB 09)
- [ ] RSVP-TE priority-based preemption validation

Use reviewed lab addressing and exclude credentials or production data from every new publication.
