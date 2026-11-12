# Notas de configuração — baseline

Esta pasta documenta a configuração observada nos arquivos locais `CE1.cfg`, `CE2.cfg`, `CE3.cfg`, `PE1.cfg`, `PE2.cfg`, `PE3.cfg` e `RR-P.cfg`.

**Os backups brutos não foram publicados.** Eles podem conter informações sensíveis e devem permanecer fora do repositório público.

## Elementos comuns confirmados
```cisco
ip multicast-routing
ip cef
router ospf 1
 network 10.0.0.0 0.255.255.255 area 0
ip pim rp-address 10.255.0.1
```
Cada equipamento tem seu próprio `router-id` OSPF, igual ao endereço da Loopback0. Os enlaces ponto a ponto usam /30; veja [endereçamento](../topology/enderecamento.md).

## Variações
- CE1: PIM Sparse Mode em Loopback0 e Fa0/0.
- CE2: PIM Sparse Mode e `ip igmp join-group 239.1.1.1` em Fa0/0.
- CE3: PIM Sparse Mode e `ip igmp join-group 239.1.1.1` em Fa0/0.
- PE1/PE2/PE3: PIM Sparse Mode nas duas interfaces FastEthernet de trânsito.
- RR-P: PIM Sparse Mode na Loopback0 e em Ethernet1/0, 1/1 e 1/2.

**Nota:** o nome RR-P não implica configuração BGP RR; não há processo BGP nos backups analisados.
