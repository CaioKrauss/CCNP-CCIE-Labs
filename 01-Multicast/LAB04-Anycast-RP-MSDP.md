# LAB 04 — Anycast RP + MSDP + Failover

**Grupo:** `239.3.3.3` · **Anycast RP:** `10.255.0.100` · **RP1:** RR-P · **RP2:** PE3 · **Source:** `10.255.0.11`.

## Conceito
Dois roteadores anunciam o mesmo `/32` do RP via OSPF; cada roteador alcança o RP logicamente mais próximo. MSDP compartilha **Source-Active (SA)** entre RPs via sessão TCP usando endereços únicos, não o Anycast. SA é informação da fonte, não a transferência de todo o fluxo de dados.

## Configuração (snapshot final)
```cisco
! RR-P e PE3
interface Loopback10
 ip address 10.255.0.100 255.255.255.255
 ip pim sparse-mode
!
ip pim rp-address 10.255.0.100 ANYCAST_GROUPS
ip access-list standard ANYCAST_GROUPS
 permit 239.3.3.3
!
! RR-P
ip msdp peer 10.255.0.33 connect-source Loopback0
ip msdp originator-id Loopback0
ip msdp cache-sa-state
! PE3
ip msdp peer 10.255.0.1 connect-source Loopback0
ip msdp originator-id Loopback0
ip msdp cache-sa-state
```

## Evidências reais
- MSDP **Up** em ambos RPs, **0 resets**.
- PE3 `show ip msdp sa-cache`: `(10.255.0.11,239.3.3.3)`, originado por RR-P `10.255.0.1`.
- PE3 `show ip mroute`: `(S,G)` flags **MT** (posteriormente **MTA/TA**), OIL Fa1/0.
- Failover: `shutdown` da **Loopback10** RR-P; RR-P aprende `10.255.0.100/32` via **OSPF**, next-hop `10.0.34.2`, métrica **11** e RPF via Ethernet1/0.
- Após renovar o Join do CE2, PE2 manteve `(*,G)` e `(S,G)` com OIL Fa1/0; contador do fluxo `10.255.0.11` **24 → 26**.
- **Limite da prova:** fluxo `(S,G)` já conhecido; não foi demonstrado novo registro de uma *fonte inédita* após a falha.

## Teste controlado
```cisco
! RR-P (laboratório apenas)
interface Loopback10
 shutdown
! Verificar no RR-P e PE2:
show ip route 10.255.0.100
show ip rpf 10.255.0.100
show ip msdp peer
show ip mroute 239.3.3.3
show ip mroute count
! Restaurar RR-P
interface Loopback10
 no shutdown
```
[Saídas reais e sequência da falha](evidencias/LAB04_ANYCAST_RP_MSDP.txt).
