# LAB 03 — PIM-BIDIR e Designated Forwarder

**Grupo:** `239.2.2.2` · **RP:** RR-P `10.255.0.2` · **Origens testadas:** CE1 e CE3.

## Conceito
PIM-BIDIR usa árvore compartilhada bidirecional `(*,G)`; adequado a muitos transmissores no mesmo grupo. Não usa PIM Register nem cria SPT `(S,G)` separada por fonte. **DF** é eleito por enlace para encaminhar pacotes em direção ao RP sem loops. BIDIR em si não é alta disponibilidade automática de RP.

## Configuração
```cisco
ip pim bidir-enable
ip pim rp-address 10.255.0.2 BIDIR_GROUPS bidir
ip access-list standard BIDIR_GROUPS
 permit 239.2.2.2
! RR-P Loopback1: 10.255.0.2/32
! CE2/CE3: ip igmp join-group 239.2.2.2
```

## Evidências reais
```text
PE2: (*,239.2.2.2), RP 10.255.0.2, flags BC
Bidir-Upstream: Fa0/0, RPF nbr 10.0.23.1
IIL: Fa1/0 e Fa0/0 (Accepting/Sparse)
OIL: Fa1/0 Forward/Sparse e Fa0/0 Bidir-Upstream/Sparse
DF em Fa0/0 = RR-P (10.0.23.1)
DF em Fa1/0 = PE2 (*10.0.2.1)
Source count 0; RP-tree forwarding: 14 → 15 → 17
```
Aumento de contadores observado; o teste de duas origens foi confirmado em chat, sem log individual rotulado para cada transmissão.

## Verificação
```cisco
show ip pim interface df
show ip mroute 239.2.2.2
show ip mroute count
```
[Saídas reais, inclusive log bruto](evidencias/LAB03_PIM_BIDIR.txt).
