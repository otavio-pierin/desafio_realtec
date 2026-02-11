# desafio_realtec
Desafio técnico para vaga de Dev Agro

--Bibliotecas utilizadas--

csv: Essencial para ler e processar o arquivo de entrada no formato solicitado. Ela lida com a separação das colunas de forma mais eficiente do que um simples comando de texto.

decimal: Utilizada para cálculos monetários, no arquivo de exemplo não é algo diferencial, mas em um cenário real é recomendado, para garantir a exatidão dos valores.

os: Usada para verificar se o arquivo existe antes de tentar abri-lo, evita o fechamento repentino do programa.

--Explicação das Funções e Lógica--

Criei uma classe chamada Processador, que contêm todas as funções necessária para implementação do programa, além disso, em um programa de proporções maiores facilitaria a manutenção.

carregar dados(self): função que limpa espaços em branco, remove acentos dos cabeçalhos, além de transformar o nome das contas em maiúscula, criando um padrão.

processar(self): percorre cada linha, somando em caso de crédito ('C') e subtraindo em caso de débito ('D'). Se um débito deixar a conta negativa o evento é registrado e impede a efetuação da transação (rollback).

gerar_relatório(self): utiliza a função sorted() para garantir a exibição em ordem alfabética. Apresenta o saldo fina das contas, totais de registros, e totais de débito e crédito, além de apresentar as transações inconsistentes.
