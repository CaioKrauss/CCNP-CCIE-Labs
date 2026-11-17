# LAB 17 — BGP Multipath / ECMP and Failover

**My goal:** use two BGP paths for 198.51.100.0/24, observe recovery after a peering failure, and distinguish Multipath from ADD-PATH.

**Result:** XR1's recovered output at **05:34:22 UTC on 2026-11-17** shows two BGP paths and two RIB descriptors marked multipath. The conversation reports the failover test as completed; only the restored-state CLI was retrievable. Traffic distribution, failure-stage behavior and convergence time remain undocumented.

## My topology

```text
R1 AS 65101 -- eBGP -- XR1 AS 65000 -- iBGP -- XR2 AS 65000 -- eBGP -- R2 AS 65102
  10.0.13.1             1.1.1.1               2.2.2.2
```

The session uses IOS XRv 6.3.1 and the existing LAB 16 topology. XR1 knows both alternatives without requiring ADD-PATH from a route reflector.

## What I configured

The final multipath configuration commands and complete running-configs were not returned by chat retrieval. I have not reconstructed them from operational flags or copied the older backup as a LAB 17 restore point.

The historical ZIP was collected at **02:23:43 -03:00 / 05:23:43 UTC**, before this output. See [configuration status and collection request](configs/LAB17-BGP-MULTIPATH-2026-11-17/README.md).

## What I observed

| Check | My real result |
|---|---|
| Sessions | XR1 peers 2.2.2.2 (AS 65000) and 10.0.13.1 (AS 65101) have numeric received-prefix counts: 2 and 1 |
| Prefix | 198.51.100.0/24: 2 available paths; best #2 |
| R1 path | AS 65101; next-hop 10.0.13.1; LOCAL_PREF 200; metric 0; external, best, multipath; community 65101:200 |
| XR2 path | AS 65102; next-hop 2.2.2.2; LOCAL_PREF 200; metric 0; internal, multipath, backup, add-path |
| RIB | Both next-hops marked BGP multi path; distance 20; tag 65101 |
| Backup indicator | Number of pic paths 1, type internal and external |
| Advertisement | Best path advertised to 2.2.2.2; alternative says Not advertised to any peer |
| Recovery context | eBGP uptime 00:00:41; prefix last modified at 05:33:41 UTC; conversation identifies this as restored peering |
| Failure / forwarding | Failure-stage CLI, CEF output, packet counters and loss/timing measurements unavailable |

Commands actually captured:

```cisco
show bgp summary
show bgp ipv4 unicast 198.51.100.0/24
show route 198.51.100.0/24
```

## What I learned

- **Multipath/ECMP** enables multiple eligible forwarding paths. Two BGP paths alone do not prove ECMP; this capture additionally shows both RIB descriptors marked multipath. CEF and traffic evidence are still needed to document actual distribution.
- **ADD-PATH** advertises multiple paths for the same prefix when negotiated and selected by policy. It does not require Multipath; Multipath does not require ADD-PATH when the router already knows the paths. Default best-path advertisement remains subject to BGP export and loop-prevention rules.
- **Backup/PIC flags are not a timing measurement.** The local `add-path` flag does not prove multiple paths were sent. Here the alternative is explicitly not advertised; no negotiated ADD-PATH exchange or PIC scalability test is established.

**Limit:** failover completion is reported in the conversation, while only recovery state is supported by the recovered user CLI. No lossless, sub-50-ms, equal traffic split, FIB backup programming or LAB 18 PIC result is claimed. ADD-PATH can reduce path hiding, but it cannot supply paths the sender never learned or make unequal paths eligible for ECMP.

**Evidence:** [Original CLI](evidencias/LAB17-BGP-MULTIPATH-2026-11-17/CLI-OBSERVED.md) · [Config status](configs/LAB17-BGP-MULTIPATH-2026-11-17/README.md) · [LAB 16 and path hiding](LAB16-BGP-POLICY-BESTPATH-IOSXR.md).
