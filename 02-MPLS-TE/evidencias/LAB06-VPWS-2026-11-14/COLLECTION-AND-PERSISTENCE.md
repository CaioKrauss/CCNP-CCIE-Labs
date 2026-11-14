# LAB 06 — Collection and persistence evidence (14 Nov 2026)

Source: user-provided archive `20261114-165756.rar`, collected at 16:57–16:58 (America/Sao_Paulo).

| Router | Running-config backup | Evidence of saved state | Outcome |
|---|---|---|---|
| R1 | yes | `write memory`; startup.cfg matches running.cfg byte-for-byte | confirmed |
| R2 | yes | `write memory`; startup.cfg matches running.cfg byte-for-byte | confirmed |
| R3 | yes | `write memory`; startup.cfg matches running.cfg byte-for-byte | confirmed |
| XR1 | yes | IOS XR active committed configuration; last listed commit ID 1000000023 | no new commit requested or performed |
| L2_CE1 | yes | collection was read-only; no post-save startup comparison | **not confirmed** |
| L2_CE2 | yes | collection was read-only; no post-save startup comparison | **not confirmed** |

Important: the RAR also contained CE1_A, CE2_A and unresponsive CE1_B/CE2_B consoles belonging to the earlier L3VPN topology. Those are **not** included in the LAB06 set, because the user requested the boxes used in the L2VPN lab.

The final XR1 running config **does not have an active L2VPN xconnect**, and Gi0/0/0/1 is shutdown, reflecting the return to the preserved L3VPN baseline. The earlier XRv xconnect-UP outputs are historical diagnostic evidence, not the archived configuration state.

The attached archive and outputs were inspected for credential-bearing configuration directives (passwords, secrets, SNMP communities, authentication keys and certificates). None were observed in these six lab configurations. This is an isolated lab; the IPv4 loopbacks 1.1.1.1 and 3.3.3.3 are not RFC 5737 documentation addresses and should not be announced to the Internet.

Some archive operation transcript files contain console interactions and timestamps; this publication preserves only the essential three save transcripts, three identical startup snapshots, six running-config snapshots and validated diagnostic excerpts.
