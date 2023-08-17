import csv
import random

class GeneralRecommendations:
    def __init__(self):
        # Carregando os produtos do CSV ao inicializar a classe
        self.produtos_csv = []
        with open('./data/produtos.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.produtos_csv.append(row)
    
    def get_recommendations(self):
        # Retornar 3 produtos aleatórios
        return random.sample(self.produtos_csv, min(3, len(self.produtos_csv)))
