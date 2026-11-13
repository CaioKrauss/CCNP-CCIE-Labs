# Advanced BGP

## Scope and status

Route reflection, Add-Path, BGP PIC, RPKI, routing policy and multivendor troubleshooting.

**Planned study area: no completed feature-specific lab or measured result is claimed here.**

## Core question

Why was one path selected or rejected, and what changes during a failure?

## What a useful result must show

Trace a prefix through receipt, policy, best-path selection, RIB and FIB. The existing L3VPN lab covers basic VPNv4 exchange, not the advanced features listed here.

## Planned workflow

1. Select the exact platform/image and document prerequisites.
2. Add the topology and addressing.
3. Explain each configuration command and its intended effect.
4. Record platform-specific verification commands, actual output and interpretation.
5. Run bounded traffic tests and, if appropriate, a separately authorized failure/recovery test.

Commands will be tied to a concrete platform when the lab is built; no universal cross-platform syntax or invented output is supplied.

## Completion checklist

- [ ] Topology and baseline captured
- [ ] Commands and their purpose explained
- [ ] Actual outputs reviewed
- [ ] Data-plane outcome measured where applicable
- [ ] Limitations and recovery documented

Use the [lab template](../LAB-TEMPLATE.md). Publish only reviewed lab data.
