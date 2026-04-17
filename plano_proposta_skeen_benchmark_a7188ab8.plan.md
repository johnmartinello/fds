---
name: Plano Proposta Skeen Benchmark
overview: Plano para preencher [proposta.md](proposta.md) cobrindo as cinco seções exigidas (apresentação do artigo, resumo, objetivo/metodologia, requisitos e impacto), com foco em um benchmark empírico comparando o Skeen clássico contra o Skeen estendido com atomic global order (Algoritmo 1 do paper) e a variante byzantina, usando o protótipo em [skeen/](skeen/).
todos:
  - id: artigo-ficha
    content: Expandir Referencial Teórico com ficha completa do artigo (autores, evento completo LADC 2022 Fortaleza, DOI, link, citações)
    status: completed
  - id: resumo-artigo
    content: "Escrever Resumo do Artigo: problema de linearizabilidade em partitioned SMR, contribuição (atomic global order + extensão Skeen via ack) e o fato de o paper ser teórico (sem avaliação experimental)"
    status: completed
  - id: abstract
    content: Redigir Abstract da proposta sintetizando objetivo de validar empiricamente a extensão proposta no paper via benchmark
    status: completed
  - id: metodologia
    content: "Detalhar Metodologia: compilação ant, matriz de parâmetros (algo 0/1/2, locality, clis, servers, msgs), workloads TPC-C e key-value com range queries (cenário da Figura 2), coleta via getResults.sh/results.py"
    status: completed
  - id: requisitos
    content: Subseção de Requisitos para Reprodução com status de disponibilidade (paper, código, configs, TPC-C, equipamentos, plano B sem Cloudlab)
    status: completed
  - id: impacto
    content: Seção de Impacto e Conexão com a Sociedade (bancos, blockchains, serviços críticos, coordenação extra custa latência ao usuário final)
    status: completed
  - id: referencias
    content: "Popular Referências seguindo o próprio paper: Pacheco/Dotti/Pedone 2022, Birman & Joseph 1987 (Skeen), Bezerra/Pedone/Van Renesse 2014 (S-SMR), Coelho et al. 2018 (Byzcast), TPC-C, repositório do protótipo"
    status: completed
  - id: revisao
    content: Revisar com o grupo e orientador; validar número de citações no Google Scholar na data da entrega
    status: completed
isProject: false
---

## Contexto identificado

- Grupo: Agatha Schneider, Fernando Vieira, Gustavo Flores, João Lucas Martinello de Oliveira, Rodrigo Fehlauer Lauermann. Orientador: Fernando Dotti.
- Tema escolhido (ver [diario.md](diario.md) linhas 26-27 e 44): avaliação de variantes do algoritmo de multicast atômico a partir do paper "Strengthening Atomic Multicast for Partitioned State Machine Replication" (Pacheco, Dotti, Pedone — LADC 2022), cujo texto completo está em [paper.md](paper.md).
- Código-fonte em [skeen/](skeen/): protótipo Java (Ant + Netty), cliente TPC-C ([MojtabasTpccClient.java](skeen/src/util/MojtabasTpccClient.java)), implementação do Skeen em [SkeenNode.java](skeen/src/skeen/SkeenNode.java) e scripts [runLocal.sh](skeen/scripts/runLocal.sh) / [runCloudlab.sh](skeen/scripts/runCloudlab.sh).
- O [runLocal.sh](skeen/scripts/runLocal.sh) (linha 2) expõe a flag `-a` com três algoritmos: `0-flex`, `1-skeen`, `2-byz` — justamente o trio que entrará no benchmark. A hipótese de trabalho é que `0-flex` corresponda à extensão com atomic global order descrita no paper (Algoritmo 1, adições em cinza) e `2-byz` a Byzcast [ref. 7 do paper]; confirmar lendo o código antes da redação final.
- Ponto crítico identificado ao ler [paper.md](paper.md): o artigo é **puramente teórico**. Seções 3 e 4 provam que o multicast atômico com global total order não basta para linearizabilidade em partitioned SMR e apresentam uma modificação do Skeen (um ack extra, linhas em cinza do Algoritmo 1 em [paper.md](paper.md) linhas 500-527). Não há seção de avaliação experimental. Logo, **o benchmark do grupo é a validação empírica inédita da extensão**, e isso deve ser explicitado como motivação na proposta.
- A proposta atual em [proposta.md](proposta.md) já traz Abstract, Introdução, Referencial Teórico, Metodologia e Referências — o plano reusa essa estrutura.

## Mapeamento das exigências do enunciado para as seções

