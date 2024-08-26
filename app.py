from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from config import db, DATABASE_URI
from models import Cliente, Treinador, Treino, Pagamento
from repositories.cliente_repository import ClienteRepository

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SECRET_KEY'] = 'minhachavesecreta'
db.init_app(app)

# @app.before_first_request
# def create_tables():
#     db.create_all()

with app.app_context():
    db.create_all()

# Inicialize o repositório
cliente_repo = ClienteRepository()

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        cliente = Cliente.query.filter_by(email=email).first()
        
        if cliente and cliente.verificar_senha(senha):
            session['cliente_id'] = cliente.id
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciais inválidas')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if Cliente.query.filter_by(email=email).first():
            flash('Email já cadastrado')
        else:
            cliente = Cliente(nome=nome, email=email)
            cliente.set_senha(senha)
            db.session.add(cliente)
            db.session.commit()
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('cliente_id', None)
    return redirect(url_for('login'))

# Página para listar clientes
@app.route('/clientes')
def show_clientes():
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Número de clientes por página
    clientes = cliente_repo.get_paginated(page=page, per_page=per_page)
    return render_template('clientes.html', clientes=clientes)

@app.route('/cliente/novo', methods=['GET'])
def new_cliente_form():
    return render_template('new_cliente.html')
  
@app.route('/cliente/<int:cliente_id>', methods=['POST'])
def delete_cliente(cliente_id):
    cliente = cliente_repo.get_by_id(cliente_id)
    cliente_repo.delete(cliente)
    return redirect(url_for('show_clientes'))

@app.route('/cliente', methods=['GET', 'POST'])
def add_cliente():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')

        if not nome or not email:
            return render_template('new_cliente.html', message='Nome e email são obrigatórios.')

        existing_cliente = cliente_repo.get_by_email(email)
        if existing_cliente:
            return render_template('new_cliente.html', message='Já existe um cliente com este e-mail.')

        cliente = Cliente(nome=nome, email=email, telefone=telefone)
        cliente_repo.add(cliente)
        
        return render_template('new_cliente.html', message='Cliente adicionado com sucesso!')
    
    return render_template('new_cliente.html')
  

@app.route('/dashboard')
def dashboard():
    if 'cliente_id' not in session:
        return redirect(url_for('login'))
    
    cliente_id = session['cliente_id']
    treinos = Treino.query.filter_by(cliente_id=cliente_id).all()
    pagamentos = Pagamento.query.filter_by(cliente_id=cliente_id).all()
    
    return render_template('dashboard.html', treinos=treinos, pagamentos=pagamentos)


# Outros Endpoints aqui (Treinador, Treino, Pagamento)

if __name__ == '__main__':
    app.run(debug=True)
