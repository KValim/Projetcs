from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Client, Procedimento, Consulta, ConsultaProcedimento, Cobranca
from datetime import datetime

@app.route('/')
def home():
    return render_template('index.html')

# Client
@app.route('/client')
def client():
    client = Client.query.all()
    return render_template('client.html', clients=client)

@app.route('/client/new', methods=['GET', 'POST'])
def new_client():
    name = request.form['name']
    birthday = request.form['birthday']
    cpf = request.form['cpf']
    phone = request.form['phone']
    address = request.form['address']
    email = request.form['email']

    # Birthday string to date
    birthday = datetime.strptime(birthday, '%Y-%m-%d').date()

    client = Client(nome=nome, birthday=birthday, cpf=cpf, phone=phone, address=address, email=email)
    db.session.add(client)
    db.session.commit()

    return redirect(url_for('client'))

@app.route('/client/edit/<int:client_id>', methods=['GET'])
def edit_client(client_id):
    client = Client.query.get_or_404(client_id)
    return render_template('edit_client.html', client=client)

@app.route('/client/update/<int:client_id>', methods=['POST'])
def update_client(client_id):
    client = Client.query.get_or_404(client_id)
    client.name = request.form['name']
    client.birthday = datetime.strptime(request.form['birthday'], '%Y-%m-%d').date()
    client.cpf = request.form['cpf']
    client.phone = request.form['phone']
    client.address = request.form['address']
    client.email = request.form['email']
    
    db.session.commit()
    return redirect(url_for('client'))





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