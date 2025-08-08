from db import db

class usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)


    def __init__(self,email, senha):
        self.email = email
        self.senha = senha
        
    def __repr__(self):
        return f"<Usuario {self.nome}>"