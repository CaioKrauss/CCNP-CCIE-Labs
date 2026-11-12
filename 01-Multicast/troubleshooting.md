# Validação e troubleshooting — PIM Sparse Mode

Este roteiro distingue **configuração**, **estado de controle** e **encaminhamento efetivo**. Não concluir que há entrega de pacotes apenas porque uma rota multicast existe.

## 1. Unicast / RPF
```cisco
show ip ospf neighbor
show ip route 10.255.0.1
show ip route 10.255.0.11
show ip rpf 10.255.0.11
```
Conferir adjacências OSPF, alcance do RP e caminho RPF até a fonte. O RPF deve apontar para a interface que leva à origem do pacote multicast, conforme a tabela unicast/MRIB.

## 2. PIM e RP
```cisco
show ip pim neighbor
show ip pim interface
show ip pim rp mapping
```
Confirmar vizinhanças em cada enlace de trânsito, interfaces com PIM habilitado e mapeamento do grupo para RP 10.255.0.1.

## 3. IGMP e árvore compartilhada
```cisco
show ip igmp groups
show ip mroute 239.1.1.1
```
Em CE2 e CE3, verificar o grupo 239.1.1.1 em Fa0/0. Na árvore `(*,G)`, conferir interface de entrada/RPF para o RP e lista de interfaces de saída (OIL) rumo aos receptores.

## 4. Fonte, Register e SPT
```cisco
show ip mroute 239.1.1.1
show ip mroute count
show ip rpf 10.255.0.11
```
Gerar tráfego de teste a partir da fonte prevista e observar evolução dos estados `(*,G)` e `(S,G)`, flags pertinentes e contadores. Se o equipamento/imagem oferecer comandos de depuração de PIM Register, utilizá-los com cautela em ambiente de laboratório.

**Não confundir:** o flag `T` indica SPT-bit no IOS; o simples aparecimento de `(S,G)` não é, isoladamente, comprovação de que todo o caminho de dados foi comutado para a SPT. Comparar IIF/OIL, RPF e contadores em diferentes nós.

## 5. Testes de falha
- Desligar uma interface de trânsito em ambiente de lab e registrar efeito sobre OSPF, PIM e mroute.
- Restaurar a interface e medir convergência.
- Alterar temporariamente uma condição de RPF e comparar comportamento, salvando a baseline antes.
- Como a topologia não tem redundância, falhas de enlace podem interromper completamente o serviço; não esperar reroute.

## Registro recomendado
Para cada teste, salvar data/hora, roteador, comandos, saída relevante, hipótese, resultado observado e conclusão. Preservar logs completos localmente e publicar apenas trechos revisados, sem segredos.

## Checklist
- [ ] Vizinhanças OSPF/PIM em todos os enlaces
- [ ] Mapeamento RP consistente
- [ ] IGMP de CE2/CE3 verificado
- [ ] `(*,239.1.1.1)` e OIL observados
- [ ] Tráfego real enviado e contadores incrementando nos receptores
- [ ] `(S,G)` e SPT avaliados com evidências
- [ ] Falha induzida, diagnóstico e recuperação documentados
