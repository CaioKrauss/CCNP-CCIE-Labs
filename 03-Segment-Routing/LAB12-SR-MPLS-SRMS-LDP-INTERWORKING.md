# LAB 12 — SR-MPLS / LDP Interworking with SRMS

**My goal:** connect LDP-only edge routers through an SR-MPLS core, using XR1 as the SR Mapping Server.

**Result:** validated SID distribution, LFIB interworking and **20/20 loopback pings in each direction**. Captures are from 2026-11-17 02:02–02:05 UTC (2026-11-16 23:02–23:05 in São Paulo).

## My topology

```text
R1 3.3.3.3 -- LDP -- XR1 1.1.1.1 -- SR -- XR2 2.2.2.2 -- LDP -- R2 4.4.4.4
            10.0.13.0/30        10.0.12.0/30         10.0.24.0/30
```

The XRs run IOS XR 6.3.1. R1/R2 use IOS CLI; their full running configs and version outputs were not included in this collection. This capture predates the second XR-to-XR link present in the final shared backup.

## What I configured

The later XR1 snapshot retains these mappings:

```cisco
segment-routing
 mapping-server
  prefix-sid-map
   address-family ipv4
    3.3.3.3/32 3 range 1
    4.4.4.4/32 4 range 1
```

XR1 also retains `segment-routing prefix-sid-map advertise-local` under IS-IS IPv4. Both XRs enable LDP on Gi0/0/0/1 toward their edge router; their core uses IS-IS SR-MPLS.

## What I observed

| Check | My real result |
|---|---|
| Mapping server | Two entries: 3.3.3.3/32 → index 3; 4.4.4.4/32 → index 4 |
| IS-IS database | XR1 advertises both SID Bindings; four Level-2 LSPs visible |
| XR2 SR label table | 16003 → 3.3.3.3/32; 16004 → 4.4.4.4/32 |
| R1 toward R2 | Outgoing label 24007; XR1 swaps 24007 → 16004 |
| R2 toward R1 | Outgoing label 24004; XR2 swaps 24004 → 16003 |
| Swap counters | XR1 24007: 4160 bytes; XR2 24004: **0 → 4160** in the supplied captures |
| Egress | XR2 16004: Pop toward R2; XR1 16003: Pop toward R1 |
| R1 → R2 | Source 3.3.3.3, destination 4.4.4.4: **20/20**, RTT 48/53/64 ms |
| R2 → R1 | Source 4.4.4.4, destination 3.3.3.3: **20/20**, RTT 32/53/68 ms |

## What I learned

The mappings reached the remote XR and produced usable forwarding entries. The swap counters and bidirectional pings provide evidence beyond configuration acceptance.

**Limit:** these are LFIB/counter and connectivity observations, not a per-packet capture or a timed failover test. The later backup is a combined end-of-session state, not an exact LAB 12 restore point.

**Evidence:** [Original CLI](evidencias/LAB12-SRMS-LDP-2026-11-17/CLI-OBSERVED.md) · [Shared XR configs](configs/LABS12-16-2026-11-17/README.md) · [Collection and coverage](evidencias/LABS12-16-2026-11-17/COLLECTION-AND-COVERAGE.md).
