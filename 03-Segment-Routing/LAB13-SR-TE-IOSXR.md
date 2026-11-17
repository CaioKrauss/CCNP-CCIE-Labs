# LAB 13 — SR Traffic Engineering

**My goal:** steer traffic from XR1 to XR2 over the alternative link with an explicit SR policy.

**Result documented here:** partial evidence — the committed policy and steering configuration are preserved. The operational results from the earlier chat turns were not returned during this documentation update, so policy UP, actual steering and packet delivery are not marked as validated.

## My topology

```text
XR1 1.1.1.1 ===== Gi0/0/0/0: 10.0.12.0/30, metric 10 ===== XR2 2.2.2.2
            ===== Gi0/0/0/2: 10.0.12.4/30, metric 100 =====
```

Both routers run IOS XR 6.3.1. The alternative interface addresses are 10.0.12.5 and 10.0.12.6.

## What I configured

XR1's collected configuration contains:

```cisco
segment-routing
 traffic-eng
  segment-list name LINK-ALTERNATIVO
   index 10 mpls label 24004
  policy SRTE-XR2
   color 100 end-point ipv4 2.2.2.2
   candidate-paths
    preference 100
     explicit segment-list LINK-ALTERNATIVO
```

The snapshot also retains color 100 policies for global prefix 172.20.2.1/32 and VPN prefix 172.20.200.2/32. Both XRs have VRF `SRTE-LAB`, RT 65000:100 and VPNv4 neighbor configuration. XR1 applies `IBGP-XR2-BASE` to IPv4 input and `SRTE-COLOR-VPN` to VPNv4 input.

## What I observed

| Check | Evidence available |
|---|---|
| Policy / segment list | Present in committed XR1 running-config |
| Alternative link | Configured on both XRs with IS-IS metric 100 |
| Color / VPN configuration | Present; operational route color and resolution not captured here |
| Policy state / BSID / forwarding | Earlier operational outputs unavailable |
| Traffic steering / delivery | No recoverable test output in this collection |

## What I learned

I need both policy state and forwarding evidence to establish that the alternative link carried the traffic. A configured explicit label alone is not that proof.

**Limit:** do not replay label 24004 without checking its current local meaning. In LAB 12's earlier XR1 LFIB it identified an LDP FEC for 3.3.3.3/32; the later SR-TE configuration uses the same number, but its contemporaneous LFIB is missing. I cannot infer label identity across snapshots or infer a platform defect from missing evidence.

**Evidence:** [XR1/XR2 snapshot](configs/LABS12-16-2026-11-17/README.md) · [Coverage and missing evidence](evidencias/LABS12-16-2026-11-17/COLLECTION-AND-COVERAGE.md).

**Snapshot status (2026-11-17 update):** the linked 05:23 UTC backup is historical, not a verified final/current restore point. Updated running-configs are requested; missing intermediate operational evidence remains pending.
