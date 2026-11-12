# LAB 02 — PIM SSM + IGMPv3

**Grupo:** `232.1.1.1` · **Sem RP** · **CE2:** origem `10.255.0.11`; **CE3:** origem `10.0.1.1`.

## Conceito
No SSM o receptor já informa o par `(S,G)` com IGMPv3 **INCLUDE**; não há RP, Register ou switchover a partir de `(*,G)`. O flag `T` pode aparecer porque a SPT específica já está ativa. IGMPv2 participa de um grupo, IGMPv3 pode selecionar fontes.

## Configuração verificada
```cisco
! Todos
ip pim ssm default
! CE2 Fa0/0
ip igmp version 3
ip igmp join-group 232.1.1.1 source 10.255.0.11
! CE3 Fa0/0
ip igmp version 3
ip igmp join-group 232.1.1.1 source 10.0.1.1
```

## Evidências reais
- PE2: `(10.255.0.11,232.1.1.1)`, flags **sTI**, IIF Fa0/0 via RR-P, OIL Fa1/0; RPF OSPF via `10.0.23.1`.
- CE2: flags **sPLTXI**, OIL Null (receptor local).
- PE3: `(10.0.1.1,232.1.1.1)`, flags **sTI**, RPF `10.0.34.1`, OIL Fa1/0.
- PE2 recebeu/encaminhou **26 → 28 pacotes**, RPF failed **0**.

## Verificação
```cisco
show ip igmp groups
show ip mroute 232.1.1.1
show ip rpf 10.255.0.11
show ip mroute count
```
[Saídas reais](evidencias/LAB02_PIM_SSM_IGMPv3.txt).
