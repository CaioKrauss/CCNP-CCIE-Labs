# Night labs — Collection and evidence coverage

## Source and integrity

I inspected the attached `20261117-022341.zip` and the workspace copy with the same name. Both have SHA-256:

```text
39e288b15cc1e4aab4469b3bde06ddd654291ddce0e34a0b72381da505e8d4a8
```

The archive has exactly five entries: two running-configs, two command transcripts and one manifest. It has no R1/R2 configuration, BFD output, policy-state output, repair output or packet capture.

| Archive member | Bytes | SHA-256 of original member bytes |
|---|---:|---|
| manifest.json | 4148 | b3171cfdeaba97dfbd1ea9687f9566259825a066215fefb94030b83ecde5ff49 |
| XR1-running.cfg | 3714 | cec2b1ff9a94fc6bd16abf5a4252fb69f6034095cd73ed45594461ef0fb5c737 |
| XR1-transcript.json | 6311 | cae9724b87df70b1e013148044d3f7eb9d9dc6e3e021baf45500e66b72b138e5 |
| XR2-running.cfg | 2392 | ada04599faec15b06edc83921da7c600d2d54d5e1af1381f6fd3b7a592653a5b |
| XR2-transcript.json | 3659 | e834e54be73eee04d4810d9b5c2fb72c4b1e2dc23f87fd4d64d30733c9d1fcaa |

The original [manifest](manifest.json) records hashes/lengths of the configs with LF line endings: XR1 **3520 bytes**, SHA-256 `04aaba9961deda0c49931664398db91ff65f9cc86105b090501627002b5965d2`; XR2 **2267 bytes**, SHA-256 `cab90231d9cb728882b01b71090094852e0ecb11cbd22876e3e0b381e7a2ad98`. Both match after CRLF→LF normalization. The archive members use CRLF; this explains the difference without altering the original manifest.

[XR1 transcript](XR1-transcript.json) · [XR2 transcript](XR2-transcript.json) · [Original configuration files](../../configs/LABS12-16-2026-11-17/README.md)

## Temporal coverage

| Event | UTC | São Paulo (UTC−03:00) |
|---|---|---|
| LAB 12 mapping / forwarding captures | Nov 17, 02:02–02:05 | Nov 16, 23:02–23:05 |
| XR2 last recorded configuration change | Nov 17, 05:04:54 | Nov 17, 02:04:54 |
| XR1 last recorded configuration change | Nov 17, 05:19:36 | Nov 17, 02:19:36 |
| Latest retrieved BGP RIB capture | Nov 17, 05:21:13.599 | Nov 17, 02:21:13.599 |
| Manifest collected_at | Nov 17, 05:23:43.555617 | Nov 17, 02:23:43.555617 |
| XR1 show running-config timestamp | Nov 17, 05:23:43.679 | Nov 17, 02:23:43.679 |
| XR2 show running-config timestamp | Nov 17, 05:23:44.749 | Nov 17, 02:23:44.749 |

The filename's **02:23 is local time**, whereas router outputs show UTC. This snapshot follows the retrieved LAB 16 checks at 05:21 UTC, but **predates LAB 17's recovered 05:34:22 UTC output**. The prior conclusion that no newer XR show run was needed was limited to the earlier recovered excerpt and is superseded. This is a historical snapshot, not a verified final/current configuration for LABs 13–17. Small host/router timestamp differences are retained; no clock synchronization measurement is claimed.

The commit lists retain timestamps from Nov 16 20:40:30 to Nov 17 05:19:36 UTC on XR1, and Nov 16 20:41:04 to Nov 17 05:04:54 UTC on XR2. They list changes, but contain no historical config diffs. They cannot reconstruct the state at each lab stage.

## What each lab can claim from recovered evidence

| Lab | Supported result | Remaining gap |
|---|---|---|
| [12 — SRMS/LDP](../../LAB12-SR-MPLS-SRMS-LDP-INTERWORKING.md) | SID mappings, LFIB swaps/counters, 20/20 pings both ways | Exact contemporaneous full configs, R1/R2 configs, packet-level capture |
| [13 — SR-TE](../../LAB13-SR-TE-IOSXR.md) | Committed explicit policy and color/VPN configuration | Original policy state, label meaning, steering and delivery results |
| [14 — LFA/TI-LFA](../../LAB14-LFA-TI-LFA-ISIS-IOSXR.md) | XR1 per-prefix FRR/TI-LFA directives | Computed repair, failure/recovery and timing evidence |
| [15 — BFD + IS-IS](../../../07-High-Availability/LAB15-BFD-ISIS-IOSXR.md) | Session topic identified; historical snapshot contains no BFD directives | Original BFD config, session state, timers and failure/recovery outputs |
| [16 — BGP Advanced](../../../06-BGP-Advanced/LAB16-BGP-POLICY-BESTPATH-IOSXR.md) | MED test state, community/LOCAL_PREF changes, iBGP best-path and RIB results | Earlier prepending/baseline outputs, R1/R2 configs; traffic/multipath not demonstrated |

“Partial evidence” describes what this publication can substantiate. It does not turn an inaccessible test into a failed test.

## Chat provenance and retrieval limits

- [Ideias para lab Multicast](https://chatgpt.com/c/6af4c0c1-7098-83e9-99c1-7f13b5e1cb49): user CLI for LAB 12 at 02:02–02:05 UTC; copied to the [LAB 12 evidence file](../LAB12-SRMS-LDP-2026-11-17/CLI-OBSERVED.md).
- [Próximo lab SR TE](https://chatgpt.com/c/6afbb8c6-3b30-83e8-ab14-6be459107b14): returned recent LAB 16 turns only, at 05:16–05:21 UTC; copied to the [LAB 16 evidence file](../../../06-BGP-Advanced/evidencias/LAB16-BGP-2026-11-17/CLI-OBSERVED.md).
- The project chat **Integrar FRR ao EVE-NG** records the collection of the two XRs and saving this ZIP.

The two ChatGPT history responses exposed no older-page cursor despite returning only recent portions. Other available project chat excerpts did not supply LAB 13–15 operational results; the web fallback required sign-in. The original chats may contain additional evidence. Their links require account access; the published CLI excerpts remain readable in GitHub.

No config was invented and no device was reconfigured or retested during publication. **Fresh XR1/XR2/R1/R2 show runs are requested for the final lab state. Historical LAB 13–15, LAB 16 prepending/baseline and LAB 17 failure-stage outputs remain missing.** Future edits should update these existing guides and indexes.

## Update — LAB 17

The [LAB 17 guide](../../../06-BGP-Advanced/LAB17-BGP-MULTIPATH-ECMP-IOSXR.md) preserves the newly retrieved 05:34:22 UTC CLI. No newer attachment was returned. The workspace ZIP hash matches the archive documented above. The raw CFG/transcript/manifest files remain unchanged.
