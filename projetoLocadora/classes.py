from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import datetime, timezone, date


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

class Filme(Base):
    __tablename__ = 'filmes'
     
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    anoLancamento = Column(Integer)
    qtdDisponivel = Column(Integer)
    diretor_id = Column(Integer, ForeignKey('diretores.id'))
    diretor = relationship('Diretor', backref='filmes')
    
class Locacao(Base):
    __tablename__ = 'locação'
    
    id = Column(Integer, primary_key=True)
    data = Column(Date)
    disponibilidade = Column(Integer)
    
    
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
    data = Column(String)
    
# Criação das tabelas no banco de dados
Base.metadata.create_all(engine)

def adicionar_diretor(nome, nacionalidade):
    diretor = session.query(Diretor).filter_by(nome=nome).first()
    if not diretor:
        diretor = Diretor(nome=nome, nacionalidade = nacionalidade)
        session.add(diretor)
        session.commit()

def adicionar_filme(nome, ano, diretor):
    diretor = session.query(Diretor).filter_by(nome=nome).first()
    if not diretor:
        print(f"diretor: {diretor}, não foi encontrado")
        return
    
    filme = Filme(nome=nome, ano=ano, diretor=diretor)
    session.add(filme)
    session.commit()

def cadastrar_cliente(nome, cpf, dataNasc, sexo):
    cliente = session.query(Cliente).filter_by(cpf=cpf).first()
    if not cliente:
        print("Esse CPF já está cadastrado")
        return
    
    cliente = Cliente(nome=nome, cpf=cpf, dataNasc=dataNasc, sexo=sexo)
    session.add(cliente)
    session.commit()

def fazer_locacao():
    pass

#adicionar diretor
# nome = 'giovana' #input('Nome do Diretor: ') 
# nacionalidade = 'brasil' #input('nacionalidade do diretor')
# adicionar_diretor(nome, nacionalidade)

#adicionar cliente
# nome= input('Nome: ')
# cpf = input('cpf: ')
# dataNasc = input('Data de Nascimento: ')
# sexo = input('sexo: ')
# cadastrar_cliente(nome, cpf, dataNasc, sexo)
