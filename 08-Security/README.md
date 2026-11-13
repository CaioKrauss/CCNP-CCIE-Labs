# Network Security

## Scope and status

CoPP, uRPF, ACLs, DHCP snooping, dynamic ARP inspection and AAA.

**Planned study area: no completed feature-specific lab or measured result is claimed here.**

## Core question

Which traffic or access is permitted, and can the intended protection be verified without disrupting legitimate traffic?

## What a useful result must show

Use explicit positive and negative cases with counters/logs. A configured rule is not evidence that the intended packet matched it.

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
