# Quality of Service

## Scope and status

Classification, marking, queuing, WRED, shaping, policing and MPLS traffic class.

**Planned study area: no completed feature-specific lab or measured result is claimed here.**

## Core question

Which traffic is matched, how is congestion handled, and where are packets delayed or dropped?

## What a useful result must show

Compare offered load, class counters, queue/drop statistics and application behavior. A policy attached to an interface does not prove it matches the intended traffic.

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
