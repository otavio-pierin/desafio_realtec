# desafio_realtec
Desafio técnico para vaga de Dev Agro

--Instruções para uso--

Adicione o caminho do arquivo csv como valor da variável "arquivo", presente no arquivo main.py e execute o mesmo.
O arquivo csv pode ter um cabeçalho, ou não, com os dados (ex: data;conta;tipo;valor;descrição)

--Bibliotecas utilizadas--

csv: Essencial para ler e processar o arquivo de entrada no formato solicitado. Ela lida com a separação das colunas de forma mais eficiente do que um simples comando de texto.

decimal: Utilizada para cálculos monetários, no arquivo de exemplo não é algo diferencial, mas em um cenário real é recomendado, para garantir a exatidão dos valores.

os: Usada para verificar se o arquivo existe antes de tentar abri-lo, evita o fechamento repentino do programa.

--Explicação das Funções e Lógica--

Criei uma classe chamada Processador, que contêm todas as funções necessária para implementação do programa, além disso, em um programa de proporções maiores facilitaria a manutenção.

carregar dados(self): função responsável por criar uma lista com todos os dados, retorna um array dados[] que contêm todos os registros, separados por dados.
ex: [
        ["data1","conta1","tipo","valor","desc1"],
        ["data2","conta2","tipo","valor","desc2"]
    ]
    nessa função também é feita uma verificação para caso o arquivo tenha um cabeçalho, para evitar possíveis erros de tipos de variáveis.

processar(self): percorre cada indice do dicionário contas, o qual guarda o nome da conta e seu saldo (ex: ["CAIXA": "200.00", "BANCO": "150.00"]), efetua a transação somando o valor ao saldo em caso de crédito ('C') e subtraindo em caso de débito ('D'). Se um débito deixar a conta negativa o evento é registrado e impede a efetuação da transação (rollback).
Além disso, é exibido cada uma das transações efetivadas, mostrando a conta responsável, o tipo, e o saldo após a transação.

gerar_relatório(self): utiliza a função sorted() para garantir a exibição em ordem alfabética. Apresenta o saldo fina das contas, totais de registros, e totais de débito e crédito, além de apresentar as transações inconsistentes.
Gera um arquivo .txt que contêm:
-total de registros,
-total creditado,
-total debitado,
-saldo de cada conta,
-inconsistências capturadas
