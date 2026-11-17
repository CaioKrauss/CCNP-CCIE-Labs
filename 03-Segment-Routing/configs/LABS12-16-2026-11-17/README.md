# Shared end-of-session XR configuration snapshot

Collected on **2026-11-17 at 02:23:43 -03:00 (05:23:43 UTC)** from the SR-MPLS lab.

- [XR1 running-config](XR1-running.cfg): last configuration change **05:19:36 UTC**.
- [XR2 running-config](XR2-running.cfg): last configuration change **05:04:54 UTC**.
- [Collection, provenance, hashes and missing files](../../evidencias/LABS12-16-2026-11-17/COLLECTION-AND-COVERAGE.md).

These are the two original CFG files from `20261117-022341.zip`, with CRLF bytes preserved. They contain the accumulated state of LABs 12–16, not five independent restore points. Other lab guides link here rather than duplicating the files.

**Coverage:** SRMS/LDP, SR-TE, XR1 FRR/TI-LFA and final BGP policy configuration are present. BFD directives are absent. R1/R2 running-configs are absent. Definitions left over from earlier steps may remain unused; inspect policy attachments.

The snapshot follows the latest retrieved BGP validation at **05:21:13 UTC**. No later XR show run is known to be missing for that validation. A newer collection would be needed only to document changes after this backup. Historical intermediate states and the missing R1/R2 configs still need their own evidence.
