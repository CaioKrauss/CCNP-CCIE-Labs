# My Multicast Labs — 01–05

I used seven Cisco IOS routers in an EVE-NG tree: **CE1 → PE1 → RR-P**, branching to **PE2/CE2** and **PE3/CE3**. I ran IPv4 tests with OSPFv2 and extended the lab to IPv6 with OSPFv3.

![My multicast topology](topology/multicast-eve-ng.png)

## What I tested

| Lab | Main idea | Key evidence |
|---|---|---|
| [01 — ASM](LAB01-PIM-SM-ASM.md) | Join group G via RP 10.255.0.1 | `(*,G)`, `(S,G)`, IOS T flag |
| [02 — SSM](LAB02-PIM-SSM-IGMPv3.md) | Join an exact source/group pair | PE2 packets **26→28** |
| [03 — BIDIR](LAB03-PIM-BIDIR.md) | One shared tree, DF election | RP-tree packets **14→17** |
| [04 — Anycast RP](LAB04-Anycast-RP-MSDP.md) | Two RPs and MSDP source discovery | Known-source packets **24→26** after RP loopback shutdown |
| [05 — IPv6](LAB05-IPv6-Multicast.md) | ASM, SSM and MLDv2 | Source filtering; both receivers replied |

## What I keep in mind

- This is a **physical tree**; changing an OSPF cost cannot create a second cable or bypass RR-P.
- In **SSM**, the source IP matters. In **BIDIR**, per-source SPT entries are not expected.
- I shut an **RP loopback** in LAB04, not an entire router. I did not prove full-router failover.
- I collected configurations after the experiments. Those snapshots are **not** exact copies of every intermediate state.

## My references

[Addressing](topology/enderecamento.md) · [Commands](comandos.md) · [Troubleshooting](troubleshooting.md) · [IPv4 configs](configs/snapshot-2026-11-12/) · [IPv6 configs](configs/snapshot-2026-11-13/) · [Raw CLI](evidencias/).
