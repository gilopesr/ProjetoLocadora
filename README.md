# Locadora de Filmes - Sistema de Gerenciamento
Este é um sistema de locadora de filmes desenvolvido em Python. O objetivo principal é gerenciar diretores, filmes, clientes, funcionários, locações e multas, permitindo uma interação simples para a administração e o controle das operações da locadora.

## Entidades Principais
Diretor: Representa o diretor do filme.

id: Identificador único do diretor.
nome: Nome do diretor.
nacionalidade: Nacionalidade do diretor.
Filme: Representa o filme disponível na locadora.

id: Identificador único do filme.
titulo: Título do filme.
anoLancamento: Ano de lançamento do filme.
diretor: Diretor do filme (relacionado à entidade Diretor).
qndDisponivel: Quantidade de filmes disponíveis para locação.
Locação: Representa uma locação realizada por um cliente.

id: Identificador único da locação.
nomeFilme: Nome do filme alugado.
data: Data de início da locação.
data_devolucao: Data prevista para devolução.
cliente: Cliente que fez a locação (relacionado à entidade Cliente).
funcionario: Funcionário responsável pela locação (relacionado à entidade Funcionário).
status: Status da locação (ativa, devolvida, renovada).
Cliente: Representa os clientes que alugam filmes na locadora.

cpf: CPF do cliente.
nome: Nome completo do cliente.
dataNasc: Data de nascimento do cliente.
sexo: Sexo do cliente.
Funcionário: Representa os funcionários da locadora.

id: Identificador único do funcionário.
nome: Nome completo do funcionário.
dataNasc: Data de nascimento do funcionário.
sexo: Sexo do funcionário.
Multa: Representa a multa gerada quando o cliente atrasa a devolução de um filme.

id: Identificador único da multa.
valor: Valor da multa.
data: Data em que a multa foi gerada.
cliente: Cliente responsável pela multa (relacionado à entidade Cliente).
paga: Status da multa (paga ou não paga).

## Funcionalidades Principais
1. Diretores
Adicionar Diretor (Acessado apenas por funcionário)

Adiciona um novo diretor ao sistema, com informações como nome e nacionalidade.
Consultar Diretores

Exibe uma lista de todos os diretores cadastrados no sistema.
Excluir Diretor

Permite ao funcionário excluir um diretor pelo id do diretor.
2. Filmes
Adicionar Filme (Acessado apenas por funcionário)

Adiciona um novo filme ao sistema com título, ano de lançamento, diretor e quantidade disponível.
Consultar Filmes

Exibe uma lista de todos os filmes disponíveis para locação.
Excluir Filme

Permite ao funcionário excluir um filme pelo título.
3. Clientes
Cadastrar Cliente

Permite o cliente se cadastrar no sistema (informações como nome, CPF, data de nascimento e sexo).
Atualizar Cliente

O cliente pode atualizar suas informações pessoais (como nome, data de nascimento, sexo).
Excluir Cliente

Permite ao funcionário excluir um cliente pelo CPF.
4. Locações
Fazer Locação

Permite ao cliente realizar uma locação, desde que esteja cadastrado no sistema.
Consultar Locações

Permite ao funcionário consultar todas as locações realizadas.
Histórico de Locações (Disponível para o cliente)

O cliente pode visualizar seu histórico de locações anteriores e as locações ativas.
Fazer Devolução

O cliente pode realizar a devolução de um filme alugado.
Renovar Locação

O cliente pode renovar a locação de um filme (prolongar o prazo de devolução).
5. Multas
Pagar Multa
Caso o cliente atrase a devolução, uma multa será gerada. O cliente pode pagar a multa através do sistema.
6. Funcionários
Cadastrar Funcionário
Permite o cadastro de novos funcionários (informações como nome, data de nascimento, CPF e sexo).
