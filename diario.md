Lab Book

Alunos: Agatha Schneider, Fernando Vieira, Gustavo Flores, João Lucas Martinello de Oliveira e Rodrigo Fehlauer Lauermann
Orientador: Fernando Dotti

Diário de Pesquisa
13/03/2026
Primeiro contato

Foi criado um grupo no WhatsApp para organizar a comunicação. O grupo então enviou um email para o professor Fernando Dotti solicitando uma conversa.

19/03/2026
Solidificação da Comunicação
O Professor foi adicionado ao grupo onde marcamos a primeira reunião para o dia 20/03/2026 às 15h.

20/03/2026
Primeira Reunião
Após entender o contexto do grupo, o professor sugeriu quatro temas para serem explorados ao longo do semestre. São eles:

Resistência de algoritmos de sistemas distribuídos em cenários pós-quânticos 
Tomando um sistema de troca de mensagens qual o impacto de um algoritmo pós-quântico nesse contexto?

Construção de forma modular através de linguagem natural um sistema distribuído
Ex: construir um sistema de mensagem baseado em UDP através de linguagem natural

Avaliar variantes de um algoritmo de multicast
Implementação do algoritmo descrito no paper: Strengthening Atomic Multicast for Partitioned State Machine Replication, suas variantes e realizar uma avaliação baseada em protótipo
Desempenho da blockchain em redes geo-distribuídas
Dado condições de latência e falhas, realizar uma comparação de desempenho entre os algoritmos Hot Staff e Tender Mint

Como não houve consenso entre o grupo a respeito do tema, o professor sugeriu que cada integrante se contextualize com o tema que mais lhe chamou atenção. Ficou acordado que o grupo escolheria um tema até o próximo encontro: 27/03/2026 às 15h 16h.

Fim do contato.

27/03/2026
Segunda Reunião

Glossário: 

Operação atômica no contexto de broadcast (difusão): todos recebem ou nenhum recebe  
Sistema Reativo: processo em repouso até que recebe uma mensagem. A partir da mensagem então há o processamento (reação) e o sistema volta ao repouso aguardando a próxima mensagem. (na literatura chamam isso de guardas)
Exemplo de Multicast: Bancos de dados do tipo Key Value Store

Dado a situação do curso em que o grupo se encontra (entre quinto semestre) e o fato de termos um protótipo pronto para testar, o professor sugeriu irmos para sugestão do algoritmo de multicast. O grupo entrou em consenso e concordou. O professor então explicou de forma didática usando um quadro digital e slides o problema.  

Contexto

Dado um serviço computacional simples que mantém um estado, como um banco.  Usuários acessam o serviço através de um provedor (sendo capazes de login, ver saldo, realizar transferências, etc..). Ao longo do tempo o serviço cresce e a dinâmica provedor-serviço não consegue escalar para atender a demanda.  Então surgem algumas alternativas:

Escalabilidade Vertical
Particionamento do serviço (seria isso escalabilidade horizontal? o processamento é paralelo) 
Usuários de determinados ID's acessam uma partição, os demais nas outras.
 Quando um usuário de uma partição tenta transferir de uma partição para outra ocorre que precisa acontecer uma sincronia entre essas partições para manter a ordem na linha do tempo do estado de cada partição. Caso contrário é possível que aconteça um ciclo. 

Problema: pode acontecer do sistema acusar uma ordem de processos impossível de acontecer, no exemplo do professor: pode acontecer de o saldo de uma conta "crie" dinheiro para fazer sentido quando olhamos as timelines.
Solução: Técnica de difusão atômica, usando replicação

Replicação
 “Nosso problema não é escalabilidade, mas sim tolerância a falhas.”

Ao invés de um único servidor bancário, cria-se réplicas desse servidor. Como manter a consistência entre réplicas? Através de determinismo (a partir de um estado só existe um estado resultante ao processar uma entrada do no sistema). O componente que recebe, ordena e entrega as mensagens é a difusão atômica.  O multicast atômico resolve o problema do ciclo. Como? Mandamos uma mensagem para um subconjunto de partições que detém dados ou validações para manter a ordem.

Existem algoritmos para permitir essa consistência. Um exemplo é o algoritmo de Skeen. (Skeen's Protocol), que usa a noção de timestamp lógico.  Quando um processo envia uma mensagem para um subgrupo de processos (a mensagem fica “bufferizada” como local), então cada processo calcula o timestamp local e propaga pros outros. Quando todos os processos fazem essa atividade então é calculado o timestamp final (dado por max([timestamps locais])). Então a mensagem pode ser processada.

Corner Case: quando houver empate o sistema desempata através de um critério homogêneo não ambíguo para manter a consistência das timestamps. Ex: certas partições tem prioridade. 
 
[ x ] Pergunta: como que o sistema decide para quais partições ele manda a primeira mensagem? Resposta: baseado no input recebido ele repassa para as partições que fazem parte do domínio desse input (ex: chaves competentes para realizar processamento)

Fim da explicação.

Compromisso para o próximo encontro (03/04 10/04/2026): ficou acordado com o professor que leremos o algoritmo de Skeen até o próximo encontro. Encontra-se no paper indicado (Algoritmo 1, Section 4.1) com implementação no Github.
Sugestão para debate futuro: por que o multicast atômico proposto por skeen, sozinho, não é suficiente?  Implementar a alteração sugerida no paper e comparar com a implementação básica.   

Fim do contato.

10/04/2026

