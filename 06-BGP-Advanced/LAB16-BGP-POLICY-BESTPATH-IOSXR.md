# LAB 16 — Advanced BGP Policy and Best Path

**My goal:** compare BGP attributes and observe how a policy on XR1 changes the route selected by XR2.

**Result:** the retrieved CLI validates community reception, LOCAL_PREF 200, propagation through iBGP and the final RIB choices. A MED test state is also preserved. Earlier AS-PATH prepending and MED before/after steps are reported in the chat summary but their raw outputs were not returned.

## My topology

```text
R1 AS 65101 ----- XR1 AS 65000 ===== iBGP ===== XR2 AS 65000 ----- R2 AS 65102
  10.0.13.1    10.0.13.2 / 1.1.1.1          2.2.2.2 / 10.0.24.1    10.0.24.2
```

The tested prefix is **198.51.100.0/24**. The XRs run IOS XR 6.3.1. Their iBGP sessions use Loopback0 and next-hop-self; R1/R2 full running configs are missing.

## What I configured

The historical XR1 snapshot contains:

```cisco
community-set LAB16-COMMUNITY
  65101:200
end-set
route-policy EBGP-R1-IN
  if community matches-any LAB16-COMMUNITY then
    set local-preference 200
  endif
  pass
end-policy
```

This policy is applied inbound to neighbor 10.0.13.1 in IPv4 unicast. The active IPv4 input policy on the XR2 iBGP neighbor is `IBGP-XR2-BASE`; the retained `IBGP-XR2-IN` definition is not attached there. I do not treat every retained policy definition as active.

## What I observed

All times below are UTC on 2026-11-17.

| Capture | My real result |
|---|---|
| XR1 05:16:32 | Two paths, equal LOCAL_PREF 100; AS 65102 via iBGP has MED 0 and is best; AS 65101 via eBGP has MED 500 |
| XR1 05:16:33 RIB | Internal BGP route via 2.2.2.2, distance 200, tag 65102 |
| XR1 05:18:35 | Community 65101:200 received; LOCAL_PREF still 100; eBGP AS 65101 is best |
| XR1 05:19:57 | One available path: AS 65101, community 65101:200, LOCAL_PREF **200**, external best |
| XR1 05:20:06 RIB | External BGP route via 10.0.13.1, distance **20** |
| XR2 05:21:11 | Two paths: iBGP via 1.1.1.1 has LOCAL_PREF **200** and wins over eBGP via 10.0.24.2 with LOCAL_PREF 100 |
| XR2 05:21:13 RIB | Internal BGP route via 1.1.1.1, distance **200**, tag 65101 |

XR2 marks its AS 65102 path “Not advertised to any peer”; XR1 shows only one available path. Together these support the recorded best-path/path-hiding observation with ordinary iBGP. This was not a route-reflector test.

## What I learned

The community was visible before LOCAL_PREF changed. The later configuration and outputs show the policy translating it into LOCAL_PREF 200 and influencing XR2's selected route.

The chat attributes the earlier MED result to cross-AS MED comparison. The output preserves the resulting attributes and RIB choice, but the enabling command and baseline output are absent from the recovered evidence. The historical snapshot no longer includes `bgp bestpath med always`.

**Limit:** no BGP ECMP/multipath, Add-Path, PIC, route-reflector behavior, traffic-delivery test or timed failover is claimed. AS-PATH prepending remains reported-only until its original CLI is recovered. `Origin-AS validity: not-found` is preserved as output, not a claim of a completed RPKI lab.

**Evidence:** [Chronological CLI captures](evidencias/LAB16-BGP-2026-11-17/CLI-OBSERVED.md) · [Historical shared XR configs](../03-Segment-Routing/configs/LABS12-16-2026-11-17/README.md) · [Temporal coverage](../03-Segment-Routing/evidencias/LABS12-16-2026-11-17/COLLECTION-AND-COVERAGE.md).

**Snapshot status (2026-11-17 update):** the linked 05:23 UTC backup is historical, not a verified final/current restore point. Updated running-configs are requested; missing intermediate operational evidence remains pending.
