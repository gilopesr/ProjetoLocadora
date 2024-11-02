from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date, Boolean
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import date, timedelta
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
        return f'Diretor: {self.nome}\n filmes = {self.filmes})'

class Filme(Base):
    __tablename__ = 'filmes'
     
    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    anoLancamento = Column(Integer)
    diretor_id = Column(Integer, ForeignKey('diretores.id'))
    diretor = relationship('Diretor', backref='filmes')
    qtdDisponivel = Column(Integer)
    

    def __repr__(self):
        return f'Filme: (titulo={self.titulo}, diretor={self.diretor.nome})'

    
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
    dataNasc = Column(String)
    sexo = Column(String)
    
class Funcionario(Base):
    __tablename__ = 'funcionarios'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    dataNasc = Column(String)
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

def excluir_diretor(id_diretor):
    diretor = delete(Diretor).where(Diretor.id == id_diretor)

    session.execute(diretor)
    session.commit()


def adicionar_filme(titulo, anoLancamento, diretor, qtdDisponivel):
    diretor = session.query(Diretor).filter_by(nome=diretor).first()
    if not diretor:
        print(f"diretor: {diretor}, não foi encontrado")
        return
    
    filme = Filme(titulo=titulo, anoLancamento=anoLancamento, diretor=diretor, qtdDisponivel=qtdDisponivel)
    session.add(filme)
    session.commit()
    
def excluir_filme(titulo):
    filme = delete(Filme).where(Filme.titulo == titulo)
    
    session.execute(filme, {'Filme': titulo})
    session.commit()

    print(f"Filme: {titulo}, excluído com sucesso.")

def cadastrar_cliente(nome, cpf, dataNasc, sexo):
    try:
        cliente = session.query(Cliente).filter_by(cpf=cpf).first()
        if cliente:
            raise cpfExistente("Esse CPF já está cadastrado.")

        cliente = Cliente(nome=nome, cpf=cpf, dataNasc=dataNasc, sexo=sexo)
        session.add(cliente)
        session.commit()
        print("Cliente cadastrado com sucesso!")
    except cpfExistente as e:
        print(e)

def excluir_cliente(cpf):
    try:
        cliente = delete(Cliente).where(Cliente.cpf == cpf)

        session.execute(cliente, {'cpf': cpf})
        session.commit()

        print(f"Cliente com CPF {cpf} excluído com sucesso.")

    except Exception as e:
        print(f"Erro ao excluir cliente com CPF {cpf}: {str(e)}")


def fazer_locacao(nomeFilme, cpf):
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

        # busca locações que ainda estão ativas, que não foram devolvidas ainda ou cuja devolução está prevista para o futuro.
        locacoes_ativas = session.query(Locacao).filter_by(cliente_cpf=cpf).filter(Locacao.data_devolucao >= date.today()).count()
        limite_locacoes = 3  

        if locacoes_ativas >= limite_locacoes:
            raise LimiteLocacao(f"O cliente atingiu o limite de locações de {limite_locacoes} filmes.")

        locacao = Locacao(nomeFilme=nomeFilme, cliente_cpf=cpf)
        locacao.data = date.today()
        locacao.data_devolucao = locacao.data + timedelta(weeks=1)
        filme.qtdDisponivel -= 1
        session.add(locacao)
        session.commit()
        print(f'Locação realizada! Devolver até {locacao.data_devolucao}')
    
    except LimiteLocacao as e:
        print(e)  


def consultar_filmes():
    filmes = session.query(Filme).all()
    for filme in filmes:
        print(filme)

def consultar_diretores():
    diretores = session.query(Diretor).all()
    for diretor in diretores:
        print(diretor)

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
    data_hoje = date.today() + timedelta(days=15)
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


# adicionar diretor
# nome = input('Nome do Diretor: ') 
# nacionalidade = input('nacionalidade do diretor: ')
# adicionar_diretor(nome, nacionalidade)


# consultar_diretores()


# excluir diretor Solicitando o ID do diretor ao usuário
#id_diretor_str = input('id Diretor que deseja excluir: ')
#print("excluido com sucesso")
#try:
#   id_diretor = int(id_diretor_str)
#   excluir_diretor(id_diretor)
#except ValueError:
#   print("ID do diretor inválido. Por favor, insira um número inteiro.")


#adicionar cliente
# nome= input('Nome: ')
# cpf = input('cpf: ')
# dataNasc = input('Data de Nascimento: ')
# sexo = input('sexo: ')
# cadastrar_cliente(nome, cpf, dataNasc, sexo)

#excluir cliente
# cpf_usuario = input("Digite o CPF do cliente que deseja excluir: ")
# excluir_cliente(cpf_usuario)

#excluir filme
# titulo = input("Digite o filme que deseja excluir: ")
# excluir_filme(titulo)

#---------------------------

#adicionar filme
# titulo = input('Titulo do filme: ')
# ano = input('ano de lançamento: ')
# diretor = input('diretor: ')
# qtdDisponivel = int(input('quantidade: '))
# adicionar_filme(titulo, ano, diretor, qtdDisponivel)

# nomeFilme = input('Titulo do filme: ')
# cpf = input('cpf do cliente: ')
#fazer_locacao(nomeFilme,cpf)

# consultar_locacoes()

# teste devolução
# id= input('id da locação: ')
# nomeFilme=input('Titulo do filme: ')
# cpf= input('cpf do cliente: ')
# fazer_devolucao(id, nomeFilme, cpf)

#pagar_multa()
