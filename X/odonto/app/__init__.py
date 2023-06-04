from flask import Flask
from .database import db
from .routes.client_routes import clients, register_filters
from .routes.procedure_routes import procedures

app = Flask(__name__)
app.config.from_object('config')

app.register_blueprint(clients)
app.register_blueprint(procedures)

register_filters(app)

db.init_app(app)