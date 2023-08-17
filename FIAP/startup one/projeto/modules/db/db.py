import json
import datetime

def load_users_data(filename='users_data.json'):
    """Carregar os dados dos usuários do arquivo JSON."""
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            for user, user_data in data.items():
                pet_data = user_data.get('pet_data', {})
                if 'Data de Nascimento do Pet' in pet_data:
                    pet_data['Data de Nascimento do Pet'] = datetime.datetime.strptime(pet_data['Data de Nascimento do Pet'], '%Y-%m-%d').date()
            return data
    except FileNotFoundError:
        return {}


def date_converter(obj):
    if isinstance(obj, datetime.date):
        return obj.strftime('%Y-%m-%d')
    raise TypeError("Type not serializable")

def save_users_data(users_data, filename='users_data.json'):
    """Salvar os dados dos usuários no arquivo JSON."""
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(users_data, file, indent=4, default=date_converter, ensure_ascii=False)
