import os
from typing import List, Optional

class DirectoryStructure:
    """Classe para gerar a estrutura de diretórios e arquivos."""

    INDENT = "    "
    PIPE = "|"
    DASH = "-- "

    def __init__(self, root_path: str, ignore_list: Optional[List[str]] = None, debug: bool = False):
        """
        Inicializa a classe com o diretório raiz e a lista de ignorados.

        Args:
            root_path (str): O caminho do diretório raiz.
            ignore_list (Optional[List[str]]): Lista de nomes de arquivos e pastas para ignorar.
            debug (bool): Modo de depuração.
        """
        self.root_path = root_path
        self.ignore_list = ignore_list if ignore_list else []
        self.debug = debug

    def _generate_structure(self, path: str, level: int):
        """
        Gera a estrutura de diretórios e arquivos de forma recursiva.

        Args:
            path (str): O caminho atual para listar.
            level (int): O nível de indentação atual.

        Returns:
            str: A estrutura de diretórios e arquivos como uma string.
        """
        structure = ""
        try:
            for item in os.listdir(path):
                if item in self.ignore_list:
                    continue

                indent = self.INDENT * level
                structure += f"{indent}{self.PIPE}{self.DASH}{item}\n"

                new_path = os.path.join(path, item)
                if os.path.isdir(new_path):
                    structure += self._generate_structure(new_path, level + 1)
        except Exception as e:
            if self.debug:
                print(f"An error occurred: {e}")
        
        return structure

    def generate_structure(self):
        """
        Inicia a geração da estrutura de diretórios e arquivos.

        Returns:
            str: A estrutura de diretórios e arquivos como uma string.
        """
        return self._generate_structure(self.root_path, 0)

    def save_structure_to_txt(self, file_name: str):
        """
        Salva a estrutura de diretórios e arquivos em um arquivo de texto.

        Args:
            file_name (str): O nome do arquivo de texto onde a estrutura será salva.
        """
        structure = self.generate_structure()
        try:
            with open(file_name, "w") as f:
                f.write(structure)
        except Exception as e:
            if self.debug:
                print(f"An error occurred while saving to txt: {e}")


# Lista de arquivos e pastas para ignorar
ignore_list = ['__pycache__', '.git', '.env']

# Crie uma instância da classe
dir_structure = DirectoryStructure('.', ignore_list=ignore_list)

# Salva a estrutura do diretório em um arquivo txt
dir_structure.save_structure_to_txt("directory_structure.txt")

# Verifica se o arquivo foi criado e lê o conteúdo
try:
    with open("directory_structure.txt", "r") as f:
        print(f.read())
except Exception as e:
    print(f"An error occurred while reading the txt file: {e}")

# Gere e imprima a estrutura do diretório
print(dir_structure.generate_structure())
