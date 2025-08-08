from flask import flask 
from models import Usuario
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'GET':
        return render_template('registrar.html')
    if request.method == 'GET':
    elif request.method == 'POST':
        email  = request.form[emailform]
        senha = request.form[senhaform]
        
        novo_usuario = Usuario(email=email, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()

        return redirect(url_for('Url_for(''home)'))  # Redirect to login page after registration
          

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)  # Run the Flask application



    