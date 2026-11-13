# LAB 03 — Bidirectional PIM and Designated Forwarders

## Objective and setup

Use one bidirectional shared tree for **239.2.2.2**, anchored at RP address **10.255.0.2** on RR-P. CE1 and CE3 were used as sources. The user reported both source tests; the stored counters are not individually labeled by source.

![BIDIR lab topology](topology/multicast-eve-ng.png)

## Mechanism

BIDIR-PIM forwards traffic along a shared (*,G) tree rather than creating a separate SPT for each source. A designated forwarder is elected on a link to control upstream forwarding toward the RP address and prevent duplicate forwarding/loops. It does not use PIM Register. See [RFC 5015](https://www.rfc-editor.org/rfc/rfc5015.html).

Consequently, a source count of zero in the captured BIDIR group display is compatible with forwarding traffic; it is not evidence that no sender exists.

## Configuration and purpose

```cisco
ip pim bidir-enable
ip pim rp-address 10.255.0.2 BIDIR_GROUPS bidir
ip access-list standard BIDIR_GROUPS
 permit 239.2.2.2
! RR-P uses Loopback1 10.255.0.2/32.
! Receiver interfaces on CE2/CE3:
ip igmp join-group 239.2.2.2
```

The global command enables BIDIR support. The RP mapping marks this group as bidirectional. Keep PIM and unicast reachability on the participating interfaces; the RP address must be reachable.

## Commands, results and explanation

```cisco
show ip pim interface df
show ip mroute 239.2.2.2
show ip mroute count
```

| PE2 evidence | Interpretation |
|---|---|
| (*,239.2.2.2), RP 10.255.0.2, flags BC | Shared bidirectional group state |
| Bidir-Upstream Fa0/0; RPF neighbor 10.0.23.1 | Upstream direction is toward RR-P |
| IIL includes Fa1/0 and Fa0/0, Accepting/Sparse | Captured accepted incoming-interface state |
| OIL includes Fa1/0 Forward/Sparse and Fa0/0 Bidir-Upstream/Sparse | Receiver-facing and upstream roles coexist in the BIDIR display |
| Fa0/0 DF = RR-P (10.0.23.1) | RR-P wins on that link |
| Fa1/0 DF = PE2 (*10.0.2.1) | PE2 is the DF on the CE-facing link |
| Source count 0; RP-tree counters 14→15→17 | Packets advance on the shared tree without per-source SPT state |

Do not apply ASM's expectation of a new (S,G) SPT to BIDIR. The absence of such state is part of the model being tested.

## Troubleshooting and limits

Check group-to-RP mapping, RP reachability and DF election before interpreting counters. A wrong DF/upstream direction can affect forwarding even when membership exists. BIDIR alone does not establish automatic RP high availability.

The evidence supports shared-tree forwarding and DF roles. It does not measure per-source throughput, prove an RP failover, or isolate one labeled counter series for each sender.

[Complete evidence and repeated raw captures](evidencias/LAB03_PIM_BIDIR.txt)
