from app import db

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_de_nascimento = db.Column(db.Date, nullable=False)
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    telefone = db.Column(db.String(15), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

class Procedimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # procedimento = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    preco = db.Column(db.Float, nullable=False)

class Consulta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    cliente = db.relationship('Cliente', backref=db.backref('consultas', lazy=True))
    data_e_hora_da_consulta = db.Column(db.DateTime, nullable=False)
    observacoes = db.Column(db.String(200))

class ConsultaProcedimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_consulta = db.Column(db.Integer, db.ForeignKey('consulta.id'), nullable=False)
    consulta = db.relationship('Consulta', backref=db.backref('consulta_procedimentos', lazy=True))
    id_procedimento = db.Column(db.Integer, db.ForeignKey('procedimento.id'), nullable=False)
    procedimento = db.relationship('Procedimento', backref=db.backref('consulta_procedimentos', lazy=True))

class Cobranca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_consulta = db.Column(db.Integer, db.ForeignKey('consulta.id'), nullable=False)
    consulta = db.relationship('Consulta', backref=db.backref('cobrancas', lazy=True))
    data_de_vencimento = db.Column(db.Date, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
