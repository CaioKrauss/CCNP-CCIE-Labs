# Post-LAB05 Snapshot — 2026-11-13

Source: seven user-uploaded .cfg files, originally named with a (2) suffix. Names were normalized. The initial publication preserved original bytes; a later revision normalized line endings to LF and removed the final newline without changing commands. That review did not run the Python collector, make a fresh device collection or restart the VM. Last configuration change is the device timestamp, not the collection timestamp.

## Publication review

The review checked passwords/secrets, usernames, SNMP communities, keys, certificates, AAA/RADIUS/TACACS, URLs and personal identifiers. No secret or personal information was identified and no redaction was required. IPv4 unicast values are in 10.0.0.0/8; IPv6 values are in 2001:DB8::/32. Absence of published credentials is not an access-hardening assessment.

## Static checks

- Seven expected hostnames and final end markers; no pagination marker or command error.
- IPv6 unicast routing, multicast routing and CEF on all nodes.
- OSPFv3 process 10/area 0, distinct router IDs and passive Loopback0.
- Six matching /64 transit subnets and distinct /128 loopbacks.
- Static RP 2001:DB8:100::1 on all nodes, assigned to RR-P Loopback0.
- CE2/CE3 join FF1E::1234 and source-specific FF3E::1234 from 2001:DB8:1::1. IOS saves the latter without the word include.
- CE1 retains 2001:DB8:1::1/64; temporary 2001:DB8:1::99/64 is absent.
- Prior IPv4 configuration remains. CE2 selects 10.255.0.11 for IPv4 SSM while CE3 selects 10.0.1.1; that historical difference was not changed.

These files establish snapshot configuration, not current operation, startup-config persistence or new traffic tests. MLDv2/ASM/SSM results remain grounded in the [console evidence](../../evidencias/LAB05-IPv6-PIM-MLDv2.txt). MLDv1 was not tested.

## Original-byte SHA-256 hashes

The following hashes describe the original CRLF bytes preserved in the [initial review commit](https://github.com/CaioKrauss/CCNP-CCIE-Labs/tree/ecb52b3204de383fbc1af7928ee7c6beaa6586f4/01-Multicast/configs/snapshot-2026-11-13). Do not compare them directly with normalized files on main. Equivalence after line-ending normalization was checked in the earlier review. This English revision preserves the current configuration bytes.

| File | SHA-256 |
|---|---|
| [CE1.cfg](CE1.cfg) | `fced1e4fe38b14c20ef8f6ef479de0cca94fefb07d3024925a74c3aef5e76a9d` |
| [CE2.cfg](CE2.cfg) | `bc4e7bba47dd029571427ff53172603f7b1d849ab5319aae84d67134aa6a2bf8` |
| [CE3.cfg](CE3.cfg) | `bfc1970037f30a841ab93873adc1e5f3083489324f865ee05be094444fc9b147` |
| [PE1.cfg](PE1.cfg) | `b6857ba7531aa15c4742d8423fbda4ae3a1ed78af6334c4fd5253443a0f0b5dc` |
| [PE2.cfg](PE2.cfg) | `c9aa42dd87c3e641618d1952f030c3f7a9c941631486f0a0b0ac49159eac2205` |
| [PE3.cfg](PE3.cfg) | `6883aee80e50e04572ea616ee866015e28f586b1a92cf240dc89289956cff23d` |
| [RR-P.cfg](RR-P.cfg) | `33b34cf49071d719929fb6f973ee7a6c8a8d07fa9c744a9af5dae6708293e975` |
