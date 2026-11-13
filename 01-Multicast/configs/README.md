# Multicast Configuration Snapshots

These directories contain reviewed snapshots for CE1, CE2, CE3, PE1, PE2, PE3 and RR-P.

| Snapshot | Meaning | Limitation |
|---|---|---|
| [2026-11-12](snapshot-2026-11-12/) | Combined final state after IPv4 Labs 01–04 | Not the exact intermediate state of every experiment |
| [2026-11-13](snapshot-2026-11-13/) | Post-LAB05 state with IPv6/OSPFv3 and ASM/SSM joins | Running-config only; does not prove persistence or current forwarding |

An older version of this note said backups had not been published. That statement predates the reviewed snapshot uploads; the directories above are now the authoritative published copies.

## Initial baseline

```cisco
ip multicast-routing
ip cef
router ospf 1
 network 10.0.0.0 0.255.255.255 area 0
ip pim rp-address 10.255.0.1
```

Each router uses a unique Loopback0-derived OSPF router ID. Transit subnets are /30. PIM sparse mode is enabled on the participating transit interfaces; initial receiver joins are on CE2/CE3 Fa0/0. Later labs add group-scoped RP mappings, SSM, BIDIR, Anycast and IPv6.

RR-P has no BGP process in these multicast snapshots. Do not infer route-reflector behavior from its hostname.

Keep raw local collection directories private until reviewed. Snapshot commands retain their original text during the English documentation revision.

[Addressing](../topology/enderecamento.md) · [Historical test evidence](../evidencias/)
