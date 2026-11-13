# Configurações observadas — L3VPN CUST-A

Coleta direta dos consoles em 13/11/2026, aproximadamente às 15:43, America/Sao_Paulo. Estes arquivos representam o estado encontrado; não são configurações recém-aplicadas.

- Nove arquivos: running/startup de CE1_A, CE2_A, R1 e R3; running do XR1.
- Comandos efetivos de running e startup equivalentes nos quatro equipamentos IOS, ignorando comentários e cabeçalhos.
- XR1: configuração ativa com histórico de commits existente. Último commit listado: 1000000019. Não houve novo commit nem teste de reboot.
- Removidos apenas eco do comando, cabeçalhos externos à configuração e prompt final. Quebras de linha normalizadas para LF; cada arquivo termina com LF.
- A configuração do XR não inclui credenciais locais na saída coletada. Estes snapshots não são um pacote completo de instalação ou autenticação da imagem.
- Revisão não identificou senhas, hashes de senha, chaves privadas, tokens ou dados de clientes de produção no conteúdo publicado. Endereços de gerenciamento do EVE e portas de console não foram incluídos.
- Os endereços são do cenário de laboratório, incluindo loopbacks em faixas públicas; não devem ser anunciados fora dele.
- Nenhum equipamento L2 foi configurado ou renomeado nesta validação L3VPN.

As [evidências de CLI](../../evidencias/LAB01-L3VPN-2026-11-13/) preservam as saídas completas revisadas. Os hashes em SHA256SUMS.txt referem-se aos bytes UTF-8/LF publicados, não a arquivos anteriores à normalização.
