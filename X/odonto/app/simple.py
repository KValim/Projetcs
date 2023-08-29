from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import or_
from datetime import datetime

import re
import os
import phonenumbers

app = Flask(__name__)
basedir = r'../instance'


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


migrate = Migrate(app, db)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, name, birthday, cpf, phone, address, email):
        self.name = name
        self.birthday = birthday
        self.cpf = cpf
        self.phone = phone
        self.address = address
        self.email = email
        
        
class Procedure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float(15), nullable=False)

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price


class ClientProcedure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    procedure_id = db.Column(db.Integer, db.ForeignKey('procedure.id'), nullable=False)
    duration = db.Column(db.String(10), nullable=True)
    teeth_involved = db.Column(db.String(50), nullable=True)
    procedure = db.relationship('Procedure', backref='client_procedures')

    def __init__(self, client_id, procedure_id, duration=None, teeth_involved=None):
        self.client_id = client_id
        self.procedure_id = procedure_id
        self.duration = duration
        self.teeth_involved = teeth_involved

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    client_procedure_id = db.Column(db.Integer, db.ForeignKey('client_procedure.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, client_id, client_procedure_id, appointment_date):
        self.client_id = client_id
        self.client_procedure_id = client_procedure_id
        self.appointment_date = appointment_date





### DB

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/del_db')
def del_db():
    db.drop_all()
    return render_template('index.html')

@app.route('/create_db')
def create_db():
    db.create_all()
    return render_template('index.html')



### HOME

@app.route('/')
def home():
    return render_template('index.html')




### CLIENTE

@app.route('/client')
def client():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', None, type=int)
    search = request.args.get('search', '')

    if search:
        query = Client.query.filter(Client.name.ilike(f'%{search}%'))
    else:
        query = Client.query

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    clients = pagination.items

    return render_template('client.html', clients=clients, pagination=pagination, search=search, per_page=per_page)


## NOVO
@app.route('/client_new', methods=['GET', 'POST'])
def client_new():  # sourcery skip: low-code-quality
    error_message = ''
    if request.method == 'POST':
        name = request.form.get('name')
        birthday = request.form.get('birthday')
        cpf = request.form.get('cpf')
        phone = request.form.get('phone')
        address = request.form.get('address')
        email = request.form.get('email')

        # Verificando se todos os campos foram preenchidos
        if not all([name, birthday, cpf, phone, address, email]):
            error_message = 'Por favor, preencha todos os campos.'
        else:
            # Adicionando validações de formato
            if not re.match("^[a-zA-Z\s]*$", name):
                error_message = 'Nome inválido. Por favor, insira um nome válido.'
            try:
                birthday = datetime.strptime(birthday, '%Y-%m-%d').date()
            except ValueError:
                error_message = 'Data de nascimento inválida. Por favor, insira a data no formato AAAA-MM-DD.'
            if not re.match("^\d{3}\.\d{3}\.\d{3}-\d{2}$", cpf):  # Validando formato de CPF
                error_message = 'CPF inválido. Por favor, insira um CPF válido.'
            if existing_client := Client.query.filter_by(cpf=cpf).first():
                # O cliente já existe, então não podemos adicioná-lo
                error_message = 'CPF já registrado.'
            try:
                # Adiciona o código do país (Brasil = 55)
                phone_55 = f'+55{phone}'
                # Faz o parse do telefone
                phone_number = phonenumbers.parse(phone_55, None)
                # Verifica se o número é válido
                if not phonenumbers.is_valid_number(phone_number):
                    raise ValueError
                # Remove todos os caracteres não numéricos do telefone
                phone = re.sub("[^0-9]", "", phone)
            except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
                error_message = 'Telefone inválido. Por favor, insira um número de telefone válido.'
            if not re.match("^[\w\.-]+@[\w\.-]+\.\w+$", email):  # Validando formato de e-mail
                error_message = 'E-mail inválido. Por favor, insira um e-mail válido.'
            if existing_client := Client.query.filter_by(email=email).first():
                # O cliente já existe, então não podemos adicioná-lo
                error_message = 'E-mail já registrado.'


        if not error_message:
            # O cliente não existe e os dados são válidos, então podemos adicioná-lo
            client = Client(name=name, birthday=birthday, cpf=cpf, phone=phone, address=address, email=email)
            db.session.add(client)
            db.session.commit()
            
            return redirect(url_for('client'))

    return render_template('client_new.html', error=error_message)


## EDIT

@app.route('/client_edit/<int:client_id>', methods=['GET', 'POST'])
def client_edit(client_id):  # sourcery skip: low-code-quality
    client = Client.query.get(client_id)
    name = ''
    birthday = ''
    cpf = ''
    phone = ''
    address = ''
    email = ''

    if client is None:
        return redirect(url_for('error_page')) 

    error_message = ''
    if request.method == 'POST':
        name = request.form.get('name')
        birthday = request.form.get('birthday')
        cpf = request.form.get('cpf')
        phone = request.form.get('phone')
        address = request.form.get('address')
        email = request.form.get('email')

        # Verificando se todos os campos foram preenchidos
        if not all([name, birthday, cpf, phone, address, email]):
            error_message = 'Por favor, preencha todos os campos.'
        else:
            # Adicionando validações de formato
            if not re.match("^[a-zA-Z\s]*$", name):
                error_message = 'Nome inválido. Por favor, insira um nome válido.'
            try:
                birthday = datetime.strptime(birthday, '%Y-%m-%d').date()
            except ValueError:
                error_message = 'Data de nascimento inválida. Por favor, insira a data no formato AAAA-MM-DD.'
            if not re.match("^\d{3}\.\d{3}\.\d{3}-\d{2}$", cpf):  # Validando formato de CPF
                error_message = 'CPF inválido. Por favor, insira um CPF válido.'
            try:
                # Adiciona o código do país (Brasil = 55)
                phone_55 = f'+55{phone}'
                # Faz o parse do telefone
                phone_number = phonenumbers.parse(phone_55, None)
                # Verifica se o número é válido
                if not phonenumbers.is_valid_number(phone_number):
                    raise ValueError
                # Remove todos os caracteres não numéricos do telefone
                phone = re.sub("[^0-9]", "", phone)
            except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
                error_message = 'Telefone inválido. Por favor, insira um número de telefone válido.'
            if not re.match("^[\w\.-]+@[\w\.-]+\.\w+$", email):  # Validando formato de e-mail
                error_message = 'E-mail inválido. Por favor, insira um e-mail válido.'
            # Verificando se o email mudou e se o novo email já está registrado
            if client.email != email and Client.query.filter_by(email=email).first():
                error_message = 'E-mail já registrado.'

        if not error_message:
            # O cliente existe e os dados são válidos, então podemos altera-lo
            client.name = name
            client.birthday = birthday
            client.cpf = cpf
            client.phone = phone
            client.address = address
            client.email = email
            db.session.commit()
            return redirect(url_for('client', client_id=client.id))
        
    return render_template('client_edit.html', client=client, error=error_message, name=name, birthday=birthday, cpf=cpf, phone=phone, address=address, email=email)

## DELETE
@app.route('/delete_client/<int:client_id>', methods=['GET', 'POST'])
def delete_client(client_id):
    client = Client.query.get(client_id)
    if client is None:
        return redirect(url_for('error_page'))  # Você pode redirecionar para uma página de erro personalizada se o cliente não existir

    db.session.delete(client)
    db.session.commit()
    return redirect(url_for('client'))  # Redireciona para a página do cliente após a exclusão



### PROCEDIMENTO

@app.route('/procedure')
def procedure():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', None, type=int)
    search = request.args.get('search', '')

    if search:
        query = Procedure.query.filter(Procedure.name.ilike(f'%{search}%'))
    else:
        query = Procedure.query

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    procedures = pagination.items

    return render_template('procedure.html', procedures=procedures, pagination=pagination, search=search, per_page=per_page)


@app.route('/procedure_new', methods=['GET', 'POST'])
def procedure_new():
    error_message = ''
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')

        if not all([name, description, price]):
            error_message = 'Por favor, preencha todos os campos.'
        else:
            procedure = Procedure(name=name, description=description, price=price)
            db.session.add(procedure)
            db.session.commit()
            
            return redirect(url_for('procedure'))

    return render_template('procedure_new.html', error=error_message)


@app.route('/procedure_edit/<int:procedure_id>', methods=['GET', 'POST'])
def procedure_edit(procedure_id):
    procedure = Procedure.query.get(procedure_id)
    
    if procedure is None:
        return redirect(url_for('error_page')) 

    error_message = ''
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')

        if not all([name, description, price]):
            error_message = 'Por favor, preencha todos os campos.'
        else:
            if not re.match("^[a-zA-Z\s]*$", name):
                error_message = 'Nome inválido. Por favor, insira um nome válido.'    
            if not re.match("^[a-zA-Z\s]*$", description):
                error_message = 'Descrição inválido. Por favor, insira uma descrição válido.'  
            if not re.match("^\d+(\.\d{1,2})?$", price):  # Corrigindo a validação do preço
                error_message = 'Preço inválido. Por favor, insira um preço válido.'  
            
        if not error_message:
            procedure.name = name
            procedure.description = description
            procedure.price = price
            db.session.commit()
            return redirect(url_for('procedure', procedure_id=procedure.id))
    else:  # Adicionando esta parte para preencher os campos quando o método for 'GET'
        name = procedure.name
        description = procedure.description
        price = procedure.price
        
    return render_template('procedure_edit.html', procedure=procedure, error=error_message, name=name, description=description, price=price)



@app.route('/delete_procedure/<int:procedure_id>', methods=['GET', 'POST'])
def delete_procedure(procedure_id):
    procedure = Procedure.query.get(procedure_id)
    
    if procedure is None:
        return redirect(url_for('error_page')) 

    db.session.delete(procedure)
    db.session.commit()
    return redirect(url_for('procedure')) 


### CLIENT PROCEDURE

@app.route('/client_procedures/<int:client_id>')
def client_procedures(client_id):
    client = Client.query.get(client_id)
    if client is None:
        return redirect(url_for('error_page'))

    procedures = ClientProcedure.query.filter_by(client_id=client_id).all()
    return render_template('client_procedures.html', client=client, procedures=procedures)


@app.route('/add_procedure_to_client/<int:client_id>', methods=['GET', 'POST'])
def add_procedure_to_client(client_id):
    client = Client.query.get(client_id)
    if client is None:
        return redirect(url_for('error_page'))
    
    if request.method == 'POST':
        procedure_id = request.form.get('procedure_id')
        duration = request.form.get('duration')
        teeth_involved = request.form.get('teeth_involved')

        client_procedure = ClientProcedure(client_id, procedure_id, duration, teeth_involved)
        db.session.add(client_procedure)
        db.session.commit()
        
        return redirect(url_for('client_procedures', client_id=client_id))

    procedures = Procedure.query.all()
    return render_template('add_procedure_to_client.html', client=client, procedures=procedures)

@app.route('/edit_client_procedure/<int:client_procedure_id>', methods=['GET', 'POST'])
def edit_client_procedure(client_procedure_id):
    client_procedure = ClientProcedure.query.get(client_procedure_id)
    if client_procedure is None:
        return redirect(url_for('error_page'))

    client = Client.query.get(client_procedure.client_id)
    if client is None:
        return redirect(url_for('error_page'))

    if request.method == 'POST':
        try:
            # Capture os dados do formulário
            procedure_id = request.form.get('procedure_id')
            duration = request.form.get('duration')
            teeth_involved = request.form.get('teeth_involved')

            # Verifique se os campos estão vazios
            if not procedure_id or not duration:
                return "Campos obrigatórios estão vazios", 400

            # Atualize os campos
            client_procedure.procedure_id = procedure_id
            client_procedure.duration = duration
            client_procedure.teeth_involved = teeth_involved

            # Faça o commit das alterações
            db.session.commit()
            return redirect(url_for('client_procedures', client_id=client.id))

        except Exception as e:
            # Faça o rollback em caso de erro e imprima a exceção para depuração
            db.session.rollback()
            print("Erro: ", e)
            return "Ocorreu um erro ao atualizar o procedimento", 500



    procedures = Procedure.query.all()
    procedure = Procedure.query.get(client_procedure.procedure_id)

    return render_template('edit_client_procedure.html', client=client, client_procedure=client_procedure, procedures=procedures, procedure=procedure)


@app.route('/delete_client_procedure/<int:client_procedure_id>', methods=['POST'])
def delete_client_procedure(client_procedure_id):
    """Exclui um procedimento associado a um cliente."""
    client_procedure = ClientProcedure.query.get(client_procedure_id)
    if client_procedure is None:
        return redirect(url_for('error_page'))

    client_id = client_procedure.client_id
    db.session.delete(client_procedure)
    db.session.commit()
    return redirect(url_for('client_procedures', client_id=client_id))


### AGENDA
# Exibir agendamentos
@app.route('/appointments')
def appointments():
    all_appointments = Appointment.query.all()
    return render_template('appointments.html', appointments=all_appointments)

# Novo agendamento
@app.route('/appointment_new', methods=['GET', 'POST'])
@app.route('/appointment_new/<int:client_id>/<int:procedure_id>', methods=['GET', 'POST'])
def appointment_new(client_id=None, procedure_id=None):
    if request.method == 'POST':
        client_id = request.form.get('client_id')
        procedure_id = request.form.get('client_procedure_id')  # Certifique-se de que este valor está sendo capturado
        appointment_date = request.form.get('appointment_date')

        if not client_id or not procedure_id or not appointment_date:
            flash('Todos os campos são obrigatórios', 'error')
            return redirect(request.url)
        
        appointment_date = datetime.strptime(appointment_date, '%Y-%m-%dT%H:%M')
        
        new_appointment = Appointment(
            client_id=client_id, 
            client_procedure_id=procedure_id,  # Certifique-se de que este valor está sendo passado
            appointment_date=appointment_date
        )
        db.session.add(new_appointment)
        db.session.commit()
        flash('Agendamento criado com sucesso!', 'success')
        return redirect(url_for('appointments'))


    # Obter informações do cliente e do procedimento para pré-preencher o formulário
    clients = db.session.query(Client).all()  # Substitua Client pelo seu modelo de Cliente
    procedures = db.session.query(Procedure).all()  # Substitua Procedure pelo seu modelo de Procedimento

    return render_template(
        'appointment_new.html', 
        clients=clients, 
        procedures=procedures, 
        selected_client_id=client_id, 
        selected_procedure_id=procedure_id
    )

# Editar agendamento
@app.route('/appointment_edit/<int:appointment_id>', methods=['GET', 'POST'])
def appointment_edit(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if request.method == 'POST':
        appointment.client_id = request.form.get('client_id')
        appointment.client_procedure_id = request.form.get('client_procedure_id')
        appointment.appointment_date = request.form.get('appointment_date')

        db.session.commit()
        return redirect(url_for('appointments'))

    clients = Client.query.all()
    return render_template('appointment_edit.html', appointment=appointment, clients=clients)

# Excluir agendamento
@app.route('/delete_appointment/<int:appointment_id>', methods=['GET', 'POST'])
def delete_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    return redirect(url_for('appointments'))




### ERRO

@app.route('/error')
def error_page():
    return render_template('error.html')

### FUNÇÕES

@app.context_processor
def utility_processor():
    def format_phone_number(num):
        return f"({num[:2]}) {num[2]} {num[3:7]} {num[7:]}"
    return dict(format_phone_number=format_phone_number)

@app.template_filter()
def currency_format(value):
    return f'R$ {value:,.2f}'.replace(",", "#").replace(".", ",").replace("#", ".")



if __name__ == '__main__':
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    app.debug = True
    app.run()
