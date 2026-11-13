# LAB 01 — PIM Sparse Mode, ASM and a Static RP

## Objective and evidence status

Explain how group membership creates a shared tree and how a source-specific tree appears. Group: **239.1.1.1**. RP: **RR-P, 10.255.0.1**. Source: CE1, using **10.255.0.11** or **10.0.1.1** in different captures. Receivers: CE2/CE3.

Historical console evidence shows membership and forwarding state. It does not include comparable end-receiver delivery counters for this group.

![Shared multicast lab topology](topology/multicast-eve-ng.png)

See [interface addressing](topology/enderecamento.md). Traffic crosses PE1 and RR-P before branching toward the receivers.

## Mechanism

A receiver requests group G through IGMP. Its last-hop router sends a PIM (*,G) Join toward the RP. The source-side designated router can encapsulate initial traffic in PIM Registers to the RP. Receivers may subsequently use a source-specific shortest-path tree. These are control-plane steps; each still requires a usable data path. See [RFC 7761](https://www.rfc-editor.org/rfc/rfc7761.html).

In this physical tree, the shared and source-specific paths can use the same interfaces. An SPT transition does not require the diagram to show a different cable.

## Configuration and purpose

Observed excerpts, not a complete paste-ready configuration:

```cisco
ip multicast-routing
ip pim rp-address 10.255.0.1 ASM_GROUPS
ip access-list standard ASM_GROUPS
 permit 239.1.1.1
! On participating interfaces:
ip pim sparse-mode
! Receiver interface in the initial capture:
ip igmp join-group 239.1.1.1
```

| Command | Purpose |
|---|---|
| ip multicast-routing | Enables IPv4 multicast routing |
| ip pim sparse-mode | Enables PIM on that interface |
| ip pim rp-address ... ASM_GROUPS | Maps the selected ASM group to the static RP |
| ip igmp join-group | Makes the router itself a local receiver for the test |

The snapshot may contain extra groups or later membership changes. Use the lab-specific evidence to reconstruct the historical step.

## Verify and interpret

| Command | Observed result | Why it matters |
|---|---|---|
| show ip igmp groups | CE2 subscribed to 239.1.1.1 | Confirms local receiver interest |
| show ip pim rp mapping | Inspect the group-to-RP mapping | A mismatched RP can send joins toward the wrong tree |
| show ip mroute 239.1.1.1 | PE2 (*,G): SJC; IIF Fa0/0, RPF neighbor 10.0.23.1; OIL Fa1/0 | The tree points upstream to RR-P and downstream to CE2 |
| show ip mroute 239.1.1.1 | PE2 (10.255.0.11,G) includes T | IOS reports the SPT bit set for that entry |
| show ip rpf 10.255.0.11 | Check the source-facing interface | Multicast arriving on the wrong RPF interface can be rejected |
| show ip mroute count | Compare counters while sending traffic | Needed to strengthen a forwarding claim beyond installed state |

```cisco
show ip pim neighbor
show ip pim rp mapping
show ip igmp groups
show ip mroute 239.1.1.1
show ip rpf 10.255.0.11
show ip mroute count
```

**Do not equate (S,G) with a proven end-to-end SPT transition.** The T flag is the relevant IOS state indicator here; compare IIF/OIL and counters across routers. CE2's null OIL is compatible with local reception: the router need not forward the packet to another interface to consume it.

## Troubleshooting and conclusion

If membership exists but the tree does not, inspect PIM neighbors and RP mapping. If the tree exists but counters do not advance, inspect source address, RPF and outgoing interfaces. Do not diagnose a physical reroute on this single-path topology.

The captures establish ASM membership, shared/source state and the IOS SPT indication. End-receiver delivery still needs its own measured evidence.

[Original command output with English annotations](evidencias/LAB01_PIM_SM_ASM.txt) · [Combined final IPv4 snapshot](configs/snapshot-2026-11-12/)
