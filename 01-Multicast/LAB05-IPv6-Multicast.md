# LAB 05 — Multicast IPv6: OSPFv3, PIM-SM, MLDv2 e SSM

**Data do teste:** 13/11/2026 · **Equipamentos:** Cisco IOS (EVE-NG), CE1/CE2/CE3, PE1/PE2/PE3 e RR-P.  
**Status:** ASM IPv6 e SSM IPv6 validados com MLDv2. MLDv1 não foi testado.

> Evidências operacionais obtidas de saídas reais enviadas na conversa. Os sete backups pós-LAB05 foram entregues pelo usuário e revisados em 13/11/2026: [snapshot-2026-11-13](configs/snapshot-2026-11-13/). O [snapshot-2026-11-12](configs/snapshot-2026-11-12/) permanece como histórico anterior ao IPv6.

## Objetivos

1. Estabelecer conectividade IPv6/OSPFv3 por toda a topologia, preservando IPv4.
2. Validar ASM IPv6 `FF1E::1234`, RP estático em RR-P, MLD Join e PIM-SM.
3. Validar SSM IPv6 `FF3E::1234`, MLDv2 `INCLUDE` com uma fonte e tráfego nos dois receptores.
4. Comparar fonte autorizada x não autorizada.

## Topologia e endereçamento

```text
CE1--PE1--RR-P--PE2--CE2
          |
          +--PE3--CE3
```

| Nó / Enlace | IPv6 |
|---|---|
| CE1 Lo0 | 2001:DB8:100::11/128 |
| PE1 Lo0 | 2001:DB8:100::12/128 |
| RR-P Lo0 / RP ASM | 2001:DB8:100::1/128 |
| PE2 Lo0 | 2001:DB8:100::23/128 |
| CE2 Lo0 | 2001:DB8:100::22/128 |
| PE3 Lo0 | 2001:DB8:100::33/128 |
| CE3 Lo0 | 2001:DB8:100::32/128 |
| CE1—PE1 | 2001:DB8:1::/64 (CE1 ::1 / PE1 ::2) |
| PE1—RR-P | 2001:DB8:12::/64 |
| RR-P—PE2 | 2001:DB8:23::/64 |
| PE2—CE2 | 2001:DB8:2::/64 (CE2 ::2) |
| RR-P—PE3 | 2001:DB8:34::/64 |
| PE3—CE3 | 2001:DB8:3::/64 (CE3 ::2) |

**Roteamento:** `ipv6 unicast-routing`, `ipv6 cef`, OSPFv3 processo 10 / área 0, router-id IPv4 derivado de Lo0, `ipv6 ospf 10 area 0` nas interfaces de trânsito/loopbacks.

## 05.0 — OSPFv3 e conectividade

- RR-P: vizinhos PE3 `10.255.0.33 FULL/BDR` em Eth1/0, PE2 `10.255.0.23 FULL/DR` em Eth1/1, PE1 `10.255.0.12 FULL/DR` em Eth1/2.
- RR-P aprende `2001:DB8:100::11/128`, `::12/128`, `::22/128`, `::23/128`, `::32/128`, `::33/128` e redes de trânsito via OSPFv3; next-hops link-local `FE80::/10`.
- CE1 ↔ PE1: adjacência FULL/BDR, ping CE1 Lo0 → PE1 Lo0 **5/5**.
- CE3 Lo0 → CE2 Lo0: ping **5/5**.

## 05.1 — ASM IPv6 (PIM-SM + MLD)

**Grupo:** `FF1E::1234` · **RP:** `2001:DB8:100::1` (RR-P) · **fonte efetiva:** `2001:DB8:1::1` (CE1 Fa0/0) · **receptores:** CE2 e CE3.

Trechos de configuração usados:

```cisco
! Todos os roteadores, com interfaces IPv6 previamente configuradas:
ipv6 multicast-routing
ipv6 pim rp-address 2001:DB8:100::1

! CE2 / CE3 na interface de acesso:
interface FastEthernet0/0
 ipv6 mld join-group FF1E::1234
```

**Evidências:**
- RR-P: 3 vizinhos PIM IPv6 (PE1/PE2/PE3); `show ipv6 pim group-map FF1E::1234` retorna `SM, RP: 2001:DB8:100::1`, static.
- CE3: MLD habilitado, **Current MLD version is 2**; `(*,FF1E::1234)` `SCLJ`, RPF para PE3, OIL Null (receptor local).
- RR-P: `(*,G)` com OIL **Ethernet1/0 → PE3** e **Ethernet1/1 → PE2**, IIF Tunnel6 (RP local).
- PE3: `(*,G)` `SC` com Fa0/0 IIF e Fa1/0 OIL; depois `(2001:DB8:1::1,FF1E::1234)` `ST` com mesmas IIF/OIL.
- Primeiro ping com source **Loopback0 `2001:DB8:100::11`** teve timeouts, causa não isolada. Ping com source **Fa0/0 `2001:DB8:1::1`** respondeu **5/5, 11 multicast replies**, vindas de CE2 `2001:DB8:2::2` e CE3 `2001:DB8:3::2`.
- PE1: `(S,G)` flags `SFT`, Fa1/0 IIF, Fa0/0 OIL. RR-P: `(S,G)` flags `ST`, Eth1/2 IIF; RR-P `show ipv6 pim traffic`: **Data Register Received 3**, **Null Register Received 1**, **Register-Stop Sent 2**. PE1 recebeu 2 Register-Stops.

