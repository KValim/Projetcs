from flask import render_template, Blueprint, request, redirect, url_for
from app.models.procedure import Procedure
from app.database import db
import redi

procedures = Blueprint('procedures', __name__)

## HOME_PROCEDURE
@procedures.route('/procedure')
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

## NEW
@procedures.route('/procedure_new', methods=['GET', 'POST'])
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
            
            return redirect(url_for('procedures.procedure'))

    return render_template('procedure_new.html', error=error_message)

# EDIT
@procedures.route('/procedure_edit/<int:procedure_id>', methods=['GET', 'POST'])
def procedure_edit(procedure_id):
    procedure = Procedure.query.get(procedure_id)
    
    if procedure is None:
        return redirect(url_for('procedures.error_page')) 

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
            return redirect(url_for('procedures.procedure', procedure_id=procedure.id))
    else:  # Adicionando esta parte para preencher os campos quando o método for 'GET'
        name = procedure.name
        description = procedure.description
        price = procedure.price
        
    return render_template('procedure_edit.html', procedure=procedure, error=error_message, name=name, description=description, price=price)


# DELETE
@procedures.route('/delete_procedure/<int:procedure_id>', methods=['GET', 'POST'])
def delete_procedure(procedure_id):
    procedure = Procedure.query.get(procedure_id)
    
    if procedure is None:
        return redirect(url_for('procedures.error_page')) 

    db.session.delete(procedure)
    db.session.commit()
    return redirect(url_for('procedures.procedure')) 




### ERRO
@procedures.route('/error')
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