- Apresentação dos dados do artigo -> "Referencial Teórico" (expandir a ficha).
- Resumo do artigo -> "Introdução" (reforçar) + novo bloco "Resumo do Artigo".
- Descrição do objetivo e metodologia -> "Metodologia" (redesenhar com matriz experimental).
- Levantamento de requisitos -> nova subseção "Requisitos para Reprodução" dentro de Metodologia.
- Reflexão sobre impacto e sociedade -> nova seção "Impacto e Conexão com a Sociedade" antes das Referências.
- Referências -> ampliar com citações principais do paper.

## Conteúdo detalhado por seção

### 1. Apresentação dos dados do artigo (Referencial Teórico)

Ficha, com dados confirmados no [paper.md](paper.md) linhas 37-42 e 57:

- Título: Strengthening Atomic Multicast for Partitioned State Machine Replication.
- Autores: Leandro Pacheco (USI, Suíça), Fernando Dotti (Escola Politécnica, PUCRS - Brasil), Fernando Pedone (USI, Suíça).
- Evento: 11th Latin-American Symposium on Dependable Computing (LADC 2022), 21-24 de novembro de 2022, Fortaleza, CE, Brasil.
- Publicação: Proceedings of LADC 2022, ACM, New York, NY, USA, 10 páginas.
- DOI citado no paper: `10.1145/nnnnnnn.nnnnnnn` (placeholder no PDF); DOI real na ACM Digital Library: `10.1145/3569902.3569909`.
- Link: https://dl.acm.org/doi/10.1145/3569902.3569909.
- Citações: 6 (Google Scholar, conforme [proposta.md](proposta.md) linha 6) — revalidar na data da entrega.
- Financiamento reconhecido (seção ACKNOWLEDGMENTS): CNPq, FAPERGS e PUCRS-PrInt/CAPES para Fernando Dotti.

### 2. Resumo do artigo

Três parágrafos, estruturados a partir do conteúdo do [paper.md](paper.md):

- **Problema**: Em partitioned state machine replication (sharding + SMR), ordenar requisições consistentemente através de multicast atômico não é suficiente para garantir linearizabilidade. Ainda que o multicast forneça global total order + prefix order (Hadzilacos & Toueg), existem execuções (Figura 2 esquerda do paper, [paper.md](paper.md) linhas 346-365) em que uma range query `r(0,1)` e inserções `w(0,v0)`, `w(1,v1)` produzem um resultado não linearizável. Para contornar, sistemas como S-SMR introduzem uma fase ad-hoc de "signal messages" entre partições ([paper.md](paper.md) linhas 371-378).
- **Contribuição**: (i) Prova formal de que atomic multicast com global total order exige coordenação adicional entre réplicas para linearizabilidade ([paper.md](paper.md) Seção 3.1). (ii) Definição de uma propriedade mais forte, **atomic global order**, que captura dependências de tempo real entre multicast e deliver ([paper.md](paper.md) linhas 392-396). (iii) Extensão do protocolo de Skeen [Birman & Joseph 1987] com um passo extra de `ack`: cada processo, após decidir o final timestamp de uma mensagem `m`, envia ack aos demais destinos e só faz deliver quando tiver coletado todos os acks ([paper.md](paper.md) Algoritmo 1, linhas 500-527, adições em cinza; argumento de correção em linhas 570-581). (iv) Observa que a extensão se aplica a diversos descendentes do Skeen (FastCast, Scalatom, White-Box Atomic Multicast, RamCast, Byzcast) e que, dentre os protocolos revisados, só o protocolo round-based de [Schiper & Pedone 2008] já satisfaz a propriedade.
- **Resultados**: Contribuição teórica (provas de correção). **O paper não apresenta avaliação experimental**: Seção 5 é related work e Seção 6 é conclusão, onde os autores deixam em aberto se é possível uma propriedade intermediária entre global total order e atomic global order ([paper.md](paper.md) linhas 919-931). Isso posiciona o nosso benchmark como contribuição complementar natural.

### 3. Objetivo do trabalho e metodologia

**Objetivo**: realizar a validação empírica da extensão proposta no paper, comparando em um mesmo protótipo ([skeen/](skeen/)) o desempenho de:

- (A) Skeen clássico (`-a 1`) — baseline sem atomic global order.
- (B) Skeen estendido com atomic global order / "flex" (`-a 0`) — implementa o passo de ack adicional do Algoritmo 1.
- (C) Variante byzantina (`-a 2`) — Byzcast, para comparação com um protocolo de classe de falhas diferente.

**Questões de pesquisa** que o benchmark deve responder:

