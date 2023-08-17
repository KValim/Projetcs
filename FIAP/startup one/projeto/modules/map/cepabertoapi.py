import requests

class CepAbertoAPI:
    
    BASE_URL = "https://www.cepaberto.com/api/v3/cep"
    HEADERS = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    def __init__(self):
        self.api_key = self._get_api_key()
        self.HEADERS['Authorization'] = f'Token token={self.api_key}'

    def _get_api_key(self):
        # A melhor prática seria ler a chave de API de um arquivo de configuração, variável de ambiente ou um serviço de segredos.
        return '7770b096dc889c542625324cf26a3e7b'

    def _sanitize_cep(self, cep):
        # Remove espaços, hifens e mantém apenas números.
        return ''.join(filter(str.isdigit, cep))

    def get_lat_lon_from_cep(self, cep):
        sanitized_cep = self._sanitize_cep(cep)
        
        response = requests.get(f"{self.BASE_URL}?cep={sanitized_cep}", headers=self.HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            return float(data['latitude']), float(data['longitude'])

        else:
            print(f"Erro ao buscar o CEP. Status code: {response.status_code}")
            return None, None
