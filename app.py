from flask import Flask, render_template, request, redirect, flash, url_for


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']

    if not email.endswith(DOMINIO_INSTITUCIONAL):
        flash('E-mail inválido: utilize o e-mail institucional.')
        return redirect(url_for('index'))

    if email in USUARIOS and USUARIOS[email] == senha:
        return "Login realizado com sucesso!"
    else:
        flash('Senha incorreta ou usuário não encontrado.')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
