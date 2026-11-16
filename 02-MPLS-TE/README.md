# My MPLS, VPN and RSVP-TE Labs

This section is where I document **service forwarding and Traffic Engineering**, using Cisco IOS, IOS XE and IOS XR.

## What I tested

| Lab | What I wanted to prove | Result |
|---|---|---|
| [L3VPN](LAB01-L3VPN-ISIS-LDP-IOS-XR.md) | VPNv4 + VRF + LDP transport | CUST-A **20/20** pings each way |
| [06 — VPWS](LAB06-L2VPN-VPWS-IOS-IOSXR.md) | LDP-signaled Ethernet pseudowire | IOS R2–R1 PW UP; CE forwarding proven |
| [07 — VPLS](LAB07-VPLS-CSR1000v-VPWS-C7200.md) | Bridge-domain + VFI + VPWS spoke | Four CEs reached each other |
| [08 — RSVP-TE](LAB08-MPLS-RSVP-TE-ISIS-AUTOROUTE.md) | Explicit ERO and local Autoroute | Tunnel via R3, **1→5→1 Mbps** |
| [09 — FRR](LAB09-MPLS-TE-FRR-NNHOP-IOS.md) | Bypass failed primary path | **Ready→Active→Ready** and traffic via R2 |
| [10 — CSPF / Affinity](LAB10-MPLS-TE-CSPF-AFFINITY-PREEMPTION-IOS.md) | Constraint-driven paths and RSVP preemption | Path changes, preemption syslog, recovery |

## How I separate the layers

- **IS-IS:** gets me to the remote router.
- **LDP/MPLS:** provides transport labels.
- **MP-BGP VPNv4 + RT:** exchanges/imports customer routes for L3VPN.
- **VPWS/VPLS:** extends an Ethernet service over a pseudowire.
- **RSVP-TE:** signals a chosen LSP and reserves resources; it does not guarantee throughput without QoS.

My original MPLS screenshot illustrates the **L3VPN** path; it does not show all later topologies.

![My initial MPLS canvas](topology/mpls-eve-ng.png)

**Evidence:** Each lab has links to its own running/startup configs and captured CLI. I keep them separate from my conclusions. SR-MPLS is documented in [LAB 11](../03-Segment-Routing/LAB11-SR-MPLS-ISIS-IOSXR.md).
