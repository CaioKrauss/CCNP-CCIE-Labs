# Documentation Changes

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
