from app.database import db

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

    def __repr__(self):
        return f'<Client {self.name}>'

