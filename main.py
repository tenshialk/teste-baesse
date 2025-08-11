from flask import Flask, render_template, request, redirect, url_for, flash
import os
from flask_login import LoginManager, login_user, login_required, logout_user,current_user
from models import Usuario
from chamados import Chamado
from db import db
import hashlib

app = Flask(__name__)
app.secret_key = 'pizza'
im = LoginManager(app)
im.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db.init_app(app)

def hash(txt):
    hash_obj = hashlib.sha256(txt.encode('utf-8'))
    return hash_obj.hexdigest()
print(hash('oi'))

@im.user_loader
def load_user(id):
    Usuario = db.ssession.querey(Usuario).filter_by(id=id).first()
    return Usuario

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/pagina_principal')
def pagina_principal():
    return render_template('pagina_principal.html')

@app.route('/abrir_chamados')
def abrir_chamados():
    return render_template('opcoes.html')

@app.route('/meus_chamados')
def meus_chamados():
    chamados = Chamado.query.filter_by(usuario_id = 1)
    return render_template('meus_chamados.html',chamados = chamados)

@app.route('/enviar_mensagem', methods=['GET', 'POST'])
def enviar_mensagem():
    if request.method == 'POST':
                
        categoria = request.form.get('formcategoria')
        mensagem = request.form.get('formmensagem')
        matricula = request.form.get('formatricula')
           
        anexo = request.files.get('formAnexo')
        print(anexo.filename)
        print(mensagem)
        print(categoria)
        # Salvar arquivo se enviado
        if anexo and anexo.filename != '':
            caminho = os.path.join('uploads', anexo.filename)
            print(caminho)
            anexo.save(caminho)
            print(f"Arquivo salvo em: {caminho}")
        
            chamado = Chamado(usuario_id = 1 ,  categoria = categoria , anexo = caminho , mensagem = mensagem , matricula = matricula  )
        else:
            chamado = Chamado(usuario_id = 1 ,  categoria = categoria ,  mensagem = mensagem, matricula = matricula )
        db.session.add(chamado)
        db.session.commit()
        return "Cadastro enviado com sucesso!"
    return render_template('enviar_mensagem.html')


@app.route('/login', methods=[ 'POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        matricula = request.form['matriculaForm']
        senha = request.form['senhaForm']
        print(matricula.startswith('2021',))
        if matricula.startswith("2021"):
            return render_template('pagina_principal.html')
        return render_template('login.html')

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'GET':
        return render_template('registrar.html')
    elif request.method == 'POST':
        matricula = request.form['matriculaForm']
        senha = request.form['senhaForm']

        novo_usuario = Usuario(matricula=matricula, senha= hash(senha))
        db.session.add(novo_usuario)
        db.session.commit()
        
        login_user(novo_usuario)

    return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
