 <h1>Locadora de Filmes - Sistema de Gerenciamento</h1>
    <p>Este é um sistema de locadora de filmes desenvolvido em Python. O objetivo principal é gerenciar diretores, filmes, clientes, funcionários, locações e multas, permitindo uma interação simples para a administração e o controle das operações da locadora.</p>

<h3>Entidades Principais</h3>
    <ul>
        <li><strong>Diretor</strong>: Representa o diretor do filme.
            <ul>
                <li><strong>id</strong>: Identificador único do diretor.</li>
                <li><strong>nome</strong>: Nome do diretor.</li>
                <li><strong>nacionalidade</strong>: Nacionalidade do diretor.</li>
            </ul>
        </li>
        <li><strong>Filme</strong>: Representa o filme disponível na locadora.
            <ul>
                <li><strong>id</strong>: Identificador único do filme.</li>
                <li><strong>titulo</strong>: Título do filme.</li>
                <li><strong>anoLancamento</strong>: Ano de lançamento do filme.</li>
                <li><strong>diretor</strong>: Diretor do filme (relacionado à entidade Diretor).</li>
                <li><strong>qndDisponivel</strong>: Quantidade de filmes disponíveis para locação.</li>
            </ul>
        </li>
        <li><strong>Locação</strong>: Representa uma locação realizada por um cliente.
            <ul>
                <li><strong>id</strong>: Identificador único da locação.</li>
                <li><strong>nomeFilme</strong>: Nome do filme alugado.</li>
                <li><strong>data</strong>: Data de início da locação.</li>
                <li><strong>data_devolucao</strong>: Data prevista para devolução.</li>
                <li><strong>cliente</strong>: Cliente que fez a locação (relacionado à entidade Cliente).</li>
                <li><strong>funcionario</strong>: Funcionário responsável pela locação (relacionado à entidade Funcionário).</li>
                <li><strong>status</strong>: Status da locação (ativa, devolvida, renovada).</li>
            </ul>
        </li>
        <li><strong>Cliente</strong>: Representa os clientes que alugam filmes na locadora.
            <ul>
                <li><strong>cpf</strong>: CPF do cliente.</li>
                <li><strong>nome</strong>: Nome completo do cliente.</li>
                <li><strong>dataNasc</strong>: Data de nascimento do cliente.</li>
                <li><strong>sexo</strong>: Sexo do cliente.</li>
            </ul>
        </li>
        <li><strong>Funcionário</strong>: Representa os funcionários da locadora.
            <ul>
                <li><strong>id</strong>: Identificador único do funcionário.</li>
                <li><strong>nome</strong>: Nome completo do funcionário.</li>
                <li><strong>dataNasc</strong>: Data de nascimento do funcionário.</li>
                <li><strong>sexo</strong>: Sexo do funcionário.</li>
            </ul>
        </li>
        <li><strong>Multa</strong>: Representa a multa gerada quando o cliente atrasa a devolução de um filme.
            <ul>
                <li><strong>id</strong>: Identificador único da multa.</li>
                <li><strong>valor</strong>: Valor da multa.</li>
                <li><strong>data</strong>: Data em que a multa foi gerada.</li>
                <li><strong>cliente</strong>: Cliente responsável pela multa (relacionado à entidade Cliente).</li>
                <li><strong>paga</strong>: Status da multa (paga ou não paga).</li>
            </ul>
        </li>
    </ul>

<h3>Funcionalidades Principais</h3>
    <h4>1. Diretores</h4>
    <ul>
        <li><strong>Adicionar Diretor</strong> (Acessado apenas por funcionário): Adiciona um novo diretor ao sistema, com informações como nome e nacionalidade.</li>
        <li><strong>Consultar Diretores</strong>: Exibe uma lista de todos os diretores cadastrados no sistema.</li>
        <li><strong>Excluir Diretor</strong>: Permite ao funcionário excluir um diretor pelo <em>id</em> do diretor.</li>
    </ul>

<h4>2. Filmes</h4>
    <ul>
        <li><strong>Adicionar Filme</strong> (Acessado apenas por funcionário): Adiciona um novo filme ao sistema com título, ano de lançamento, diretor e quantidade disponível.</li>
        <li><strong>Consultar Filmes</strong>: Exibe uma lista de todos os filmes disponíveis para locação.</li>
        <li><strong>Excluir Filme</strong>: Permite ao funcionário excluir um filme pelo título.</li>
    </ul>

<h4>3. Clientes</h4>
    <ul>
        <li><strong>Cadastrar Cliente</strong>: Permite o cliente se cadastrar no sistema (informações como nome, CPF, data de nascimento e sexo).</li>
        <li><strong>Atualizar Cliente</strong>: O cliente pode atualizar suas informações pessoais (como nome, data de nascimento, sexo).</li>
        <li><strong>Excluir Cliente</strong>: Permite ao funcionário excluir um cliente pelo CPF.</li>
    </ul>

<h4>4. Locações</h4>
    <ul>
        <li><strong>Fazer Locação</strong>: Permite ao cliente realizar uma locação, desde que esteja cadastrado no sistema.</li>
        <li><strong>Consultar Locações</strong>: Permite ao funcionário consultar todas as locações realizadas.</li>
        <li><strong>Histórico de Locações</strong> (Disponível para o cliente): O cliente pode visualizar seu histórico de locações anteriores e as locações ativas.</li>
        <li><strong>Fazer Devolução</strong>: O cliente pode realizar a devolução de um filme alugado.</li>
        <li><strong>Renovar Locação</strong>: O cliente pode renovar a locação de um filme (prolongar o prazo de devolução).</li>
    </ul>

<h4>5. Multas</h4>
    <ul>
        <li><strong>Pagar Multa</strong>: Caso o cliente atrase a devolução, uma multa será gerada. O cliente pode pagar a multa através do sistema.</li>
    </ul>

<h4>6. Funcionários</h4>
    <ul>
        <li><strong>Cadastrar Funcionário</strong>: Permite o cadastro de novos funcionários (informações como nome, data de nascimento, CPF e sexo).</li>
    </ul>
