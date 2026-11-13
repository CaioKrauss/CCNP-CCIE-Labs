# Integrated Troubleshooting

## Scope and status

Structured diagnosis across IGP, BGP, MPLS, multicast, QoS, IPv6 and security.

**Planned study area: no completed feature-specific lab or measured result is claimed here.**

## Core question

Which observation distinguishes a control-plane fault from a forwarding-plane fault?

## What a useful result must show

Start with the exact failed traffic tuple, follow the path, test one hypothesis at a time and verify recovery. Avoid changing several variables simultaneously.

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
