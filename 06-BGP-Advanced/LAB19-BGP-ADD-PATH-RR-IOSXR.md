# LAB 19 — BGP ADD-PATH + Route Reflection

## What I learned

I verified that XR1 can advertise its non-best AS65101 path to XR2 while still preferring AS65102. XR2 keeps both BGP paths but forwards through R2. Historical failure and recovery outputs show the selected next-hop changing to XR1 and back to R2. They do not measure convergence speed.

## Topology and actual configuration

```text
R1 (AS65101) — XR1 (AS65000, RR) — XR2 (AS65000, client) — R2 (AS65102)
3.3.3.3         1.1.1.1             2.2.2.2                4.4.4.4
```

Test prefix: **198.51.100.0/24**, originated on both IOS edges with a static Null0 route and a BGP network statement. XR1–R1 uses 10.0.13.2/30 ↔ 10.0.13.1/30; XR2–R2 uses 10.0.24.1/30 ↔ 10.0.24.2/30. The XR loopbacks peer over the existing IS-IS/SR transport.

[Full current configurations and persistence](configs/LAB19-ADD-PATH-RR-2026-11-18/README.md) were collected on November 18, 2026, 16:36–16:37 São Paulo (19:36–19:37 UTC). XR configuration headers identify IOS XR 6.3.1; IOS headers identify version 15.2.

Key excerpts from the current configuration (not a complete deployment template):

```cisco
! XR1
route-policy LAB19-ADDPATH
  set path-selection all advertise
end-policy
!
router bgp 65000
 address-family ipv4 unicast
  additional-paths send
  additional-paths selection route-policy LAB19-ADDPATH
 !
 neighbor 2.2.2.2
  remote-as 65000
  update-source Loopback0
  address-family ipv4 unicast
   route-policy IBGP-XR2-BASE in
   route-reflector-client
   route-policy PASS-ALL out
   next-hop-self
```

```cisco
! XR2
router bgp 65000
 address-family ipv4 unicast
  additional-paths receive
```

XR2's inbound policy from R2 sets LOCAL_PREF 200 for the prefix. The R1 path retains LOCAL_PREF 100 and community 65101:200. The previously defined PIC-EDGE-TEST policy remains in XR1's configuration but is not the active additional-paths selection policy.

**Correction to an earlier chat suggestion:** neither collected running-config contains a neighbor-level `capability additional-paths` statement, yet operational output explicitly confirms Send/Receive for IPv4 Unicast. The collected configuration is authoritative for this lab/version; no suggested command was inserted into the backup. VPNv4 shows operation None.

## RR, path hiding and Path ID

A Route Reflector reduces the need for a full iBGP mesh. Originator ID and Cluster List help prevent reflection loops. This lab has one RR and one client: it verifies the client relationship and additional-path advertisement, not multi-client or multi-cluster reflection.

With ordinary best-only advertisement, an alternate path can remain hidden from other routers. Here XR1 prefers the route learned from XR2; returning that same path to its originator is not the objective. ADD-PATH allows XR1 to advertise the eligible R1 alternative instead.

The recovered LAB19 history starts after configuration at 19:29. A precise pre-ADD-PATH LAB19 raw baseline is not available. The [earlier LAB18 XR2 capture](evidencias/LAB18-BGP-PIC-2026-11-18/XR2-live-cli.txt) shows only AS65102 at 19:14:29; it is contextual evidence, not a controlled before/after RR test.

ADD-PATH identifies a path using the prefix plus a sender-assigned 32-bit Path Identifier. The number is not a preference, AS number, hop count or global identifier. XR1 Local Path ID 3 matches XR2 Received Path ID 3 in the current session. Historical values 2 → 0 → 3 must be preserved as observed, not rewritten or interpreted as preference changes. A displayed zero alone does not establish that ADD-PATH is disabled.

## Evidence and sequence

All router timestamps below are UTC on November 18, 2026. Historical files preserve user-supplied CLI from conversation 6afbb8c6-3b30-83e8-ab14-6be459107b14; live files are direct console captures.

