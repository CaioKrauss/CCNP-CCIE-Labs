# Observed Configurations — CUST-A L3VPN

Collected directly from device consoles on 2026-11-13 at approximately 15:43, America/Sao_Paulo. These are the configurations found during validation, not newly applied configurations.

- Nine files: running/startup for CE1_A, CE2_A, R1 and R3; running for XR1.
- Effective running/startup commands match on the four IOS devices after excluding comments and capture headers.
- XR1 has an active configuration and an existing commit history; latest listed commit 1000000019. No new commit or reboot test was performed.
- Only command echo, external capture headers and the final prompt were removed. Configuration files use UTF-8/LF.
- The captured XR configuration does not include local access credentials. These snapshots are not a complete image-installation or authentication package.
- Publication review found no password/hash, private key, token or production-customer data. EVE management addresses and console ports are excluded.
- Addresses belong to this isolated scenario; some loopbacks use public IPv4 values and must not be advertised outside the lab.
- L2 devices were not configured or renamed. CE1_B/CE2_B, later identified in the supplied screenshot, were not part of the five-device capture.

[CLI evidence](../../evidencias/LAB01-L3VPN-2026-11-13/) preserves the command responses. SHA256SUMS.txt hashes the current published UTF-8 bytes; English editorial headers in evidence files were translated and the manifest regenerated. Router responses and configuration commands were preserved.
