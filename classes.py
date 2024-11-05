from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date, Boolean
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import date, timedelta, datetime
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
Base.metadata.create_all(engine)

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
            raise ValueError("O cliente deve ser maior de idade para se cadastrar.")
        
        cliente = Cliente(nome=nome, cpf=cpf, dataNasc=dataNasc, sexo=sexo)
        session.add(cliente)
        session.commit()
        print("Cliente cadastrado com sucesso!")
    
    except cpfExistente as e:
        print(e)
    except ValueError as e:
        print(e)

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
        filme.qtdDisponivel -= 1
        session.add(locacao)
        session.commit()
        print(f'Locação realizada em: {locacao.data} | ID: {locacao.id}\n Devolver até {locacao.data_devolucao}')
    
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
        print(f'Locação ID: {locacao.id}\n Nome do Filme: {locacao.nomeFilme}\n Data: {locacao.data}\n Cliente: {cliente_nome}')
        print('-'*20)

def fazer_devolucao(id, nomeFilme, cpf):
    filme = session.query(Filme).filter_by(titulo=nomeFilme).first()
    if not filme:
        print("Filme não encontrado.")
        return
    
    # Consulta a locação pelo id e cpf
    locacao = session.query(Locacao).filter_by(id=id, cliente_cpf=cpf).first()
    if not locacao:
        print("Locação não encontrada.")
        return
    
    #consultar a data da devolução para conferir a multa
    data_hoje = date.today() #+ timedelta(days=15) teste multa
    if data_hoje <= locacao.data_devolucao:
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
        print('Devolução concluída com atraso! Obrigado pela preferência!')

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


def main():
    while True:
        print("Bem-vindo ao sistema de locadora!")
        print("1 - Entrar como Funcionário")
        print("2 - Entrar como Cliente")
        print("3 - Sair")
        print('4 - primeiro acesso')
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            cpf_funcionario = input("Digite seu CPF de funcionário: ")
            funcionario = session.query(Funcionario).filter_by(cpf=cpf_funcionario).first()
            if funcionario:
                menu_funcionario(funcionario)
            else:
                print("Funcionário não encontrado. Tente novamente.")
        
        elif opcao == '2':
            menu_cliente()
                    
        elif opcao == '4':
            nome = str(input("Nome do novo funcionário: "))
            dataNasc = str(input("Data de nascimento do novo funcionário (DD/MM/AAAA): "))
            cpf = int(input("CPF do novo funcionário: "))
            sexo = str(input("Sexo do novo funcionário (M/F): "))
            cadastrar_funcionario(nome, dataNasc, cpf, sexo)
            
        elif opcao == '3':
            print("Saindo do sistema...")
            break
        
        else:
            print("Opção inválida! Tente novamente.")

# Menu de opções para Funcionário
def menu_funcionario(funcionario):
    while True:
        print(f"\nBem-vindo, {funcionario.nome}!")
        print("1 - Adicionar Diretor")
        print("2 - Adicionar Filme")
        print("3 - Excluir Diretor")
        print("4 - Excluir Filme")
        print("5 - Excluir Cliente")
        print("6 - Cadastrar Novo Funcionário")
        print("7 - Sair")
        
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
            nome = input("Nome do novo funcionário: ")
            dataNasc = input("Data de nascimento do novo funcionário (DD/MM/AAAA): ")
            cpf = int(input("CPF do novo funcionário: "))
            sexo = input("Sexo do novo funcionário (M/F): ")
            cadastrar_funcionario(nome, dataNasc, cpf, sexo)
        
        elif opcao == '7':
            print("Saindo do menu de funcionário...")
            break
        
        else:
            print("Opção inválida! Tente novamente.")

# Menu de opções para Cliente
def menu_cliente():
    while True:
        print(f"\nBem-vindo, Oque deseja fazer hoje?")
        print("1 - Fazer Cadastro")
        print("2 - Fazer Locação")
        print("3 - Fazer Devolução")
        print("4 - Pagar Multa")
        print("5 - Consultar Filmes")
        print("6 - Consultar Diretores")
        print("7 - Consultar Locações")
        print("8 - Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("Digite seu nome: ")
            cpf_cliente = input("Digite seu CPF: ")
            dataNasc = input("Digite sua data de nascimento (DD/MM/AAAA): ")
            sexo = input("Digite seu sexo (M/F): ")
            cadastrar_cliente(nome, cpf_cliente, dataNasc, sexo)
        
        elif opcao == '2':
            nomeFilme = input("Digite o nome do filme que deseja alugar: ")
            cpf_cliente = input("Digite seu CPF: ")
            funcionario_id = int(input("Digite o ID do funcionário que registrou a locação: "))
            fazer_locacao(nomeFilme, cpf_cliente, funcionario_id)
            
        elif opcao == '3':
            id_locacao = int(input("Digite o ID da locação: "))
            nomeFilme = input("Digite o nome do filme a ser devolvido: ")
            cpf_cliente = input("Digite seu CPF: ")
            fazer_devolucao(id_locacao, nomeFilme, cpf_cliente)
        
        elif opcao == '4':
            pagar_multa()
        
        elif opcao == '5':
            consultar_filmes()
        
        elif opcao == '6':
            consultar_diretores()
        
        elif opcao == '7':
            consulta_locacoes()
            
        elif opcao == '8':
            print("Saindo do menu de cliente...")
            break
        
        else:
            print("Opção inválida! Tente novamente.")
            
            
if __name__ == "__main__":
    main()
