from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Cliente, Procedimento, Consulta, ConsultaProcedimento, Cobranca
from datetime import datetime

@app.route('/')
def home():
    return render_template('index.html')

# Adicione suas rotas e funções de visualização aqui, por exemplo:
# Rotas para adicionar, editar, excluir e listar clientes, procedimentos, consultas e cobranças.

# Clientes
@app.route('/clientes')
def clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)

@app.route('/clientes/novo', methods=['GET', 'POST'])
def novo_cliente():
    nome = request.form['nome']
    data_de_nascimento = request.form['data_de_nascimento']
    cpf = request.form['cpf']
    telefone = request.form['telefone']
    endereco = request.form['endereco']
    email = request.form['email']

    # Convertendo a string da data em um objeto date
    data_de_nascimento = datetime.strptime(data_de_nascimento, '%Y-%m-%d').date()

    cliente = Cliente(nome=nome, data_de_nascimento=data_de_nascimento, cpf=cpf, telefone=telefone, endereco=endereco, email=email)
    db.session.add(cliente)
    db.session.commit()

    return redirect(url_for('clientes'))

@app.route('/clientes/editar/<int:cliente_id>', methods=['GET'])
def editar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    return render_template('editar_clientes.html', cliente=cliente)

@app.route('/clientes/atualizar/<int:cliente_id>', methods=['POST'])
def atualizar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    cliente.nome = request.form['nome']
    cliente.data_de_nascimento = datetime.strptime(request.form['data_de_nascimento'], '%Y-%m-%d').date()
    cliente.cpf = request.form['cpf']
    cliente.telefone = request.form['telefone']
    cliente.endereco = request.form['endereco']
    cliente.email = request.form['email']
    
    db.session.commit()
    return redirect(url_for('clientes'))





# Procedimentos
@app.route('/procedimentos')
def procedimentos():
    procedimentos = Procedimento.query.all()
    return render_template('procedimentos.html', procedimentos=procedimentos)

# @app.route('/procedimentos/novo', methods=['GET', 'POST'])
# def novo_procedimento():
#     if request.method == 'POST':
#         nome = request.form['nome']
#         descricao = request.form['descricao']
#         preco = request.form['preco']
        
#         novo_procedimento = Procedimento(nome=nome, descricao=descricao, preco=preco)
#         db.session.add(novo_procedimento)
#         db.session.commit()

#         return redirect(url_for('procedimentos'))

#     return render_template('novo_procedimento.html')


# @app.route('/procedimentos/editar/<int:id>', methods=['GET', 'POST'])
# def editar_procedimento(id):
#     procedimento = Procedimento.query.get(id)
    
#     if request.method == 'POST':
#         procedimento.nome = request.form['nome']
#         procedimento.descricao = request.form['descricao']
#         procedimento.preco = request.form['preco']

#         db.session.commit()

#         return redirect(url_for('procedimentos'))

#     return render_template('editar_procedimento.html', procedimento=procedimento)

# @app.route('/procedimentos/<int:procedimento_id>/delete', methods=['POST'])
# def excluir_procedimento(procedimento_id):
#     procedimento = Procedimento.query.get_or_404(procedimento_id)
#     db.session.delete(nome)
#     db.session.commit()
#     flash('Procedimento excluído com sucesso.')
#     return redirect(url_for('procedimentos'))

# Consultas
@app.route('/consultas')
def consultas():
    consultas = Consulta.query.all()
    return render_template('consultas.html', consultas=consultas)

@app.route('/consultas/nova', methods=['GET', 'POST'])
def nova_consulta():
    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        data_e_hora_da_consulta = request.form['data_e_hora_da_consulta']
        observacoes = request.form['observacoes']
        
        
        # Convertendo a string da data em um objeto date
        data_e_hora_da_consulta = datetime.strptime(data_e_hora_da_consulta, '%Y-%m-%dT%H:%M').date()

        
        nova_consulta = Consulta(id_cliente=id_cliente, data_e_hora_da_consulta=data_e_hora_da_consulta, observacoes=observacoes)
        db.session.add(nova_consulta)
        db.session.commit()

        return redirect(url_for('consultas'))

    return render_template('nova_consulta.html')

@app.route('/consultas/editar/<int:id>', methods=['GET', 'POST'])
def editar_consulta(id):
    consulta = Consulta.query.get(id)
    
    if request.method == 'POST':
        consulta.id_cliente = request.form['id_cliente']
        consulta.data_e_hora_da_consulta = request.form['data_e_hora_da_consulta']
        consulta.observacoes = request.form['observacoes']

        db.session.commit()

        return redirect(url_for('consultas'))

    return render_template('editar_consulta.html', consulta=consulta)

@app.route('/consultas/excluir/<int:id>')
def excluir_consulta(id):
    consulta = Consulta.query.get(id)
    db.session.delete(consulta)
    db.session.commit()

    return redirect(url_for('consultas'))

# Cobranças
@app.route('/cobrancas')
def cobrancas():
    cobrancas = Cobranca.query.all()
    return render_template('cobrancas.html', cobrancas=cobrancas)

@app.route('/cobrancas/nova', methods=['GET', 'POST'])
def nova_cobranca():
    if request.method == 'POST':
        id_consulta = request.form['id_consulta']
        data_de_vencimento = request.form['data_de_vencimento']
        valor_total = request.form['valor_total']
        status = request.form['status']
        
        # Convertendo a string da data em um objeto date
        data_de_vencimento = datetime.strptime(data_de_vencimento, '%Y-%m-%d').date()

        
        nova_cobranca = Cobranca(id_consulta=id_consulta, data_de_vencimento=data_de_vencimento, valor_total=valor_total, status=status)
        db.session.add(nova_cobranca)
        db.session.commit()

        return redirect(url_for('cobrancas'))

    return render_template('nova_cobranca.html')

@app.route('/cobrancas/editar/<int:id>', methods=['GET', 'POST'])
def editar_cobranca(id):
    cobranca = Cobranca.query.get(id)
    
    if request.method == 'POST':
        cobranca.id_consulta = request.form['id_consulta']
        cobranca.data_de_vencimento = request.form['data_de_vencimento']
        cobranca.valor_total = request.form['valor_total']
        cobranca.status = request.form['status']

        db.session.commit()

        return redirect(url_for('cobrancas'))

    return render_template('editar_cobranca.html', cobranca=cobranca)

@app.route('/cobrancas/excluir/<int:id>')
def excluir_cobranca(id):
    cobranca = Cobranca.query.get(id)
    db.session.delete(cobranca)
    db.session.commit()

    return redirect(url_for('cobrancas'))