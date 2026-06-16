# Importar bibliotecas necessárias
from xml.etree import ElementTree as Xet
import os
import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
import warnings

def arrumar_cfop(file):
    # Registrar o namespace
    Xet.register_namespace("", "http://www.portalfiscal.inf.br/nfe")
    # Buscar os aqruivos txt com as listas de produtos por cfop no diretório do script
    file_dir = Path(__file__).parent
    list_dir = os.listdir(file_dir)
    # Criar as listas de 5102 e 5405, caso houver
    if "5102.txt" in list_dir:
        text_file = file_dir / "5102.txt"
        with open(text_file, 'r', encoding="utf-8") as f:
            cfop_5102 = f.read().split(',')
    if "5405.txt" in list_dir:
        text_file = file_dir / "5405.txt"
        with open(text_file, 'r', encoding="utf-8") as f:
            cfop_5405 = f.read().split(',')
    
    # Processar o arquivo XML
    tree = Xet.parse(file)
    # Obter o nome do arquivo para sobrescrever
    nome_documento = file
    # Obter a raiz do documento
    root = tree.getroot()
    
    # Obter todos os produtos
    itens = root.findall(".//{*}det/{*}prod")
    # Iterar sobre todos os produtos
    for i in itens:
        # Obter o código do produto
        prod = i.find("{http://www.portalfiscal.inf.br/nfe}cProd").text
        # Obter o nome do produto
        prod_nome = i.find("{http://www.portalfiscal.inf.br/nfe}xProd").text
        # Obter o CFOP
        cfop = i.find("{http://www.portalfiscal.inf.br/nfe}CFOP").text
        # Obter o nódulo do CFOP
        cfop_node = i.find("{http://www.portalfiscal.inf.br/nfe}CFOP")
        # Caso o cfop seja 5405 e o produto esteja na lista de 5102, mudar os CFOP para 5102
        if (prod in cfop_5102 and cfop == "5405"):
            cfop_node.text = "5102"
        # Caso o cfop seja 5102 e o produto esteja na lista de 5405, mudar os CFOP para 5405
        elif (prod in cfop_5405 and cfop == "5102"):
            cfop_node.text = "5405"
        # Caso o produto esteja nas duas listas, mostrar isso no console e em um aviso
        elif ((prod in cfop_5102) and (prod in cfop_5405)):
            print("Produto duplicado: " + prod + ": " + prod_nome)
            warnings.warn("Produto duplicado: " + prod + ": " + prod_nome)
        # Caso o produto não esteja em nenhuma lista, mostrar isso no console e em um aviso
        elif (not(prod in cfop_5102) and not(prod in cfop_5405)):
            print("Produto não achado nas listas: " + prod + ": " + prod_nome)
            warnings.warn("Produto não achado nas listas: " + prod + ": " + prod_nome)
            
    # Reescrever o arquivo
    tree.write(nome_documento, default_namespace=None)

if __name__ == "__main__":

    def main_funtion():
        # Obter o caminho que contém os xmls
        path = path_variable.get()
        # Mudar o diretório para onde estão os xmls
        os.chdir(path)
        # Obter a lista de arquivos do diretório atual
        files = os.listdir(path)
        # Fechar o widget principal
        root.destroy()
        # Executar a função de arrumar CFOP para cada um dos arquivos xml
        for filename in files:
            if filename.endswith(".xml"):
                arrumar_cfop(filename)
    # Navegar em diretórios quando selecionado o botão ao lado do input de diretórios
    def browse_path():
        selected_path = filedialog.askdirectory(
            initialdir=r"C:\Users\Conape03\Downloads"
        )
        if selected_path:
            path_variable.set(selected_path)

    # Cria um widget para mostrar os campos desejados pelo usuário
    root = tk.Tk()
    root.title("Diretório")
    # Permitir o redimensionamento do widget
    root.resizable(True, True)

    # Criar um frame para guardar o navegador de diretórios e o botão
    path_frame = tk.Frame(root)
    path_frame.pack(fill=tk.X, padx=10)
    # Criar a variável de diretório e os elementos do widget
    path_variable = tk.StringVar(value=r"C:\Users\Conape03\Downloads")
    path_label = ttk.Label(root, text="Destino de downloads")
    path_entry = tk.Entry(path_frame, textvariable=path_variable)
    path_entry.pack(side=tk.LEFT, padx=(0,5), fill='both', expand=True)
    browse_btn = tk.Button(path_frame, text="Navegar", command=browse_path)
    browse_btn.pack(side=tk.RIGHT, padx=(5,0))
    # Criar o botão para rodar a função principal
    confirm_btn = tk.Button(root, text="Confirmar", command=main_funtion)
    confirm_btn.pack()
    root.mainloop()