from app.database import db

class Procedure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float(15), nullable=False)

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price
        
    def __repr__(self):
        return f'<Procedure {self.name}>'