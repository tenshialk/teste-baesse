from db import db
from flask_login import UserMixi

class Mensagem(db.Model):
    __tablename__ = 'mensagem'
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(30), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    anexo = db.Column(db.String(), nullable=True)
    mensagem = db.Column(db.Text, nullable=False)

