import csv
import random

class RecommendationBySpecies:
    def __init__(self):
        # Carregando os produtos do CSV ao inicializar a classe
        self.produtos_csv = []
        with open('./data/produtos.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.produtos_csv.append(row)
        
        # Carregando as espécies e raças do CSV ao inicializar a classe
        self.especies_racas = {}
        with open('./data/especie_raca.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                especie = row['Especie']
                raca = row['Raca']
                if especie not in self.especies_racas:
                    self.especies_racas[especie] = []
                self.especies_racas[especie].append(raca)
    
    def get_recommendations(self, pet_data):
        pet_raca = pet_data.get('Raca', '')
        pet_especie = pet_data.get('Especie', '')
        
        # Se a espécie do pet não estiver no arquivo, retorna uma lista vazia
        if pet_especie not in self.especies_racas:
            return []
        
        # Filtrar produtos para a raça e espécie específica ou para a espécie genérica
        produtos_relevantes = [
            produto for produto in self.produtos_csv if 
            (produto['Especie'] == pet_especie and (produto['Raca'] == pet_raca or produto['Raca'] == 'Todos')) 
            or (produto['Especie'] == 'Todos')
            ]
        
        # Selecionar dois produtos aleatórios
        produtos_selecionados = random.sample(produtos_relevantes, min(2, len(produtos_relevantes)))

        return produtos_selecionados