**Ressalva:** contador `Packet Sent on Loopback Errors` no PIM subiu até 33 em PE1/RR-P; não foi demonstrado vínculo causal com perda de tráfego. A saída `(S,G)` do RR-P mostrou apenas Eth1/1, apesar da OIL de `(*,G)` incluir Eth1/0/Eth1/1; PE3 possuía `(S,G)` com OIL rumo a CE3.

## 05.2 — SSM IPv6 (MLDv2 source-specific)

**Grupo:** `FF3E::1234` · **fonte permitida:** `2001:DB8:1::1` · **sem RP nem PIM Register**.

```cisco
! CE2 e CE3 / interface de acesso
interface FastEthernet0/0
 ipv6 mld join-group FF3E::1234 2001:DB8:1::1

! Verificações
show ipv6 mld interface FastEthernet0/0
show ipv6 mld groups
show ipv6 mroute FF3E::1234
show ipv6 mroute FF3E::1234 count
```

**Sintaxe efetivamente salva:** os backups de CE2 e CE3 mostram o comando acima sem a palavra `include`. INCLUDE descreve o filtro de fonte observado nos testes; o trecho foi ajustado para reproduzir literalmente o running-config.

Evidências: CE2/CE3 possuem inscrição para `FF3E::1234`. PE2 e PE3 instalaram `(2001:DB8:1::1,FF3E::1234)` flags **sTI**, com IIF Fa0/0 e OIL Fa1/0. RPF de PE2 para RR-P via `FE80::C806:1EFF:FEB0:1D`; PE3 via `FE80::C806:1EFF:FEB0:1C`. O CE2 apresentou `sPLTI` com OIL Null (receptor local). Ping SSM via CE1 Fa0/0: **5/5, 10 multicast replies**, cinco de cada receptor.

Os contadores no CE2 tinham `SW Forwarding 0` e `Other drops` 3→4→5 com `RPF failed 0`, coerentes com OIL Null do receptor. No PE2 foi observado posteriormente `SW Forwarding 8`, `Other 0/0/0` para a fonte autorizada.

## 05.3 — Teste de filtragem de fontes (MLDv2 INCLUDE)

Segundo endereço **temporário** configurado em CE1 Fa0/0:

```cisco
interface FastEthernet0/0
 ipv6 address 2001:DB8:1::99/64
```

| Teste | Resultado observado |
|---|---|
| `ping ipv6 FF3E::1234 source 2001:DB8:1::99 repeat 5` | **0/5**, nenhum receptor respondeu |
| `ping ipv6 FF3E::1234 source 2001:DB8:1::1 repeat 5` | **5/5**, 10 respostas: CE2 e CE3 |

**Conclusão:** o teste positivo/negativo é consistente com o filtro INCLUDE em MLDv2. Não foi apresentada uma captura simultânea de pacotes descartados para a origem `::99`; não atribuir o timeout a um ponto exato da rede sem essa evidência.

## Comandos rápidos

```cisco
show ipv6 ospf neighbor
show ipv6 route ospf
show ipv6 pim neighbor
show ipv6 pim interface
show ipv6 pim group-map FF1E::1234
show ipv6 mld interface FastEthernet0/0
show ipv6 mld groups
show ipv6 mroute FF1E::1234
show ipv6 mroute FF3E::1234
show ipv6 mroute FF3E::1234 count
show ipv6 rpf 2001:DB8:1::1
show ipv6 pim traffic
```

## Pendências / próximos passos

- **MLDv1 não validado:** `ipv6 mld ?` não exibiu comando `version` na imagem IOS; a versão observada foi MLDv2.
- **Limpeza confirmada no running-config recebido:** CE1 Fa0/0 contém somente `2001:DB8:1::1/64`; `2001:DB8:1::99/64` está ausente. Os arquivos não comprovam gravação em startup-config.
- **Backups pós-LAB05 recebidos e revisados:** sete hostnames corretos, arquivos terminando em `end`, IPv6 unicast/multicast/CEF, OSPFv3 10 área 0, Loopback0 passiva e RP `2001:DB8:100::1` nos sete nós; endereços dos seis enlaces compatíveis entre pares. CE2/CE3 mantêm joins ASM e SSM. Validação estática; não foram executados novos testes de rede nem o script Python, e a VM não foi reiniciada.
- Investigar, caso desejado, o motivo do timeout com origem Loopback0 e contador de loopback PIM.
- LAB 06: mVPN/MPLS (se suportado pelas imagens de roteador disponíveis).

**Observação de segurança:** o repositório é público; publicar novos `show running-config` apenas depois de inspecionar credenciais e outras informações sensíveis.