| Stage | Observed result | Source |
|---|---|---|
| 19:29:33 configuration excerpt | XR1 RR-client and additional-paths selection configured | [Historical configuration](evidencias/LAB19-ADD-PATH-RR-2026-11-18/history-655bce15-8b06-44c1-ab29-055fed7f83ab.txt) |
| 19:30:20–30 negotiation | XR1 Send; XR2 Receive. XR1 AS65101 marked add-path and advertised to 2.2.2.2; Local/Received Path ID 2 | [Negotiation and paths](evidencias/LAB19-ADD-PATH-RR-2026-11-18/history-f7abd30f-351f-4111-8379-91d4fdd6049b.txt) |
| 19:32:50–51 failover state | XR2 only AS65101, best via 1.1.1.1; RIB internal distance 200; CEF resolves through Gi0/0/0/0 → 10.0.12.1 | [Failure-stage CLI](evidencias/LAB19-ADD-PATH-RR-2026-11-18/history-b6b71504-b5f7-4dde-ad89-3f15d3913e00.txt) |
| 19:33:53 recovery | XR2 two paths; AS65101 Received Path ID 3; AS65102 LOCAL_PREF 200 best; CEF Gi0/0/0/1 → 10.0.24.2 | [Recovery CLI](evidencias/LAB19-ADD-PATH-RR-2026-11-18/history-8bb1e086-fcb7-45ce-9309-5b12e0257087.txt) |
| 19:37 current state | Send/Receive and AS65101 announcement reconfirmed; XR2 still has two paths with ID 3 and forwards via R2 | [XR1 live](evidencias/LAB19-ADD-PATH-RR-2026-11-18/XR1-live-cli.txt), [XR2 live](evidencias/LAB19-ADD-PATH-RR-2026-11-18/XR2-live-cli.txt) |

The historical procedure called for shutdown/no shutdown of XR2's eBGP neighbor 10.0.24.2 with commit. The supplied raw evidence captures the resulting states, not the shutdown commands themselves. No failure was injected again during this collection.

## ADD-PATH vs multipath vs PIC

| Feature | Purpose | What this lab establishes |
|---|---|---|
| ADD-PATH | Advertise additional BGP paths to a capable receiver | Negotiated Send/Receive plus actual non-best path advertisement |
| Multipath / ECMP | Install multiple eligible active forwarding paths | Not observed: two BGP paths, one active CEF exit |
| PIC | Prepare alternate forwarding state for fast convergence | No PIC timing claim; additional BGP visibility alone does not prove installed backup or fast failover |

## Commands to review

```cisco
! XR1
show running-config
show configuration commit list
show bgp neighbors 2.2.2.2
show bgp ipv4 unicast 198.51.100.0/24
! XR2
show running-config
show configuration commit list
show bgp neighbors 1.1.1.1
show bgp ipv4 unicast 198.51.100.0/24
show route 198.51.100.0/24
show cef ipv4 198.51.100.0/24 detail
! R1 / R2 (IOS)
show running-config
show ip bgp summary
show ip bgp 198.51.100.0
write memory
show startup-config
```

## Persistence and limits

- XR1/XR2: empty candidate checked, commit executed, both returned `No configuration changes to commit.` Existing running state was already committed; no new commit ID was created.
- R1/R2: write memory returned [OK]; startup and running configurations matched exactly.
- All four running configurations were unchanged before/after saving; six configuration files and hashes are included.
- No reboot test, packet-loss measurement, convergence timing or controlled pre-ADD-PATH comparison was performed.
- CEF/RIB changes establish forwarding-table recovery, not uninterrupted packet delivery. The test prefix terminates in Null0 at the edges.
- Multi-client RR reflection and cluster-loop tests remain future work.

References: [RFC 7911 — ADD-PATH](https://www.rfc-editor.org/rfc/rfc7911.html), [Cisco — IOS XR path selection](https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/217097-bgp-path-selection-in-ios-xr.html). Documentation explains the concepts; device outputs establish this lab's behavior.
