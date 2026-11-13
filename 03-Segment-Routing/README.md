# Segment Routing

## Scope and status

SR-MPLS, segment identifiers, SR-TE, TI-LFA and SRv6.

**Planned study area: no completed feature-specific lab or measured result is claimed here.**

## Core question

How does a segment list select a path, and how is that path resolved in the forwarding plane?

## What a useful result must show

Compare the intended segment list with the installed policy and a measured packet path. A configured policy alone does not establish that traffic uses it.

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
