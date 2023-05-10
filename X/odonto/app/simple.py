from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


import os
app = Flask(__name__)
basedir = r'C:\Users\KAIQUEHENRIQUEVALIM\Documents\GitHub\Projetcs\X\odonto\instance'


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

from flask_migrate import Migrate
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





@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/del_db')
def del_db():
    db.drop_all()
    return render_template('index.html')

@app.route('/create_db')
def create_db():
    db.create_all()
    return render_template('index.html')


@app.route('/client')
def client():
    clients_in_db = Client.query.all()
    return render_template('client.html', clients=clients_in_db)

@app.route('/client_new', methods=['GET', 'POST'])
def client_new():
    if request.method != 'POST':
        return render_template('client_new.html')
    name = request.form['name']
    birthday = request.form['birthday']
    cpf = request.form['cpf']
    phone = request.form['phone']
    address = request.form['address']
    email = request.form['email']

    # Birthday string to date
    birthday = datetime.strptime(birthday, '%Y-%m-%d').date()

    if existing_client := Client.query.filter_by(email=email).first():
        # The client already exists, so we can't add it
        
        return redirect(url_for('error_page'))
    # The client does not exist, so we can add it
    client = Client(name=name, birthday=birthday, cpf=cpf, phone=phone, address=address, email=email)
    db.session.add(client)
    db.session.commit()

    return redirect(url_for('client'))


@app.route('/error')
def error_page():
    return render_template('error.html')



if __name__ == '__main__':
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    app.run(debug=True)
