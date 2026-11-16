# My Network Automation Notes

I use automation to collect configurations **consistently**, not to assume a successful connection means a complete capture.

## Utility I already have

- [Cisco IOS console backup guide](backup-show-run-eve.md)
- [Python source](backup_show_run_eve.py)

The script connects to selected EVE-NG Telnet consoles, disables paging, runs `show running-config` and checks for an output terminator/prompt before saving. I review the resulting files before publishing them.

**Scope:** this script targets the original seven-router IOS multicast lab. It is **not** the IOS XR collector, and I have not used this file to validate NETCONF, RESTCONF or Ansible.

## What I plan to study

I still want to test YANG models, NETCONF/RESTCONF, Ansible and automated validation. Each future lab needs a real execution and captured result.

[My lab template](../LAB-TEMPLATE.md).
