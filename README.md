# CCNP / CCIE Advanced Networking Labs

Hands-on networking labs focused on advanced routing, Service Provider technologies, troubleshooting, and network automation.

## Study plan
**12 weeks | 60 sessions | 120 hours**  
**November 16, 2026 – February 5, 2027**  
Monday–Friday, 15:00–17:00 (America/Sao_Paulo).

| Week | Focus | Folder |
|---|---|---|
| 1–2 | Multicast advanced: PIM-SM, RPF, RP, SPT, SSM | [01-Multicast](01-Multicast/) |
| 3 | MPLS forwarding, LDP synchronization, RSVP-TE and FRR | [02-MPLS-TE](02-MPLS-TE/) |
| 4 | SR-MPLS, SR-TE, TI-LFA, SRv6 | [03-Segment-Routing](03-Segment-Routing/) |
| 5 | EVPN/VXLAN and multihoming | [04-EVPN-VXLAN](04-EVPN-VXLAN/) |
| 6 | QoS and MPLS TC | [05-QoS](05-QoS/) |
| 7 | BGP Add-Path, PIC, RPKI and multivendor policies | [06-BGP-Advanced](06-BGP-Advanced/) |
| 8 | BFD, VRRP, LACP and MSTP | [07-High-Availability](07-High-Availability/) |
| 9 | CoPP, uRPF, DAI and AAA | [08-Security](08-Security/) |
| 10 | Python, NETCONF, RESTCONF and Ansible | [09-Automation](09-Automation/) |
| 11 | Telemetry, observability and IPv6 | [10-IPv6](10-IPv6/) |
| 12 | Integrated troubleshooting challenge | [11-Troubleshooting](11-Troubleshooting/) |

## Lab methodology
1. Review advanced concepts and make a hypothesis (20 min).
2. Build or modify a topology in EVE-NG, inject faults, and troubleshoot (75 min).
3. Verify the control and forwarding planes, collect evidence, and write a short RCA (25 min).

Use [LAB-TEMPLATE.md](LAB-TEMPLATE.md) to document each lab. Prefer Cisco IOS-XE/IOS-XR and use Huawei/Nokia images when available.

> **Security:** Only publish synthetic IP addresses, credentials and configurations. Do not commit production/customer data, passwords, tokens, or confidential logs.

This is an independent study project, not an official Cisco training course.
