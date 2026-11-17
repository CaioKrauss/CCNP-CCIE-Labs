# LAB 14 — LFA / TI-LFA with IS-IS

**My goal:** protect the preferred XR1-to-XR2 path and compare repair behavior with the alternative link.

**Result documented here:** partial evidence — per-prefix FRR and TI-LFA configuration is present on XR1. Repair installation, activation and measured convergence are not recoverable from the available chat excerpts.

## My topology

The shared snapshot has two XR1–XR2 links: Gi0/0/0/0 with IS-IS metric 10 and Gi0/0/0/2 with metric 100. See the [LAB 13 topology](LAB13-SR-TE-IOSXR.md).

## What I configured

XR1's committed configuration contains:

```cisco
router isis CORE
 interface GigabitEthernet0/0/0/0
  point-to-point
  address-family ipv4 unicast
   fast-reroute per-prefix
   fast-reroute per-prefix ti-lfa
   metric 10
```

The collected XR2 configuration has no corresponding FRR directives. This snapshot therefore does not establish symmetric protection.

## What I observed

| Check | Evidence available |
|---|---|
| Per-prefix FRR / TI-LFA enabled | Confirmed in XR1 running-config |
| Alternate link configuration | Present on both XRs |
| Computed backup / repair labels | Operational output unavailable |
| Failure, repair and recovery | Historical test output unavailable |
| Loss / convergence time | No measured result available |

## What I learned

Enabling FRR is one step; a programmed repair and its behavior during a failure require separate evidence. The final configuration alone cannot establish whether an earlier repair used LFA or TI-LFA.

**Limit:** “partial evidence” is a documentation status, not a claim that the test failed. I have not assigned a sub-50-ms result, a repair stack, or a success rate without the original outputs.

**Evidence:** [Shared XR configs](configs/LABS12-16-2026-11-17/README.md) · [Collection and coverage](evidencias/LABS12-16-2026-11-17/COLLECTION-AND-COVERAGE.md).
