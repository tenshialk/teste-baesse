from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user,current_user
from models import Usuario
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
    return redirect(url_for('opcoes'))

@app.route('/opcoes')
def opcoes():
    return render_template('opcoes.html')  # renderiza a página de opções

@app.route('/enviar_mensagem')
def enviar_mensagem():
    return render_template('meus_chamados.html')

@app.route('/envia_mensagem', methods=['GET', 'POST'])
def envia_mensagem():
    area = request.args.get('area', 'geral')
    if request.method == 'GET':
        return render_template('envia_mensagem.html', area=area)
    else:
        # lógica para salvar mensagem
        return redirect(url_for('pagina_principal'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        matricula = request.form['matriculaForm']
        senha = request.form['senhaForm']
        if not matricula or not matricula.startswith("2021"):
            flash('Senha inválida', 'error')
        senha = hash(senha)
        user = db.session.query(Usuario).filter_by(matricula=matricula , senha=senha).first()
        if not user:
            return redirect(url_for('pagina_principal'))
        load_user(Usuario)


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
