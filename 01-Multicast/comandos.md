# Comandos rápidos — Multicast (IOS)

```cisco
terminal length 0
show ip ospf neighbor
show ip route 10.255.0.11
show ip pim neighbor
show ip pim rp mapping
show ip pim interface df
show ip igmp groups
show ip mroute 239.1.1.1
show ip mroute 232.1.1.1
show ip mroute 239.2.2.2
show ip mroute 239.3.3.3
show ip mroute count
show ip rpf 10.255.0.11
show ip rpf 10.255.0.100
show ip msdp summary
show ip msdp peer
show ip msdp sa-cache
```

| Verificação | Procurar |
|---|---|
| OSPF/RPF | interface e vizinho corretos para source/RP |
| PIM | vizinhos e RP Mapping |
| ASM | `(*,G)`, `(S,G)`, flag `T` |
| SSM | `(S,G)`, flags `sTI`, contadores |
| BIDIR | `(*,G)`, flag `B`, eleição DF |
| MSDP | Peer Up, SA Cache e mudanças de RP |
| Data Plane | contadores crescentes e ausência de RPF failures |

Antes de publicar novos backups, remover segredos e dados reais de produção.
