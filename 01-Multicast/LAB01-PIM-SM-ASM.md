# LAB 01 — PIM Sparse Mode (ASM) e Static RP

**Grupo:** `239.1.1.1` · **RP:** RR-P `10.255.0.1` · **Source:** CE1 `10.255.0.11` e `10.0.1.1` nas capturas · **Receiver:** CE2 / CE3.

## Conceito
- IGMP informa interesse no **grupo**; PIM Join `(*,G)` constrói shared tree em direção ao RP.
- Primeiro salto da origem pode encapsular o tráfego em PIM Register unicast para o RP; isso independe de IGMP Join prévio.
- Entrada `(S,G)` identifica uma fonte. Flag IOS `T` = SPT-bit set; a entrada `(S,G)` isolada não basta para afirmar switchover.
- RPF usa informação da MRIB/OSPF para escolher interface correta. No desenho atual há um único caminho físico até a origem.

## Configuração observada
```cisco
ip multicast-routing
ip pim rp-address 10.255.0.1 ASM_GROUPS
ip access-list standard ASM_GROUPS
 permit 239.1.1.1
! Nas interfaces envolvidas: ip pim sparse-mode
! CE2/CE3: ip igmp join-group 239.1.1.1 (captura inicial)
```
> Snapshot final dos dispositivos pode mostrar grupos adicionais ou Join ASM removido de CE2 por mudança de lab. As evidências iniciais preservam o estado do LAB 01.

## Evidência real
PE2: `(*,239.1.1.1)` flags **SJC**, IIF Fa0/0 RPF `10.0.23.1`, OIL Fa1/0; `(10.255.0.11,239.1.1.1)` com **T**, mesma IIF/OIL. CE2 tinha `OIL: Null` por estar inscrito localmente.

## Comandos
```cisco
show ip pim neighbor
show ip pim rp mapping
show ip igmp groups
show ip mroute 239.1.1.1
show ip rpf 10.255.0.11
show ip mroute count
```
[Saídas reais](evidencias/LAB01_PIM_SM_ASM.txt) · [Configurações finais](configs/snapshot-2026-11-12/).
