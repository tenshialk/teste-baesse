from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'minha_chave_secreta'

# Usuário de exemplo
USUARIOS = {
    'admin': '1234',
    'mariana': 'abcd'
}

@app.route('/')
def home():
    if 'usuario' in session:
        return f"Bem-vindo(a), {session['usuario']}! <a href='/logout'>Sair</a>"
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if usuario in USUARIOS and USUARIOS[usuario] == senha:
            session['usuario'] = usuario
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('home'))
        # Nenhuma mensagem em caso de erro
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Você saiu da conta.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
