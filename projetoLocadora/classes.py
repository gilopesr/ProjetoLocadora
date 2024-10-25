from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import date


#criação e conexão do banco de dados com POO
engine = create_engine('sqlite:///locadora.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

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
    qtdDisponivel = Column(Integer)
    diretor_id = Column(Integer, ForeignKey('diretores.id'))
    diretor = relationship('Diretor', backref='filmes')

    def __repr__(self):
        return f'Filme: (titulo={self.titulo}, diretor={self.diretor.nome})'

    
class Locacao(Base):
    __tablename__ = 'locação'
    
    id = Column(Integer, primary_key=True)
    nomeFilme = Column(String)
    data = date.today()
    disponibilidade = Column(Integer)
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
    
# Criação das tabelas no banco de dados
Base.metadata.create_all(engine)

def adicionar_diretor(nome, nacionalidade):
    diretor = session.query(Diretor).filter_by(nome=nome).first()
    if not diretor:
        diretor = Diretor(nome=nome, nacionalidade = nacionalidade)
        session.add(diretor)
        session.commit()

def adicionar_filme(titulo, anoLancamento, diretor, qtdDisponivel):
    diretor = session.query(Diretor).filter_by(nome=diretor).first()
    if not diretor:
        print(f"diretor: {diretor}, não foi encontrado")
        return
    
    filme = Filme(titulo=titulo, anoLancamento=anoLancamento, diretor=diretor, qtdDisponivel=qtdDisponivel)
    session.add(filme)
    session.commit()

def cadastrar_cliente(nome, cpf, dataNasc, sexo):
    cliente = session.query(Cliente).filter_by(cpf=cpf).first()
    if cliente:
        print("Esse CPF já está cadastrado")
        return
    
    cliente = Cliente(nome=nome, cpf=cpf, dataNasc=dataNasc, sexo=sexo)
    session.add(cliente)
    session.commit()

def fazer_locacao(nomeFilme, nomeCliente, cpf):
    filme = session.query(Filme).filter_by(titulo=nomeFilme).first()
    if not filme or filme.qtdDisponivel <= 0:
        print("O filme está indisponível para locação no momento")
        return
    
    locacao = Locacao(nomeFilme=nomeFilme, cliente=nomeCliente,cliente_cpf=cpf)
    filme.qtdDisponivel -= 1
    session.add(locacao)
    session.commit()



def consultar_filmes():
    filmes = session.query(Filme).all()
    for filme in filmes:
        print(filme)

def consultar_diretores():
    diretores = session.query(Diretor).all()
    for diretor in diretores:
        print(diretor)

def consulta_emprestimos():
    pass

#adicionar diretor
# nome = input('Nome do Diretor: ') 
# nacionalidade = input('nacionalidade do diretor')
# adicionar_diretor(nome, nacionalidade)

#adicionar cliente
# nome= input('Nome: ')
# cpf = input('cpf: ')
# dataNasc = input('Data de Nascimento: ')
# sexo = input('sexo: ')
# cadastrar_cliente(nome, cpf, dataNasc, sexo)

# consultar_diretores()
# titulo = 'harry potter 2'
# ano = 2012
# diretor = 'jk'
# qtdDisponivel = 3
# adicionar_filme(titulo, ano, diretor, qtdDisponivel)

nomeFilme = 'harry potter 2'
nomeCliente = 'giovana'
cpf = 1234678
fazer_locacao(nomeFilme, nomeCliente, cpf)


