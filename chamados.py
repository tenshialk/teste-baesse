from db import db
from flask_login import UserMixin

class Chamado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    matricula = db.Column(db.String(100), nullable=False)
    anexo = db.Column(db.String(200))  # caminho do arquivo salvo (opcional)
    mensagem = db.Column(db.Text, nullable=False)
    usuario = db.relationship('Usuario', backref='chamados')
