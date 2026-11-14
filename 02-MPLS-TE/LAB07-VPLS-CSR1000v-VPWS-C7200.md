# LAB 07 — VPLS bridging on CSR1000v with a Cisco 7200 VPWS spoke

**Live collection:** 14 November 2026, starting 18:25–18:26 America/Sao_Paulo, followed by forwarding tests. **Source:** EVE-NG `VPLS.unl`, six running nodes. R1 is CSR1000v IOS XE 16.12; R2 and the four CEs are Cisco 7200 IOS 15.2. These are fresh console captures, not LAB06 backups.

**Result:** four customer sites communicate through bridge-domain 100. R1 VFI `VPLS100` and R2 VC 100 are UP; LDP is Oper. All 12 directed CE pairs reached 10/10 replies, with three pairs requiring a repeat after an initial 9/10. No configuration changes, saves or reloads were performed.

## Topology and addressing

```text
L2_CE2 Fa0/0 (.2/24) ---- Gi3
L2_CE3 Fa0/0 (.3/24) ---- Gi2  R1 CSR1000v
L2_CE4 Fa0/0 (.4/24) ---- Gi1  BD100 + VFI VPLS100
                                  Gi4 10.0.0.1/30
                                   |
                                  Fa1/0 10.0.0.2/30
                              R2 Cisco 7200
                                  Fa0/0 xconnect VC100
                                   |
                              L2_CE1 Fa0/0 (.1/24)

CE subnet: 192.168.100.0/24
PW endpoints: R1 Lo0 1.1.1.1/32 <--> R2 Lo0 2.2.2.2/32
```

The port map follows the collected interface descriptions and service configuration. CDP did not independently confirm the wiring: R1 reports CDP disabled, and the other neighbor outputs are empty. Connectivity and MAC learning provide operational corroboration.

The underlay is a direct R1–R2 link with static routes to the remote loopback and `mpls ip`; this lab does not use the LAB06 R3/IS-IS transit path. R1 bridges three local untagged attachment circuits and one pseudowire. R2 uses a point-to-point xconnect for CE1; it does not have a multipoint VFI. This is a VPLS bridge with a VPWS access spoke, not a tested multi-PE VPLS full mesh.

## Configuration relationships

The complete reviewed snapshots are in [configs/LAB07-VPLS-2026-11-14](configs/LAB07-VPLS-2026-11-14/), one file per hostname. The following excerpts are from those live captures.

R1 connects the VFI and Ethernet service instances to the same bridge-domain:

```cisco
l2vpn vfi context VPLS100
 vpn id 100
 member 2.2.2.2 encapsulation mpls
!
bridge-domain 100
 member GigabitEthernet1 service-instance 100
 member GigabitEthernet2 service-instance 100
 member GigabitEthernet3 service-instance 100
 member vfi VPLS100
!
interface GigabitEthernet3
 description VPLS-TO-L2_CE2
 no ip address
 negotiation auto
 no mop enabled
 no mop sysid
 service instance 100 ethernet
  encapsulation untagged
```

Gi1 and Gi2 use the same service-instance/untagged pattern. R2 supplies the remote Ethernet circuit:

```cisco
interface FastEthernet0/0
 description VPWS-TO-L2_CE1
 no ip address
 duplex full
 no keepalive
 xconnect 1.1.1.1 100 encapsulation mpls
```

## Evidence from this collection

| Check | Observed result |
|---|---|
| R1 `show bridge-domain 100` | UP; MAC learning enabled; three EFPs and one VFI neighbor |
| R1 `show l2vpn vfi` | VPLS100 UP, multipoint, LDP, VPN ID 100; peer 2.2.2.2 VC 100 |
| R1/R2 `show mpls ldp neighbor` | Oper; link discovery and targeted hellos |
| R2 `show mpls l2transport vc detail` | VC 100 UP to 1.1.1.1; Fa0/0 up/up; MTU 1500/1500 |
| Encapsulation | Service labels local/remote 16/16; imposed stack `{16}`; Control Word On, autosense; sequencing disabled |
| R2 VC counters before → after tests | Receive 49 → 112; send 122 → 191; receive/sequence/send drops remained 0 |
| ARP | All four CE tables contain the other three CE IP/MAC mappings after the tests |

