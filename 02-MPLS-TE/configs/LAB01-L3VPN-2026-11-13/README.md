# My L3VPN CUST-A Configuration Capture

I collected these from the device consoles on **2026-11-13, around 15:43 (Brazil)**, without applying new configuration.

- **IOS:** running/startup snapshots of CE1_A, CE2_A, R1 and R3. Their effective commands matched.
- **IOS XR:** XR1 running-config and existing commit history; I did **not** test persistence after reboot.
- The nine files contain my tested CUST-A path, not CE1_B/CE2_B or the later L2VPN lab.
- I removed console prompts/collection headers; I did not modify service commands.
- I reviewed the published files for secrets. Loopbacks using public IPv4 values belong **only** in the isolated lab.

My router responses are in the [CLI evidence folder](../../evidencias/LAB01-L3VPN-2026-11-13/), with the associated `SHA256SUMS.txt`. These config files show what was configured; my ping/traceroute results are documented separately in [LAB 01](../../LAB01-L3VPN-ISIS-LDP-IOS-XR.md).
