from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date, Boolean
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import date, timedelta, datetime
import time
from sqlalchemy import delete

#criação e conexão do banco de dados com POO
engine = create_engine('sqlite:///locadora.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

#erros personalizados
class cpfExistente(Exception):
    pass

class LimiteLocacao(Exception):
    pass

class MenorDeIdade(Exception):
    pass


class Diretor(Base):
    __tablename__ = 'diretores'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    nacionalidade = Column(String)

    def __repr__(self):
        filmes_nome = ", ".join([filme.titulo for filme in self.filmes])
        return f'Diretor: {self.nome} | Filmes: {filmes_nome}'

class Filme(Base):
    __tablename__ = 'filmes'
     
    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    anoLancamento = Column(Integer)
    diretor_id = Column(Integer, ForeignKey('diretores.id'))
    diretor = relationship('Diretor', backref='filmes')
    qtdDisponivel = Column(Integer)
    funcionario_id = Column(Integer, ForeignKey('funcionarios.id'))
    funcionario = relationship('Funcionario', backref='filmes')
    

    def __repr__(self):
        return f'Filme: {self.titulo} | diretor:{self.diretor.nome}'

    
class Locacao(Base):
    __tablename__ = 'locação'
    
    id = Column(Integer, primary_key=True)
    nomeFilme = Column(String)
    data = Column(Date)
    data_devolucao = Column(Date)
    cliente_cpf = Column(Integer, ForeignKey('clientes.cpf'))
    cliente = relationship('Cliente', backref='locação')
    funcionario_id = Column(Integer, ForeignKey('funcionarios.id'))
    funcionario = relationship ('Funcionario', backref='locação')
    status = Column(String, default='Ativa')
    
    
class Cliente(Base):
    __tablename__ = 'clientes'
    
    cpf = Column(Integer, primary_key=True)
    nome = Column(String)
    dataNasc = Column(Date)
    sexo = Column(String)
    
class Funcionario(Base):
    __tablename__ = 'funcionarios'
    
    id = Column(Integer, primary_key=True)
    cpf = Column(Integer)
    nome = Column(String)
    dataNasc = Column(Date)
    sexo = Column(String)

class Multa(Base):
    __tablename__ = 'multas'

    id = Column(Integer, primary_key=True)
    valor = Column(Float)
    data = Column(Date)
    cliente_cpf = Column(Integer, ForeignKey('clientes.cpf'))
    cliente = relationship('Cliente', backref='multas')
    paga = Column(Boolean, default=False)
    
# Criação das tabelas no banco de dados
#Base.metadata.create_all(engine)

def adicionar_diretor(nome, nacionalidade):
    diretor = session.query(Diretor).filter_by(nome=nome).first()
    if not diretor:
        diretor = Diretor(nome=nome, nacionalidade = nacionalidade)
        session.add(diretor)
        session.commit()
        print(f"Diretor {nome} Adicionado!")

def excluir_diretor(id_diretor):
    diretor = delete(Diretor).where(Diretor.id == id_diretor)

    session.execute(diretor)
    session.commit()
    print(f"Diretor Excluido")


def adicionar_filme(titulo, anoLancamento, diretor, qtdDisponivel, funcionario_id):
    diretor = session.query(Diretor).filter_by(nome=diretor).first()
    funcionario = session.query(Funcionario).filter_by(id=funcionario_id).first()
    
    if not diretor:
        print(f"diretor: {diretor}, não foi encontrado")
        return
    
    if not funcionario:
        print(f"Funcionario não encontrado")
        return
    
    filme = Filme(titulo=titulo, anoLancamento=anoLancamento,diretor=diretor, qtdDisponivel=qtdDisponivel, funcionario_id=funcionario_id)
    session.add(filme)
    session.commit()
    print(f'filme: {titulo} adicionado a locadora!')
    
def excluir_filme(titulo):
    filme = delete(Filme).where(Filme.titulo == titulo)
    
    session.execute(filme, {'Filme': titulo})
    session.commit()

    print(f"Filme: {titulo} excluído com sucesso.")

def cadastrar_funcionario(nome, dataNasc, cpf, sexo):
    funcionario = session.query(Funcionario).filter_by(cpf=cpf).first()
    if funcionario:
        print(f"Funcionário com CPF {cpf} já cadastrado.")
        return
    
    dataNasc = datetime.strptime(dataNasc, "%d/%m/%Y").date() 
    
    funcionario = Funcionario(nome=nome, dataNasc=dataNasc, cpf=cpf, sexo=sexo)
    session.add(funcionario)
    session.commit()
    print(f"Funcionário {nome} cadastrado com sucesso!")


def cadastrar_cliente(nome, cpf, dataNasc, sexo):
    try:
        # Verifica se o cliente já existe no banco de dados
        cliente = session.query(Cliente).filter_by(cpf=cpf).first()
        if cliente:
            raise cpfExistente("Esse CPF já está cadastrado.")
        
        # Converter a string de data no formato DD/MM/AAAA para um objeto datetime
        dataNasc = datetime.strptime(dataNasc, "%d/%m/%Y").date()
        # Verificar se o cliente é maior de idade
        data_atual = datetime.now()
        idade = data_atual.year - dataNasc.year - ((data_atual.month, data_atual.day) < (dataNasc.month, dataNasc.day))
        
        if idade < 18:
            raise MenorDeIdade("O cliente deve ser maior de idade para se cadastrar.")
        
        cliente = Cliente(nome=nome, cpf=cpf, dataNasc=dataNasc, sexo=sexo)
        session.add(cliente)
        session.commit()
        print("Cliente cadastrado com sucesso!")
    
    except cpfExistente as e:
        print(e)
    except MenorDeIdade as e:
        print(e)
        
def atualizar_cliente(cpf):
    cliente = session.query(Cliente).filter_by(cpf=cpf).first()
    
    if not cliente:
        print(f"Cliente com CPF {cpf} não encontrado.")
        return
    
    while True:
        print("O que você deseja atualizar?")
        print("1 - Nome")
        print("2 - Data de Nascimento")
        print("3 - Sexo")
        print("4 - Cancelar")

        opcao = input()

        if opcao == '1':
            novo_nome = input("Digite o novo nome: ")
            cliente.nome = novo_nome
            print(f"Nome atualizado!")

        elif opcao == '2':
            nova_dataNasc = input("Digite a nova data de nascimento (DD/MM/AAAA): ")
            try:
                nova_dataNasc = datetime.strptime(nova_dataNasc, "%d/%m/%Y").date()
                cliente.dataNasc = nova_dataNasc
                print(f"Data de nascimento atualizada para: {nova_dataNasc}")
            except ValueError:
                print("Formato de data inválido. Tente novamente.")

        elif opcao == '3':
            novo_sexo = input("Digite o novo sexo (M/F): ").upper()
            if novo_sexo in ['M', 'F']:
                cliente.sexo = novo_sexo
                print(f"Dado atualizado!")
            else:
                print("Sexo inválido. Deve ser 'M' ou 'F'.")
        
        elif opcao == '4':
            print("Atualização cancelada.")
            return

        else:
            print("Opção inválida!")
        
        session.commit()
        continuar = input("Deseja atualizar mais algum dado? (S/N): ").upper()
        if continuar != 'S':
            print("Encerrando a atualização.")
            break

def excluir_cliente(cpf):
    try:
        cliente = delete(Cliente).where(Cliente.cpf == cpf)

        session.execute(cliente, {'cpf': cpf})
        session.commit()

        print(f"Cliente com CPF {cpf} excluído com sucesso.")

    except Exception as e:
        print(f"Erro ao excluir cliente com CPF {cpf}: {str(e)}")


def fazer_locacao(nomeFilme, cpf, funcionario_id):
    session = Session()
    try:
        filme = session.query(Filme).filter_by(titulo=nomeFilme).first()
        if not filme or filme.qtdDisponivel <= 0:
            print("O filme está indisponível para locação no momento.")
            return
        
        cliente = session.query(Cliente).filter_by(cpf=cpf).first()
        if not cliente:
            print("Cliente não encontrado.")
            return
        
        funcionario = session.query(Funcionario).filter_by(id=funcionario_id).first()
        if not funcionario:
            print("Funcionário não encontrado. Não é possível registrar a locação.")
            return
    
        # busca locações que ainda estão ativas, que não foram devolvidas ainda ou cuja devolução está prevista para o futuro.
        locacoes_ativas = session.query(Locacao).filter_by(cliente_cpf=cpf).filter(Locacao.data_devolucao >= date.today()).count()
        limite_locacoes = 3  

        if locacoes_ativas >= limite_locacoes:
            raise LimiteLocacao(f"O cliente atingiu o limite de locações de {limite_locacoes} filmes.")

        multa_pendente = session.query(Multa).filter_by(cliente_cpf=cpf).filter(Multa.paga == False).first()
        if multa_pendente:
            print(f'É necessário fazer o pagamento da multa para alugar o filme. Multa pendente: R${multa_pendente.valor}')
            return
        
        
        locacao = Locacao(nomeFilme=nomeFilme, cliente_cpf=cpf, funcionario_id=funcionario_id)
        locacao.data = date.today()
        locacao.data_devolucao = locacao.data + timedelta(weeks=1)
        locacao.status = 'Ativa'
        filme.qtdDisponivel -= 1
        session.add(locacao)
        session.commit()
        print(f'Locação realizada em: {locacao.data} | ID: {locacao.id}')
        print(f'Devolver até {locacao.data_devolucao}')
    
    except LimiteLocacao as e:
        print(e)  


def consultar_filmes():
    filmes = session.query(Filme).all()
    for filme in filmes:
        print(filme)
        print('-'*20)

def consultar_diretores():
    diretores = session.query(Diretor).all()
    for diretor in diretores:
        print(diretor)
        print('-'*20)

def consulta_locacoes():
    #faz acesso a tabela que queremos utilizar
    locacoes = session.query(Locacao).all()
    if not locacoes:
        print("Não há locações registradas.")
        return

    for locacao in locacoes:
        cliente_nome = locacao.cliente.nome
        print(f'Locação ID: {locacao.id}')
        print(f'Nome do Filme: {locacao.nomeFilme}')
        print(f'Data: {locacao.data}')
        print(f'Cliente: {cliente_nome}')
        print('-'*20)
        
def historico_locacoes(cpf):
    locacoes = session.query(Locacao).join(Cliente).filter(Cliente.cpf == cpf).all()

    if not locacoes:
        print(f"Não há locações registradas para o cliente {cliente_nome}.")
        return

    cliente_nome = locacoes[0].cliente.nome  # A primeira locação contém o cliente

    print(f"Histórico de Locações do Cliente {cliente_nome}:")
    for locacao in locacoes:
        # Imprime os detalhes de cada locação
        print(f'Locação ID: {locacao.id}')
        print(f'Nome do Filme: {locacao.nomeFilme}')
        print(f'Data da Locação: {locacao.data}')
        print('-'*30)

def fazer_devolucao(id, nomeFilme, cpf):
    filme = session.query(Filme).filter_by(titulo=nomeFilme).first()
    locacao = session.query(Locacao).filter_by(id=id, cliente_cpf=cpf).first()
    if not filme:
        print("Filme não encontrado.")
        return
        
    # consulta a locação pelo id e cpf
    if not locacao:
        print("Locação não encontrada.")
        return
        
    #consultar a data da devolução para conferir a multa
    data_hoje = date.today() #+ timedelta(days=15) teste multa
    if data_hoje <= locacao.data_devolucao:
        locacao.status = 'Devolvida'
        filme.qtdDisponivel += 1
        session.commit()
        print(f'Devolução concluida! Obrigada pela preferencia!')
    else:
        dias_atraso = (data_hoje - locacao.data_devolucao).days
        multa = Multa(valor=dias_atraso * 5, data=data_hoje, cliente_cpf=cpf)
        session.add(multa)  
        filme.qtdDisponivel += 1
        session.commit()  
        print(f'Devolução atrasada! Você deve R$ {multa.valor:.2f} de multa.')
        print('Devolução concluída com atraso. Obrigado pela preferência!')
        
def renovar_filme(id, nomeFilme, cpf):
    filme = session.query(Filme).filter_by(titulo=nomeFilme).first()
    locacao = session.query(Locacao).filter_by(id=id, cliente_cpf=cpf).first()
    if not filme:
        print("Filme não encontrado.")
        return
        
        # consultar a locação pelo id e cpf 
    if not locacao:
        print("Locação não encontrada.")
        return
        
        # verificação de datas
    if locacao.data_devolucao < date.today():
        print(f"Não é possível renovar, a devolução do filme {nomeFilme} está em atraso!")
        return
        
    nova_data_devolucao = locacao.data_devolucao + timedelta(days=7)
    locacao.data_devolucao = nova_data_devolucao
    session.commit()
        
    print(f"A renovação foi realizada com sucesso! Nova data de devolução: {nova_data_devolucao}")

def pagar_multa():
    try:
        # exibe multas pendentes
        multas_pendentes = session.query(Multa).filter(Multa.paga == False).all()
        if not multas_pendentes:
            print("Não há multas pendentes.")
            return
        
        print("Multas pendentes:")
        for multa in multas_pendentes:
            print(f"ID: {multa.id}, Valor: R$ {multa.valor}, Data: {multa.data}")

        # pega o id da multa pra pagar
        id_multa = int(input("Digite o ID da multa que deseja pagar: "))

        # encontra  a multa pelo id
        multa = session.query(Multa).filter(Multa.id == id_multa, Multa.paga == False).first()
        if multa:
            multa.paga = True  
            session.commit()  # salva na tabela
            print(f"Multa de R$ {multa.valor} paga com sucesso!")
        else:
            print("Multa não encontrada ou já foi paga.")
            
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        session.rollback()  # Reverte a transação em caso de erro
    finally:
        session.close()

def inicializar():
    if not session.query(Funcionario).first():
        cadastrar_funcionario('sara', '01/01/2000', 15486235099, 'm')
            
    if not session.query(Diretor).first():
        adicionar_diretor('greta gerwig','norte americana')
        adicionar_diretor('byron howard', 'estadunidense')
        adicionar_diretor('tim burton', 'norte americano')
        adicionar_diretor('christopher nolan', 'britânico')
        adicionar_diretor('james cameron', 'canadense')


    if not session.query(Filme).first():
        adicionar_filme('barbie',2023,'greta gerwig',7,1)
        adicionar_filme('adoraveis mulheres',2019,  'greta gerwig', 5,1)
        adicionar_filme('zootopia', 2016,'byron howard', 5,1 )
        adicionar_filme('bolt', 2008, 'byron howard', 2,1)
        adicionar_filme('beetlejuice', 1988, 'tim burton', 4,1)
        adicionar_filme('a noiva cadaver',2005, 'tim burton', 7,1 )
        adicionar_filme('oppenheimer',2023, 'christopher nolan', 2,1 )
        adicionar_filme('interestelar', 2014, 'christopher nolan', 4,1)
        adicionar_filme('avatar', 2009, 'james cameron', 3,1 )
        adicionar_filme('titanic',1997, 'james cameron', 1,1 )

    if not session.query(Cliente).first():
        cadastrar_cliente('giovana' ,76894514523, '02/05/2002', 'f')
        cadastrar_cliente('bruna' ,45678912354,'10/06/2002', 'f')
        cadastrar_cliente('lavinia' ,32415678964,'24/10/2003', 'f')
        cadastrar_cliente('pedro' ,12365495135, '14/05/2005', 'm')
        cadastrar_cliente('joão' ,75395145663, '25/01/2004', 'm')
        

    print("Dados iniciais inseridos com sucesso!")

def main():
    while True:
        print("Bem-vindo a Locadora!")
        print("1 - Entrar como Funcionário")
        print("2 - Login Cliente")
        print("3 - Criar Conta Cliente")
        print("4 - Consultar Diretores")
        print("5 - Consultar Filmes")
        print("6 - Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            cpf_funcionario = input("Digite seu CPF de funcionário: ")
            funcionario = session.query(Funcionario).filter_by(cpf=cpf_funcionario).first()
            if funcionario:
                menu_funcionario(funcionario)
            else:
                print("Funcionário não encontrado. Tente novamente.")
        
        elif opcao == '2':
            cpf_cliente = input("Digite seu CPF de cliente: ")
            cliente = session.query(Cliente).filter_by(cpf=cpf_cliente).first()
            if cliente:
                menu_cliente(cliente)
            else:
                print("Cliente não encontrado. Tente novamente.")
            
        elif opcao == '3':
            nome = input("Digite seu nome: ")
            cpf_cliente = input("Digite seu CPF: ")
            dataNasc = input("Digite sua data de nascimento (DD/MM/AAAA): ")
            sexo = input("Digite seu sexo (M/F): ")
            cadastrar_cliente(nome, cpf_cliente, dataNasc, sexo)
            
            print('...Entrando na conta')
            time.sleep(3)
            cliente = session.query(Cliente).filter_by(cpf=cpf_cliente).first()
            if cliente:
                menu_cliente(cliente)
            else:
                print("Erro ao criar a conta. Tente novamente.")
        
        elif opcao == '4':
            consultar_diretores()
            
        elif opcao == '5':
            print("Saindo do sistema...")
            break
        
        else:
            print("Opção inválida! Tente novamente.")

# Menu de opções para Funcionário
def menu_funcionario(funcionario):
    while True:
        print(f"Bem-vindo, {funcionario.nome}!")
        print("1 - Adicionar Diretor")
        print("2 - Adicionar Filme")
        print("3 - Excluir Diretor")
        print("4 - Excluir Filme")
        print("5 - Excluir Cliente")
        print("6 - Consultar Locações")
        print("7 - Cadastrar Novo Funcionário")
        print("8 - Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("Nome do diretor: ")
            nacionalidade = input("Nacionalidade do diretor: ")
            adicionar_diretor(nome, nacionalidade)
        
        elif opcao == '2':
            titulo = input("Título do filme: ")
            anoLancamento = int(input("Ano de lançamento: "))
            diretor_nome = input("Nome do diretor: ")
            qtdDisponivel = int(input("Quantidade disponível: "))
            funcionario_id = funcionario.id
            adicionar_filme(titulo, anoLancamento, diretor_nome, qtdDisponivel, funcionario_id)
        
        elif opcao == '3':
            id_diretor = input("ID do diretor a ser excluído: ")
            excluir_diretor(id_diretor)
        
        elif opcao == '4':
            titulo = input("Título do filme a ser excluído: ")
            excluir_filme(titulo)
        
        elif opcao == '5':
            cpf_cliente = int(input("Digite o CPF do cliente a ser excluído: "))
            excluir_cliente(cpf_cliente)
            
        elif opcao == '6':
            consulta_locacoes()
            
        elif opcao == '7':
            nome = input("Nome do novo funcionário: ")
            dataNasc = input("Data de nascimento do novo funcionário (DD/MM/AAAA): ")
            cpf = int(input("CPF do novo funcionário: "))
            sexo = input("Sexo do novo funcionário (M/F): ")
            cadastrar_funcionario(nome, dataNasc, cpf, sexo)
        
        elif opcao == '8':
            print("Saindo do menu de funcionário...")
            break
        
        else:
            print("Opção inválida! Tente novamente.")

# Menu de opções para Cliente
def menu_cliente(cliente):
    while True:
        print(f"Bem-vindo, {cliente.nome}!")
        print("1 - Fazer Locação")
        print("2 - Realizar Devolução")
        print("3 - Renovar Filme")
        print("4 - Pagar Multa")
        print("5 - Histórico Locações")
        print("6 - Atualizar Dados")
        print("7 - Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nomeFilme = input("Digite o nome do filme que deseja alugar: ")
            cpf_cliente = cliente.cpf
            funcionario_id = int(input("Digite o ID do funcionário que registrou a locação: "))
            fazer_locacao(nomeFilme, cpf_cliente, funcionario_id)
        
        elif opcao == '2':
            id_locacao = int(input("Digite o ID da locação: "))
            nomeFilme = input("Digite o nome do filme a ser devolvido: ")
            cpf_cliente = cliente.nome
            fazer_devolucao(id_locacao, nomeFilme, cpf_cliente)
            
        elif opcao == '3':
            id_locacao = int(input("Digite o ID da locação: "))
            nomeFilme = input("Digite o nome do filme a ser renovado: ")
            cpf_cliente = cliente.cpf
            renovar_filme(id_locacao, nomeFilme, cpf_cliente)
        
        elif opcao == '4':
            pagar_multa()
            
        elif opcao == '5':
            historico_locacoes(cliente.cpf)
        
        elif opcao == '6':
            atualizar_cliente(cliente.cpf)
            
        elif opcao == '7':
            print("Saindo do menu de cliente...")
            break
        else:
            print("Opção inválida! Tente novamente.")
            
            
if __name__ == "__main__":
    # Criar as tabelas, caso ainda não existam
    Base.metadata.create_all(engine)

    # Inserir dados iniciais no banco de dados
    inicializar()

    # Chama o menu principal
    main()