Counters include any other traffic during the interval; their deltas are not an exact count of the test ICMP packets.

### Learned MAC locations on R1

| Site | MAC | Learned location |
|---|---|---|
| L2_CE1 | CA06.14C7.0000 | VPLS100.404013 (remote PW) |
| L2_CE2 | CA02.0DD6.0000 | GigabitEthernet3.EFP100 |
| L2_CE3 | CA03.0D84.0000 | GigabitEthernet2.EFP100 |
| L2_CE4 | CA04.0D32.0000 | GigabitEthernet1.EFP100 |

### Directed ping matrix

Each command used an explicit source, `repeat 10 timeout 1`, with 100-byte ICMP echoes. Cells show first attempt, then repeat where performed.

| Source → destination | CE1 | CE2 | CE3 | CE4 |
|---|---|---|---|---|
| CE1 | — | 10/10 | 10/10 | 10/10 |
| CE2 | 10/10 | — | 9/10 → 10/10 | 9/10 → 10/10 |
| CE3 | 10/10 | 10/10 | — | 9/10 → 10/10 |
| CE4 | 10/10 | 10/10 | 10/10 | — |

The three initial misses are consistent with neighbor resolution, but no packet capture established their cause. They remain in the published transcripts.

## Saved configuration and boot state

`terminal length 0` was issued before collection. Each running/startup capture contains the configuration through `end` and the expected hostname prompt. Comparison ignores comments, blank lines and trailing spaces.

| Device | Running vs startup | Configuration register |
|---|---|---|
| R1 | Same effective commands outside PKI certificate storage representation | 0x2102 |
| R2 | Matching effective commands | 0x2142; will be 0x2102 at next reload |
| L2_CE1 | Matching effective commands | 0x2142; will be 0x2102 at next reload |
| L2_CE2 | Matching effective commands | 0x2142; will be 0x2102 at next reload |
| L2_CE3 | Matching effective commands | 0x2142; will be 0x2102 at next reload |
| L2_CE4 | Matching effective commands | 0x2142; will be 0x2102 at next reload |

R1 running displays inline certificates; startup references `nvram:IOS-Self-Sig#1.cer` and `nvram:CiscoLicensi#1CA.cer`. `dir nvram:` confirms both files exist. Certificate bytes were not compared. The VPLS/service commands are already saved. The next-boot register correction was present before collection; no register was changed here. Persistence is verified from saved state, not by a reboot test.

## What the bridge does

R1 learns source MACs and looks up destination MACs. Known unicast follows the learned port; broadcasts and unknown unicasts are flooded to eligible members other than the ingress, subject to split-horizon. VPLS pseudowire split-horizon prevents forwarding between mesh pseudowires. There is only one PW in this lab, so that behavior was not exercised. See [RFC 4762](https://www.rfc-editor.org/rfc/rfc4762).

The MAC table and successful pings support forwarding between the four sites. They do not independently prove per-frame flooding behavior, multicast snooping, maximum MTU, performance, failover or multi-PW split-horizon.

## Repeat the checks

```cisco
! R1
terminal length 0
show bridge-domain 100
show l2vpn vfi
show mpls ldp neighbor
! R2
show mpls l2transport vc detail
! Every device
show running-config
show startup-config
show version | include Configuration register
! Example on CE2
ping 192.168.100.1 source 192.168.100.2 repeat 10 timeout 1
show ip arp
```

Check interfaces and loopback reachability first, then LDP/PW state and MTU, bridge-domain membership, learned MACs, ARP and bidirectional forwarding.

## Files and sanitization

- [Six hostname-based running snapshots](configs/LAB07-VPLS-2026-11-14/).
- [Six startup snapshots, console transcripts and collection manifest](evidencias/LAB07-VPLS-2026-11-14/).
- [Collection metadata and hashes](evidencias/LAB07-VPLS-2026-11-14/manifest.json).

Full original captures remain local. Published R1 captures replace certificate hex payloads and the license UDI serial with explicit redaction markers; no service configuration was invented or substituted. Full `show version` stays local; published transcripts contain its configuration-register excerpt. No credential-bearing configuration directives were found in these six snapshots. The EVE login credentials are not included. Sanitized snapshots are study records, not guaranteed paste-ready restores of device identity/PKI. LAB06 files remain unchanged.
