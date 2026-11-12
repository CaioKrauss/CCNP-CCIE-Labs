# Laboratório 01 — Multicast IPv4 com PIM Sparse Mode

## Objetivo
Estudar e validar PIM-SM em uma topologia Cisco IOS de sete roteadores: formação de vizinhanças, descoberta de RP estático, IGMP, árvore compartilhada (*,G), estado (S,G), RPF e comportamento do SPT.

> **Baseline:** configuração exportada dos sete roteadores em 12/11/2026. Este laboratório usa endereços privados de estudo. Os backups integrais não são publicados.

## Topologia
```text
CE1 -- PE1 -- RR-P -- PE2 -- CE2
                 |
                 +----- PE3 -- CE3
```
- **CE1:** lado da fonte multicast prevista (Loopback0 10.255.0.11).
- **CE2 e CE3:** receptores locais, com `ip igmp join-group 239.1.1.1` nas interfaces de acesso.
- **RR-P:** ponto central físico e RP estático em 10.255.0.1. O nome RR-P **não implica** BGP Route Reflector configurado neste laboratório.
- **PE1, PE2 e PE3:** trânsito multicast entre CEs e core.
- **IGP:** OSPF processo 1, área 0, em todos os roteadores.
- **PIM:** Sparse Mode nas interfaces de trânsito; Loopback0 também habilitada para PIM no CE1 e RR-P.
- **RP:** `ip pim rp-address 10.255.0.1` nos sete roteadores.

Consulte [endereçamento e enlaces](topology/enderecamento.md) para interfaces e sub-redes.

## Conceitos e fluxo esperado
1. CE2 e CE3 solicitam o grupo `239.1.1.1` com `ip igmp join-group`.
2. Os roteadores enviam PIM Join em direção ao RP, seguindo a informação de roteamento unicast usada no RPF.
3. A árvore compartilhada `(*,239.1.1.1)` pode apresentar interfaces de saída para os ramos dos receptores.
4. Quando há tráfego real da fonte, o DR de origem pode encapsular pacotes PIM Register para o RP. Os estados `(S,G)` e o eventual switchover para SPT devem ser verificados com comandos e contadores; não presumir a transição apenas pela presença de entradas.
5. A topologia física tem caminho único. Alterar custos OSPF, sem adicionar enlaces, não cria caminho alternativo.

## Configuração-base (trechos verificados)
```cisco
! Todos os roteadores
ip multicast-routing
router ospf 1
 network 10.0.0.0 0.255.255.255 area 0
ip pim rp-address 10.255.0.1

! CE2, FastEthernet0/0; CE3, FastEthernet0/0
ip pim sparse-mode
ip igmp join-group 239.1.1.1
```
Cada roteador possui `router-id` OSPF correspondente à Loopback0; veja a tabela de endereçamento. Os trechos acima são exemplos documentais, não um script para aplicar indiscriminadamente em interfaces.

## Verificação operacional
```cisco
terminal length 0
show ip interface brief
show ip ospf neighbor
show ip pim neighbor
show ip pim rp mapping
show ip igmp groups
show ip mroute
show ip rpf 10.255.0.11
show ip route 10.255.0.1
```
**Importante:** `show ip rpf 10.255.0.11` verifica o RPF para a fonte prevista; o RPF para o RP deve ser avaliado separadamente quando pertinente. A existência de estado `(*,G)` ou `(S,G)` não substitui testes de encaminhamento e contadores.

## Evidências e próximos testes
- Foram realizados testes de coleta via console Telnet/Dynamips e disponibilizados outputs de PIM, IGMP, mroute e RPF.
- A configuração dos sete roteadores foi exportada e conferida.
- Ainda é necessário preservar evidência reprodutível de **tráfego multicast efetivamente recebido** e de **SPT switchover** antes de marcar essas validações como concluídas.
- Consulte [roteiro de validação e troubleshooting](troubleshooting.md).

## Segurança e reutilização
Os backups `show running-config` completos permanecem locais: podem conter segredos e não devem ser enviados automaticamente ao GitHub. Para novos labs, reutilizar a topologia-base e modificar enlaces somente quando o tema exigir redundância.

## Progresso
- [x] Topologia e plano de endereçamento documentados
- [x] Configuração-base analisada
- [x] Coleta automatizada de outputs testada
- [ ] Evidência de entrega de pacotes multicast e contadores
- [ ] Evidência do switchover RPT → SPT
- [ ] Troubleshooting com falha induzida e recuperação