1. Qual o custo (latência, throughput) do ack extra do atomic global order em relação ao Skeen clássico?
2. Como esse custo varia com a taxa de mensagens multi-partição (parâmetro `%locality` de [runLocal.sh](skeen/scripts/runLocal.sh))?
3. Como o custo escala com o número de partições/servidores e de clientes?
4. Como o Byzcast se compara em cenários equivalentes (tolerância a falhas vs. latência)?

**Metodologia em passos**:

1. Leitura cruzada do paper + código: mapear as adições em cinza do Algoritmo 1 às classes em [skeen/src/skeen/](skeen/src/skeen/) — em particular `receiveStep1Msg` e `receiveStep2Msg` em [SkeenNode.java](skeen/src/skeen/SkeenNode.java) — e confirmar em qual classe mora o "flex".
2. Compilar o projeto via `ant` (ver [build.xml](skeen/build.xml)); validar execução local mínima.
3. Definir **matriz experimental** usando os parâmetros do [runLocal.sh](skeen/scripts/runLocal.sh) (linhas 12-18): `duration` (ex.: 60s), `algo in {0, 1, 2}`, `#clis in {1, 4, 16, 64}`, `#servers in {2, 3, 4}`, `%locality in {0, 25, 50, 75, 100}`, `#msgs` fixo, `#exp >= 3` para média e desvio.
4. Executar **duas cargas**:
   - TPC-C embutida ([MojtabasTpccClient.java](skeen/src/util/MojtabasTpccClient.java)) — carga realista.
   - Key-value com range queries — reproduzindo o cenário da Figura 2 do paper ([paper.md](paper.md) linhas 316-324), onde o problema de linearizabilidade aparece claramente. Se a carga não estiver pronta no código, criar um cliente mínimo análogo.
5. Rodar localmente para shakedown e depois migrar para ambiente geo-distribuído via [runCloudlab.sh](skeen/scripts/runCloudlab.sh). Plano B se Cloudlab não estiver disponível: emular latência entre VMs/processos com `tc netem` em máquina única.
6. Coletar métricas com [getResults.sh](skeen/scripts/getResults.sh) e [results.py](skeen/scripts/results.py); instrumentar throughput (msgs/s), latência média e percentis (p50/p95/p99) e custo de mensagens via [Stats.java](skeen/src/util/Stats.java).
7. Produzir gráficos comparativos: latência vs. `%locality`, throughput vs. `#clis`, escalabilidade vs. `#servers`.
8. Discutir overhead observado à luz do paper: Skeen original precisa de ~3 passos (start, local-ts, delivery); a extensão acrescenta 1 passo de ack — esperar aumento de latência ordem-da-grandeza de 33%, mas validar empiricamente.

Fluxo experimental resumido:

```mermaid
flowchart LR
    paper[paper.md Algoritmo 1] --> map[Mapear extensao no codigo skeen/]
    map --> build[ant build]
    build --> runLocal[runLocal.sh algo 0/1/2]
    runLocal --> logs[logs txt por nodo e cliente]
    logs --> getResults[getResults.sh]
    getResults --> resultsPy[results.py]
    resultsPy --> plots[Graficos: latencia, throughput, escalabilidade]
    plots --> discussao[Discussao vs. paper]
```

### 4. Levantamento de requisitos para reprodução

Listar em bullets com status (disponível / a recriar) e URL quando houver:

