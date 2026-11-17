# LAB 15 — BFD + IS-IS

**My goal:** study BFD integration with IS-IS and distinguish fault detection from forwarding recovery.

**Result documented here:** evidence pending. The session identifies this as LAB 15, but its original BFD outputs were not returned by chat retrieval. The final XR1/XR2 backup contains IS-IS configuration and **no BFD directives**.

## My topology

The shared session uses IOS XR 6.3.1 on XR1 and XR2, with two direct links and IS-IS metrics 10 and 100. The available backup does not identify which interface participated in the earlier BFD test.

## What I configured

No BFD configuration has been reconstructed. Its absence from the final snapshot cannot establish whether an earlier configuration was removed, rejected or never committed.

## What I observed

| Check | Evidence available |
|---|---|
| IS-IS configuration | Present in the final XR1/XR2 running configs |
| BFD configuration / session state | Not present in the supplied collection |
| Negotiated timers / discriminator | Unavailable |
| IS-IS reaction to BFD failure | Unavailable |
| Traffic loss / recovery time | Unavailable |

## What I learned

A final running-config is not a history of every test performed that night. I need the BFD session output, associated IS-IS state and failure/recovery evidence before recording the outcome.

**Limit:** no success or failure is inferred. A protocol timer is not a measured outage. A later show run alone will not recover a removed historical BFD configuration.

**Evidence:** [Shared XR snapshot](../03-Segment-Routing/configs/LABS12-16-2026-11-17/README.md) · [Coverage and outstanding sources](../03-Segment-Routing/evidencias/LABS12-16-2026-11-17/COLLECTION-AND-COVERAGE.md).
