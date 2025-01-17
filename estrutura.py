import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Configuração do logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),  # Log no console
        logging.FileHandler("app.log")  # Salva logs em arquivo
    ]
)

# Inicializando o app Flask
app = Flask(__name__)

# Configuração do banco de dados (usando variáveis de ambiente)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URI',
    'postgresql://postgres.fiubhlapstreyxlyejic:CxyZpOggR2MmF1GY@db@aws-0-us-west-1.pooler.supabase.com:5432/postgres'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db: SQLAlchemy


# Modelos
class Postagem(db.Model):
    __tablename__ = 'postagem'
    id_postagem = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    id_autor = db.Column(db.Integer, db.ForeignKey(
        'autor.id_autor'), nullable=False)


class Autor(db.Model):
    __tablename__ = 'autor'
    id_autor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    senha = db.Column(db.String)
    admin = db.Column(db.Boolean)
    postagens = db.relationship('Postagem')


# Inicializando o banco de dados
def inicializar_banco():
    logging.info("Iniciando inicialização do banco de dados.")
    try:
        with app.app_context():
            logging.debug("Contexto do aplicativo Flask inicializado.")
            db.drop_all()
            logging.info("Todas as tabelas foram excluídas.")

            db.create_all()
            logging.info("Todas as tabelas foram recriadas.")

            # Criando um autor inicial
            autor = Autor(nome='Alison', email='alissontenob.aq@gmail.com',
                          senha='qd10cs02', admin=True)
            db.session.add(autor)
            db.session.commit()
            logging.info("Autor inicial criado com sucesso.")
    except Exception as e:
        logging.error(
            "Erro durante a inicialização do banco de dados.", exc_info=True)
    finally:
        logging.debug("Processo de inicialização do banco de dados concluído.")


if __name__ == '__main__':
    logging.info("Aplicação iniciada.")
    inicializar_banco()
    logging.info("Aplicação finalizada.")