- Paper: **disponível** — [paper.md](paper.md) local e ACM DL (https://dl.acm.org/doi/10.1145/3569902.3569909).
- Código-fonte do protótipo: **disponível** em [skeen/](skeen/) (repositório git já clonado, ver [skeen/.git/config](skeen/.git/config) para URL remota).
- Dependências Java: **disponíveis** — JDK 8+ e Apache Ant (ver `source="1.8"` em [build.xml](skeen/build.xml) linha 19); bibliotecas Netty em `skeen/lib/` (conferir versões e listar no README da proposta).
- Workload TPC-C: **disponível** embutida em [MojtabasTpccClient.java](skeen/src/util/MojtabasTpccClient.java); não requer dataset externo.
- Workload key-value com range queries (cenário da Figura 2 do paper): **a recriar** se não estiver presente — cliente mínimo que multicasta inserts e range queries a 2 partições.
- Arquivos de configuração: **disponíveis** em [skeen/config/](skeen/config/) — [hosts.config](skeen/config/hosts.config), [servers.conf](skeen/config/servers.conf), [clients.conf](skeen/config/clients.conf), [locality.conf](skeen/config/locality.conf); precisam ser ajustados para a topologia de cada experimento.
- Scripts: **disponíveis** — [runLocal.sh](skeen/scripts/runLocal.sh), [runCloudlab.sh](skeen/scripts/runCloudlab.sh), [getResults.sh](skeen/scripts/getResults.sh), [results.py](skeen/scripts/results.py), [killAll.sh](skeen/scripts/killAll.sh), [sshserver.sh](skeen/scripts/sshserver.sh), [sshcli.sh](skeen/scripts/sshcli.sh).
- Equipamentos:
  - Local: **disponível** — máquina do grupo com multi-core para 2-4 servidores + clientes.
  - Geo-distribuído: **a recriar/solicitar** — acesso ao Cloudlab (solicitar via orientador) ou conjunto de VMs em laboratório/nuvem com `tc netem` para emular latência WAN.
- Ambiente Python para [results.py](skeen/scripts/results.py): **a verificar** — rodar `results.py` e listar dependências (numpy, matplotlib, pandas provavelmente); documentar `requirements.txt` no repositório da proposta.
- Documentação de reprodução (README com passo a passo dos experimentos): **a criar** pelo grupo.

### 5. Impacto e conexão com a sociedade

Texto curto (2 parágrafos):

- **Por que importa**: serviços que sustentam a sociedade moderna — bancos, sistemas de pagamento (Pix), prontuários eletrônicos, identidade digital (gov.br), blockchains e bancos de dados em nuvem — dependem de replicação particionada para escalar com tolerância a falhas. O [diario.md](diario.md) linhas 42-61 já traz a motivação (bancos, saldos, risco de inconsistência). O paper mostra que, sem uma propriedade como atomic global order, cada requisição multi-partição carrega uma coordenação adicional silenciosa que se traduz em **latência extra para o usuário final** e **custo energético/infraestrutura** para o provedor.
- **Contribuição social do benchmark**: medir o custo real dessa coordenação permite que projetistas de sistemas críticos tomem decisões informadas sobre quando vale trocar o Skeen clássico pela versão estendida, potencialmente reduzindo latência em operações sensíveis (transferências bancárias, autorizações de saúde) e consumo energético de data centers. Além disso, o trabalho é um exercício formativo em pesquisa reprodutível em sistemas distribuídos dentro do estado da arte nacional (autor orientador do paper é o orientador do grupo).

### 6. Referências

Citar, no mínimo:

- Pacheco, L.; Dotti, F.; Pedone, F. (2022). Strengthening Atomic Multicast for Partitioned State Machine Replication. LADC 2022, ACM. DOI 10.1145/3569902.3569909.
- Birman, K. P.; Joseph, T. A. (1987). Reliable Communication in the Presence of Failures. ACM TOCS 5(1). — Skeen original, ref. [5] do paper.
- Bezerra, C. E.; Pedone, F.; Van Renesse, R. (2014). Scalable State-Machine Replication. DSN. — S-SMR, ref. [4].
- Coelho, P.; Ceolin Jr., T.; Bessani, A.; Dotti, F.; Pedone, F. (2018). Byzantine Fault-Tolerant Atomic Multicast. DSN. — Byzcast, ref. [7].
- Hadzilacos, V.; Toueg, S. (1994). A Modular Approach to Fault-Tolerant Broadcasts. — taxonomia, ref. [20].
- Herlihy, M.; Wing, J. (1990). Linearizability. ACM TOPLAS 12(3). — ref. [21].
- Lamport, L. (1978). Time, Clocks, and the Ordering of Events in a Distributed System. CACM 21(7). — ref. [22].
- TPC Benchmark C (TPC-C) specification — http://www.tpc.org/tpcc/.
- Repositório do protótipo (URL do git em [skeen/.git/config](skeen/.git/config)).

## Próximos passos sugeridos (ordem de edição)

1. Mapear no código skeen/ quem é "flex" (hipótese: o Skeen estendido do Algoritmo 1) e registrar no diário/proposta.
2. Expandir "Referencial Teórico" com a ficha completa do artigo.
3. Escrever o bloco "Resumo do Artigo" (problema, contribuição, natureza teórica sem avaliação empírica).
4. Preencher "Abstract" (um parágrafo: propósito do trabalho + benchmark empírico proposto).
5. Reescrever "Metodologia" com a matriz de parâmetros, workloads e pipeline de coleta.
6. Adicionar subseção "Requisitos para Reprodução".
7. Adicionar seção "Impacto e Conexão com a Sociedade".
8. Popular "Referências" conforme lista acima.
9. Revisar com o grupo e orientador; revalidar o número de citações no Google Scholar próximo da entrega.
