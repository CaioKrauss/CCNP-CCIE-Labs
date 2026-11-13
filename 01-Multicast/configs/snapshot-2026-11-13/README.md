# Snapshot pós-LAB05 — 13/11/2026

Origem: sete arquivos `.cfg` anexados pelo usuário (nomes originais com sufixo `(2)`). Conteúdo preservado integralmente; apenas os nomes foram normalizados. Não foi executado o script Python, não houve nova coleta nem reinicialização da VM. O horário de `Last configuration change` é do roteador, não o horário de coleta.

## Revisão de segurança

Leitura integral e busca por senhas/segredos, usuários, comunidades SNMP, chaves, certificados, AAA/RADIUS/TACACS, URLs e identificadores pessoais. Nenhum segredo ou dado pessoal foi identificado; nenhuma redação foi necessária. Endereços unicast IPv4 em 10.0.0.0/8 e IPv6 em 2001:DB8::/32; demais grupos são multicast de laboratório. Configurações destinam-se ao laboratório: a ausência de credenciais publicadas não constitui validação de endurecimento de acesso.

## Conferência estática

- Sete arquivos com hostname esperado e término `end`, sem marcador de paginação ou erro de comando.
- IPv6 unicast-routing, multicast-routing e CEF presentes em todos.
- OSPFv3 processo 10, área 0 nos enlaces e Loopback0; router-ids distintos e Loopback0 passiva.
- Seis enlaces com endereços /64 coerentes entre as pontas; loopbacks /128 distintas.
- RP estático 2001:DB8:100::1 em todos; endereço presente em RR-P Loopback0.
- CE2 e CE3: `ipv6 mld join-group FF1E::1234` e `ipv6 mld join-group FF3E::1234 2001:DB8:1::1`. O IOS salva o segundo comando sem a palavra `include`.
- CE1: fonte 2001:DB8:1::1/64 presente; endereço temporário 2001:DB8:1::99/64 ausente.
- Configurações IPv4 dos labs anteriores preservadas. Divergência legada: CE2 solicita SSM IPv4 232.1.1.1 de 10.255.0.11; CE3 solicita o mesmo grupo de 10.0.1.1. Não alterada nesta revisão do LAB05 IPv6.

Os arquivos comprovam configuração presente no snapshot, não estado operacional atual, persistência em startup-config ou novos testes de tráfego. MLDv2 e resultados de ASM/SSM permanecem fundamentados nas [evidências de console](../../evidencias/LAB05-IPv6-PIM-MLDv2.txt); MLDv1 não foi testado.

## Integridade SHA-256

Hashes dos bytes originais, incluindo CRLF.

| Arquivo | SHA-256 |
|---|---|
| [CE1.cfg](CE1.cfg) | `fced1e4fe38b14c20ef8f6ef479de0cca94fefb07d3024925a74c3aef5e76a9d` |
| [CE2.cfg](CE2.cfg) | `bc4e7bba47dd029571427ff53172603f7b1d849ab5319aae84d67134aa6a2bf8` |
| [CE3.cfg](CE3.cfg) | `bfc1970037f30a841ab93873adc1e5f3083489324f865ee05be094444fc9b147` |
| [PE1.cfg](PE1.cfg) | `b6857ba7531aa15c4742d8423fbda4ae3a1ed78af6334c4fd5253443a0f0b5dc` |
| [PE2.cfg](PE2.cfg) | `c9aa42dd87c3e641618d1952f030c3f7a9c941631486f0a0b0ac49159eac2205` |
| [PE3.cfg](PE3.cfg) | `6883aee80e50e04572ea616ee866015e28f586b1a92cf240dc89289956cff23d` |
| [RR-P.cfg](RR-P.cfg) | `33b34cf49071d719929fb6f973ee7a6c8a8d07fa9c744a9af5dae6708293e975` |
