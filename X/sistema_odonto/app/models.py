from app import db

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

class Procedimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    procedimento = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    preco = db.Column(db.Float, nullable=False)

class Consulta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_client = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    client = db.relationship('Client', backref=db.backref('consultas', lazy=True))
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
