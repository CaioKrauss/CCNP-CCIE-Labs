# My Post-LAB05 IPv6 Snapshot — 2026-11-13

I received seven `.cfg` files after LAB 05 and normalized their names and line endings **without changing the IOS commands**. The device's "Last configuration change" timestamp is not the file collection time.

## What I checked

- All seven hostnames and complete config end markers.
- IPv6 routing, multicast, CEF and OSPFv3 process 10/area 0.
- Six matching /64 transit links and seven distinct loopbacks.
- Static ASM RP `2001:DB8:100::1` and CE2/CE3 ASM + source-specific joins.
- CE1's temporary `2001:DB8:1::99` was **absent** in the final snapshot.
- Original IPv4 SSM joins differ by CE: CE2 `10.255.0.11`, CE3 `10.0.1.1`.

I found no credential or personal-data content during publication review. These are **running-config snapshots**, not fresh traffic tests or proof of saved startup state. **MLDv1 was not tested.**

[My LAB05 traffic results](../../LAB05-IPv6-Multicast.md) · [CLI capture](../../evidencias/LAB05-IPv6-PIM-MLDv2.txt).

## Original-byte SHA-256 hashes

I kept these hashes for the original CRLF uploads preserved in the [initial review commit](https://github.com/CaioKrauss/CCNP-CCIE-Labs/tree/ecb52b3204de383fbc1af7928ee7c6beaa6586f4/01-Multicast/configs/snapshot-2026-11-13). They do **not** match the later LF-normalized published bytes. I keep them to identify the historical originals.

| File | SHA-256 |
|---|---|
| [CE1.cfg](CE1.cfg) | `fced1e4fe38b14c20ef8f6ef479de0cca94fefb07d3024925a74c3aef5e76a9d` |
| [CE2.cfg](CE2.cfg) | `bc4e7bba47dd029571427ff53172603f7b1d849ab5319aae84d67134aa6a2bf8` |
| [CE3.cfg](CE3.cfg) | `bfc1970037f30a841ab93873adc1e5f3083489324f865ee05be094444fc9b147` |
| [PE1.cfg](PE1.cfg) | `b6857ba7531aa15c4742d8423fbda4ae3a1ed78af6334c4fd5253443a0f0b5dc` |
| [PE2.cfg](PE2.cfg) | `c9aa42dd87c3e641618d1952f030c3f7a9c941631486f0a0b0ac49159eac2205` |
| [PE3.cfg](PE3.cfg) | `6883aee80e50e04572ea616ee866015e28f586b1a92cf240dc89289956cff23d` |
| [RR-P.cfg](RR-P.cfg) | `33b34cf49071d719929fb6f973ee7a6c8a8d07fa9c744a9af5dae6708293e975` |

