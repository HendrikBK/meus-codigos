# Script para retirar o caractere \x90 de arquivos
# Importar bibliotecas necessárias
import re

# Definir a função principal
def limpar_arquivo(file):
    # Abrir o arquivo e ler seu conteúdo
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        data = f.read()
    # Salvar o conteúdo em uma nova variável e substituir o caractere inválido
    new_data = re.sub(r'\x90', "", data)
    # Sobreescrver o arquivo
    with open(file, 'w', encoding="utf-8") as f:
        f.write(new_data)