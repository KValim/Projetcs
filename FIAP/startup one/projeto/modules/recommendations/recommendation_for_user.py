import csv
import random

class RecommendationForUser:
    def __init__(self):
        # Carregando os produtos do CSV ao inicializar a classe
        self.produtos_csv = []
        with open('./data/produtos.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.produtos_csv.append(row)
    
    def get_recommendations(self, pet_data):
        pet_raca = pet_data.get('Raca', '')
        pet_especie = pet_data.get('Especie', '')
        
        # Filtrar produtos para a raça específica e produtos genéricos para a espécie
        produtos_relevantes = [produto for produto in self.produtos_csv if 
                               (produto['Especie'] == pet_especie and (produto['Raca'] == pet_raca or produto['Raca'] == 'Todos')) 
                               or (produto['Especie'] == 'Todos')]
        
        # Selecionar dois produtos aleatórios
        produtos_selecionados = random.sample(produtos_relevantes, min(2, len(produtos_relevantes)))

        return produtos_selecionados
