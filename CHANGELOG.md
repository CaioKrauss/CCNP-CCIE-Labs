# Documentation Changes

## 2026-11-17 — LAB 17 and corrected snapshot scope

- Added original LAB 17 recovery-state CLI, a concise guide and a configuration-gap README, preserving the existing folder scheme.
- Documented BGP/RIB multipath, reported failover, and ADD-PATH vs Multipath without inferring FIB traffic distribution or negotiated ADD-PATH.
- Superseded the earlier final-snapshot wording: the 05:23 UTC backup predates the recovered LAB 17 output at 05:34 UTC. Raw historical backups remain unchanged; fresh configurations and missing test logs are requested.
- Reused LABs 12–16 without duplicates; retained their partial-evidence status.


## 2026-11-17 — Night labs 12–16 and shared XR snapshot

- Added LAB 12 SRMS/LDP with original SID/LFIB outputs and 20/20 pings each way; added LAB 16 BGP with chronological user CLI and final policy/RIB observations.
- Added LAB 13 SR-TE and LAB 14 LFA/TI-LFA as partial-evidence records, and LAB 15 BFD + IS-IS as evidence pending. Missing historical outputs are not reported as failed tests.
- Preserved the five original ZIP members once, linked across labs, and documented missing R1/R2 and intermediate configurations.
- Corrected the temporal interpretation: 02:23 -03:00 is 05:23 UTC, after the final recovered BGP checks. Documented original-byte hashes and the manifest's LF normalization.
- Updated root/topic indexes without replacing the earlier LAB 11 evidence. No router changes or new tests were performed.

## 2026-11-16 — Shorter, first-person study notes

- Rewrote my **12 completed lab guides** as compact first-person reports: **what I tested → configured → observed → learned**.
- Simplified the root and topic indexes, troubleshooting, automation guide, future-study pages and lab template. I kept practical commands and exact measured results.
- Preserved original device configs, CLI logs, manifests, screenshots and historical source details. For LAB 11, I moved the long original report to a separate **evidence archive** and linked it from the short guide.
- Checked internal Markdown link targets and reviewed the text configuration/evidence files for obvious credential directives. Raw captures were not silently rewritten.
- Clarified that **IGP state, programmed forwarding entries, ping and timed failover results are different types of proof**. I kept all not-tested limitations, including SR-TE and measured FRR time.

These edits are documentation only: **I did not rerun the EVE-NG devices or change router configurations**.

## 2026-11-13 — English public edition

- Rewrote all 27 existing Markdown documents in English and expanded the six completed lab guides with command purpose, observed results, interpretation, troubleshooting and explicit limits.
- Added the owner's original multicast and MPLS topology screenshots. No screenshot was fabricated or edited.
- Clarified that the MPLS collection validates CUST-A only. CE1_B/CE2_B are visible in the screenshot but were not collected; L2 devices remain reserved for later work.
- Translated editorial annotations in ten evidence files while preserving router-response lines. Configuration snapshot bytes remain unchanged.
- Updated the L3VPN SHA-256 manifest for the current published evidence bytes after translating headers. Original historical hashes in the multicast snapshot README retain their original-byte meaning.
- Corrected the outdated multicast configuration note that said snapshots were not published. Preserved the earlier LAB05 cleanup question as historical and linked its later resolution.
- Translated the automation utility's help, comments and messages. Kept callable names, CLI options, environment variables and legacy error-file suffixes compatible. Replaced the embedded management host with documentation placeholder 192.0.2.10; users must set --host for their environment. Declared Python 3.10+ as the supported baseline.
- Retained existing paths for link compatibility. Planned study areas are explicitly labeled as planned, with no invented operational results.

This is an editorial and publication update. No new multicast, fault-injection or customer-B test was performed, and no router configuration was changed as part of the rewrite. The separate Notion revision notebook remains in Portuguese.
