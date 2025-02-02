from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atividades.db'  # Caminho do banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Atividade
class Atividade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    turma = db.Column(db.String(80), nullable=False)
    nome = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    dataEntrega = db.Column(db.String(10), nullable=False)

# Modelo de Turma
class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    professor = db.Column(db.String(120), nullable=False)
    alunos = db.Column(db.Integer, nullable=False)

# Modelo de Usuário
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)

# Criar o banco de dados dentro do contexto da aplicação
with app.app_context():
    db.create_all()

# Rota para a página inicial
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# Rota para a página de login
@app.route('/login')
def login_page():
    return send_from_directory('static', 'home.html')

# Rota para o dashboard
@app.route('/dashboard')
def dashboard():
    return send_from_directory('static', 'cadastrarturma.html')

# Rota para turmas
@app.route('/turmas', methods=['GET'])
def get_turmas():
    turmas = Turma.query.all()
    turmas_lista = [
        {
            'id': turma.id,
            'nome': turma.nome,
            'descricao': turma.descricao,
            'professor': turma.professor,
            'alunos': turma.alunos
        } for turma in turmas
    ]
    return jsonify(turmas_lista)

# Rota para adicionar uma nova turma
@app.route('/turmas', methods=['POST'])
def add_turma():
    data = request.get_json()
    nova_turma = Turma(
        nome=data['nome'],
        descricao=data['descricao'],
        professor=data['professor'],
        alunos=data['alunos']
    )
    db.session.add(nova_turma)
    db.session.commit()
    return jsonify({"message": "Turma adicionada com sucesso!"}), 201

# Rota para deletar uma turma
@app.route('/turmas/<int:id>', methods=['DELETE'])
def delete_turma(id):
    turma = Turma.query.get_or_404(id)
    db.session.delete(turma)
    db.session.commit()
    return jsonify({"message": "Turma excluída com sucesso!"})

# Rota para obter todas as atividades
@app.route('/atividades', methods=['GET'])
def get_atividades():
    atividades = Atividade.query.all()
    atividades_lista = [
        {
            'id': atividade.id,
            'turma': atividade.turma,
            'nome': atividade.nome,
            'descricao': atividade.descricao,
            'dataEntrega': atividade.dataEntrega
        } for atividade in atividades
    ]
    return jsonify(atividades_lista)

# Rota para adicionar uma nova atividade
@app.route('/atividades', methods=['POST'])
def add_atividade():
    data = request.get_json()
    nova_atividade = Atividade(
        turma=data['turma'],
        nome=data['nome'],
        descricao=data['descricao'],
        dataEntrega=data['dataEntrega']
    )
    db.session.add(nova_atividade)
    db.session.commit()
    return jsonify({"message": "Atividade adicionada com sucesso!"}), 201

# Rota para deletar uma atividade
@app.route('/atividades/<int:id>', methods=['DELETE'])
def delete_atividade(id):
    atividade = Atividade.query.get_or_404(id)
    db.session.delete(atividade)
    db.session.commit()
    return jsonify({"message": "Atividade excluída com sucesso!"})

# Rota para exibir a página de atividades
@app.route('/atividades.html')
def atividades_html():
    return send_from_directory('static', 'atividades.html')

# Rota de cadastro de usuário
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    senha = data['password']

    # Verifica se o e-mail já está cadastrado
    usuario_existente = Usuario.query.filter_by(email=email).first()
    if usuario_existente:
        return jsonify({"message": "E-mail já cadastrado."}), 400

    # Cria um novo usuário
    novo_usuario = Usuario(email=email, senha=senha)
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201

# Rota de login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    senha = data['password']

    # Verifica se o usuário existe e a senha está correta
    usuario = Usuario.query.filter_by(email=email, senha=senha).first()
    if usuario:
        return jsonify({"message": "Login bem-sucedido!"}), 200
    else:
        return jsonify({"message": "Usuário ou senha incorretos."}), 401

# Iniciar o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
