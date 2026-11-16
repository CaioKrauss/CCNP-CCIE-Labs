# My Multicast Configuration Snapshots

I collected seven Cisco IOS running configs (CE1–CE3, PE1–PE3 and RR-P).

| Snapshot | What I captured | Important limit |
|---|---|---|
| [2026-11-12](snapshot-2026-11-12/) | Final combined **IPv4** state after LABs 01–04 | Not every intermediate experiment |
| [2026-11-13](snapshot-2026-11-13/) | **IPv6/OSPFv3**, ASM/SSM joins and earlier IPv4 config | Running state, not a startup/reboot test |

I use these to check the *configured* baseline and [the original CLI evidence](../evidencias/) to explain *what happened* during each lab.

**Reminder:** RR-P was a PIM RP / transit node here; its name does **not** imply a configured BGP route reflector. I review every capture for secrets before publishing it.

[Addressing](../topology/enderecamento.md) · [Backup utility](../../09-Automation/backup-show-run-eve.md).
