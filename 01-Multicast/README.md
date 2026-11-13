# Multicast IPv4 e IPv6 — Labs 01–05 (CCNP/CCIE SP)

Topologia Cisco IOS no EVE-NG, com sete roteadores, OSPFv2 (IPv4) e OSPFv3 (IPv6). Evidências dos Labs 01–04 coletadas em 12/11/2026; LAB 05 documentado a partir de saídas do console em 13/11/2026. Os arquivos de evidências registram saídas reais, não exemplos inventados.

```text
CE1 (source) --- PE1 --- RR-P (RP ASM / BIDIR / Anycast 1)
                            |                    |
                            +--- PE2 --- CE2     +--- PE3 (Anycast 2) --- CE3
```

> Observação: topologia em estrela com **caminho único** via RR-P. PE3 não tem enlace direto com PE2; mudar custo OSPF sem adicionar links não cria caminho alternativo. O nome RR-P não representa BGP RR neste laboratório.

## Laboratórios concluídos

| Lab | Grupo | Controle | Evidências |
|---|---|---|---|
| [01 — PIM-SM (ASM)](LAB01-PIM-SM-ASM.md) | `239.1.1.1` | Static RP `10.255.0.1` | IGMP Join, `(*,G)`, `(S,G)`, flag T e RPF |
| [02 — PIM-SSM + IGMPv3](LAB02-PIM-SSM-IGMPv3.md) | `232.1.1.1` | Sem RP | source filtering e contadores 26→28 no PE2 |
| [03 — PIM-BIDIR](LAB03-PIM-BIDIR.md) | `239.2.2.2` | RP `10.255.0.2` | DF, `(*,G)`, RP-tree 14→17; fontes CE1/CE3 testadas |
| [04 — Anycast RP + MSDP](LAB04-Anycast-RP-MSDP.md) | `239.3.3.3` | Anycast `10.255.0.100` | MSDP Up, SA, failover OSPF e novo Join; PE2 24→26 |
| [05 — IPv6 ASM + SSM / MLDv2](LAB05-IPv6-Multicast.md) | `FF1E::1234` e `FF3E::1234` | RP IPv6 (ASM), INCLUDE (SSM) | OSPFv3, PIM Register, SPT, 2 receptores, filtro de fonte positivo/negativo |

- [Comandos de consulta](comandos.md)
- [Validação e troubleshooting](troubleshooting.md)
- [Evidências TXT dos 5 labs](evidencias/) (LAB05 extraído das saídas compartilhadas no chat)
- [Snapshot histórico pré-LAB05 — 12/11](configs/snapshot-2026-11-12/)
- [Snapshot pós-LAB05 — 7 show running-configs revisados em 13/11](configs/snapshot-2026-11-13/)
- [Topologia e endereçamento](topology/enderecamento.md)
- [Backup automatizado de show run](../09-Automation/backup_show_run_eve.py)

## Baseline vigente

- **OSPF:** processo 1, área 0, usando as loopbacks e os enlaces ponto a ponto.
- **ASM:** ACL `ASM_GROUPS` → RP `10.255.0.1`.
- **SSM:** `ip pim ssm default` → `232.0.0.0/8`.
- **BIDIR:** ACL `BIDIR_GROUPS` → RP `10.255.0.2` com `bidir`.
- **Anycast:** ACL `ANYCAST_GROUPS` → RP lógico `10.255.0.100`, compartilhado entre RR-P e PE3; MSDP entre `10.255.0.1` e `10.255.0.33`.

## Estado e limitações

- Há comprovação de encaminhamento multicast nos labs SSM, BIDIR e Anycast via `show ip mroute count`.
- Para o PIM-SM inicial, existem tabelas `(S,G)` com flag T, mas o registro enviado não inclui contadores comparáveis de entrega ao receptor para esse grupo.
- O teste de failover Anycast comprovou reconvergência do RP, nova inscrição e contadores no PE2; **não** demonstrou registro de uma *nova source inédita* após a falha.
- O teste BIDIR de duas fontes foi confirmado na conversa, sem uma captura de contador individual rotulada por cada origem.
- **LAB05 IPv6:** ASM + MLDv2 e SSM + filtragem de fontes verificados; **MLDv1 específico não foi testado**.
- **Backups pós-LAB05 publicados:** IPv6, OSPFv3, RP e joins ASM/SSM conferidos nos sete arquivos. `2001:DB8:1::99` ausente no CE1; gravação em startup-config não comprovada pelos backups.
- **Próximos labs:** mVPN/MPLS e troubleshooting de RPF com redundância física.

## Segurança

O repositório é público. Os sete arquivos de cada snapshot foram revisados quanto a senhas, tokens e chaves; não foram encontrados dados desse tipo. Os arquivos contêm apenas endereçamento fictício/de laboratório, inclusive IPv6 de documentação 2001:DB8::/32. Em novos backups, revise credenciais/segredos antes de publicar. Não publique arquivos do diretório local `backups/` indiscriminadamente.
