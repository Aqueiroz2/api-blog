from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'KkasjkajAAASJHKXLKS@#$,LMAM2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:CxyZpOggR2MmF1GY@db.ihxzozdgxmebnupixdji.supabase.co:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db: SQLAlchemy


class Postagem(db.Model):
    __tablename__ = 'postagem'
    id_postagem = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    id_autor = db.Column(db.Integer, db.ForeignKey(
        'autor.id_autor'), nullable=False)


class Autor(db.Model):
    __tablename = 'autor'
    id_autor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    senha = db.Column(db.String)
    admin = db.Column(db.Boolean)
    postagens = db.relationship('Postagem')


def inicializar_banco():
    with app.app_context():
        db.drop_all()
        db.create_all()
        autor = Autor(nome='Alison', email='alissontenob.aq@gmail.com',
                      senha='qd10cs02', admin=True)
        db.session.add(autor)
        db.session.commit()


if __name__ == '__main__':
    inicializar_banco()
