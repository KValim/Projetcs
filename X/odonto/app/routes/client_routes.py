import phonenumbers
import re

from flask import render_template, Blueprint, request, redirect, url_for
from app.models.client import Client
from datetime import datetime

clients = Blueprint('clients', __name__)


### DB
from app.database import db
@clients.before_app_first_request
def create_tables():
    db.create_all()

@clients.route('/del_db')
def del_db():
    db.drop_all()
    return render_template('index.html')

@clients.route('/create_db')
def create_db():
    db.create_all()
    return render_template('index.html')



### HOME

@clients.route('/')
def home():
    return render_template('index.html')


## HOME_CLIENT
@clients.route('/client')
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
@clients.route('/client_new', methods=['GET', 'POST'])
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
            
            return redirect(url_for('clients.client'))

    return render_template('client_new.html', error=error_message)


## EDIT

@clients.route('/clients.client_edit/<int:client_id>', methods=['GET', 'POST'])
def client_edit(client_id):  # sourcery skip: low-code-quality
    client = Client.query.get(client_id)
    name = ''
    birthday = ''
    cpf = ''
    phone = ''
    address = ''
    email = ''

    if client is None:
        return redirect(url_for('clients.error_page')) 

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
@clients.route('/delete_client/<int:client_id>', methods=['GET', 'POST'])
def delete_client(client_id):
    client = Client.query.get(client_id)
    if client is None:
        return redirect(url_for('clients.error_page'))  # Você pode redirecionar para uma página de erro personalizada se o cliente não existir

    db.session.delete(client)
    db.session.commit()
    return redirect(url_for('clients.client'))  # Redireciona para a página do cliente após a exclusão



### ERRO
@clients.route('/error')
def error_page():
    return render_template('error.html')

def register_filters(app):
    @app.template_filter()
    def currency_format(value):
        return f'R$ {value:,.2f}'.replace(",", "#").replace(".", ",").replace("#", ".")

    @app.context_processor
    def utility_processor():
        def format_phone_number(num):
            return f"({num[:2]}) {num[2]} {num[3:7]} {num[7:]}"
        return dict(format_phone_number=format_phone_number)
