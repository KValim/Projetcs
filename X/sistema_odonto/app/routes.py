from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Cliente, Procedimento, Consulta, ConsultaProcedimento, Cobranca

@app.route('/')
def home():
    return render_template('index.html')

# Adicione suas rotas e funções de visualização aqui, por exemplo:
# Rotas para adicionar, editar, excluir e listar clientes, procedimentos, consultas e cobranças.

@app.route('/clientes')
def clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)

@app.route('/procedimentos')
def procedimentos():
    procedimentos = Procedimentos.query.all()
    return render_template('procedimentos.html', procedimentos=procedimentos)

@app.route('/consultas')
def consultas():
    consultas = Consultas.query.all()
    return render_template('consultas.html', consultas=consultas)

@app.route('/cobrancas')
def cobrancas():
    cobrancas = Cobrancas.query.all()
    return render_template('cobrancas.html', cobrancas=cobrancas)
