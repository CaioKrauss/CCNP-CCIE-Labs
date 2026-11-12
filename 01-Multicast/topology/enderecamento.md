# Topologia e endereçamento — Multicast PIM-SM

Fonte: configurações `show running-config` de CE1, CE2, CE3, PE1, PE2, PE3 e RR-P, coletadas em 12/11/2026.

## Enlaces ponto a ponto

| Origem | Interface / IP | Destino | Interface / IP | Rede |
|---|---|---|---|---|
| CE1 | Fa0/0 — 10.0.1.1/30 | PE1 | Fa1/0 — 10.0.1.2/30 | 10.0.1.0/30 |
| PE1 | Fa0/0 — 10.0.12.1/30 | RR-P | Et1/2 — 10.0.12.2/30 | 10.0.12.0/30 |
| RR-P | Et1/1 — 10.0.23.1/30 | PE2 | Fa0/0 — 10.0.23.2/30 | 10.0.23.0/30 |
| PE2 | Fa1/0 — 10.0.2.1/30 | CE2 | Fa0/0 — 10.0.2.2/30 | 10.0.2.0/30 |
| RR-P | Et1/0 — 10.0.34.1/30 | PE3 | Fa0/0 — 10.0.34.2/30 | 10.0.34.0/30 |
| PE3 | Fa1/0 — 10.0.3.1/30 | CE3 | Fa0/0 — 10.0.3.2/30 | 10.0.3.0/30 |

## Loopbacks e papéis

| Nó | Loopback0 / Router ID OSPF | Papel |
|---|---|---|
| CE1 | 10.255.0.11/32 | Fonte prevista |
| PE1 | 10.255.0.12/32 | Trânsito |
| RR-P | 10.255.0.1/32 | RP estático |
| PE2 | 10.255.0.23/32 | Trânsito |
| CE2 | 10.255.0.22/32 | Receptor IGMP |
| PE3 | 10.255.0.33/32 | Trânsito |
| CE3 | 10.255.0.32/32 | Receptor IGMP |

## Características da baseline
- Cisco IOS 15.2, imagens C7200/Dynamips.
- `ip multicast-routing` em todos os nós.
- `router ospf 1` com `network 10.0.0.0 0.255.255.255 area 0` em todos os nós.
- `ip pim rp-address 10.255.0.1` em todos os nós.
- PIM Sparse Mode em todos os enlaces da tabela.
- CE1 e RR-P também possuem PIM Sparse Mode na Loopback0.
- CE2 e CE3 possuem `ip igmp join-group 239.1.1.1` em Fa0/0.
- A Loopback0 de CE2 e CE3 **não** possui PIM configurado na baseline.
- RR-P possui interfaces adicionais administrativamente desligadas, não utilizadas neste laboratório.

A topologia é uma árvore sem enlaces redundantes. Para estudar ECMP, FRR e caminhos alternativos será necessário adicionar conexões e rever a configuração.
