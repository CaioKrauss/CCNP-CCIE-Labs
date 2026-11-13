# Network Automation

## Scope and status

Python, NETCONF/YANG, RESTCONF, Ansible and configuration validation.

**Planned study area: no completed feature-specific lab or measured result is claimed here.** A local IOS backup utility is already available; see below.

## Core question

Can collection or validation be repeated reliably while distinguishing complete output from errors?

## What a useful result must show

Validate command-response alignment, complete captures and explicit failures before trusting automated results.

## Planned workflow

1. Select the exact platform/image and document prerequisites.
2. Add the topology and addressing.
3. Explain each configuration command and its intended effect.
4. Record platform-specific verification commands, actual output and interpretation.
5. Run bounded traffic tests and, if appropriate, a separately authorized failure/recovery test.

Commands will be tied to a concrete platform when the lab is built; no universal cross-platform syntax or invented output is supplied.

## Available utility

- [IOS console backup guide](backup-show-run-eve.md)
- [Python source](backup_show_run_eve.py)

The utility is a collection aid, not proof of NETCONF/RESTCONF/Ansible validation.

## Completion checklist

- [ ] Topology and baseline captured
- [ ] Commands and their purpose explained
- [ ] Actual outputs reviewed
- [ ] Data-plane outcome measured where applicable
- [ ] Limitations and recovery documented

Use the [lab template](../LAB-TEMPLATE.md). Publish only reviewed lab data.
