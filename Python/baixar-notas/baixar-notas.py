#  Importar bibliotecas necessárias
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import shutil
import zipfile
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
from utils.pad_numero import pad_num
from utils.converter_nota_pdf import converter_nota_pdf
from utils.join_pdf import join_pdfs
import tkinter as tk
from tkinter import ttk, filedialog

# Baixe as notas de uma empresa e organize os arquivos em um diretório único
def organizar_arquivos(url, nome, mes, ano, driver):
    # Baixe as notas, usando a url construída na main
    baixar_notas(url, driver)
    # Adicione um zero na frente do número do mês, caso seja de um dígito
    mes = pad_num(mes, 2)
    # Crie um diretório para a empresa selecionada
    dest_path = './' + nome
    os.makedirs(dest_path, exist_ok=True)
    # Liste os arquivos na pasta downloads
    files = os.listdir()
    # Itere sobre todos os arquivos. Planilhas devem ser renomeadas e movidas, zips de vem ser movidos, descompactados e apagados
    for file in files:

        if file.endswith(".xlsx"):
            # Crie um nove nome para a planilha, usando os parêmtros fornecidos
            new_file_name = nome + " " + mes + "." + ano + ".xlsx"
            # Renomeie a planilha
            os.rename(file, new_file_name)
            # Mova a planilha
            shutil.move(new_file_name, dest_path)
        elif file.endswith(".zip"):
            # Mova o zip
            shutil.move(file, dest_path)
            # Mude o diretório para a pasta de destino das notas
            os.chdir(dest_path)
            # Descompacte o zip
            with zipfile.ZipFile(file, 'r') as zip_ref:
                zip_ref.extractall()
            # Apague o zip
            os.remove(file)
            # Retorne ao diretório principal
            os.chdir('..')
    # Mude o diretório para a pasta de destino das notas
    os.chdir(dest_path)
    # Liste os arquivos na pasta
    xml_files = os.listdir()
    # Itere sobre todos os arquivos
    for xml_file in xml_files:
        # Caso o arquivo seja um xml, converta para pdf e apague o xml
        if xml_file.endswith(".xml"):
            converter_nota_pdf(xml_file)
            os.remove(xml_file)
    # Crie um pdf com os demais pdfs
    join_pdfs(nome + " " + mes + "." + ano)

# Função para baixar notas 
def baixar_notas(url, driver):
    # Force o navegador a acessar outra página para evitar erros com o SIEG
    driver.get("https://www.google.com")
    # Navegue até a página do SIEG
    driver.get(url)
    # Tente acessar o site do SIEG
    try:
        # Tente localizar o elemento para selecionar todas as notas
        checkbox = WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.ID, "lblSelectAll"))
        )
        # Caso o checkbox não esteja selecionado, selecione
        if not checkbox.is_selected():
            checkbox.click()
        # Busque e clique o botão de download de planilha do Excel
        download_btn = WebDriverWait(driver, 300).until(
            EC.element_to_be_clickable((By.ID, "MainContent_cphMainContent_ListXmlFile_ExcelLinkBtn"))
        )
        download_btn.click()
        # Clique no botão de download para gerar o modal
        driver.find_element(By.CSS_SELECTOR, ".btn.btn-success.float-right.margin-top").click()
        # Procure e clique no botão de download que apareceu no modal, para baixar os xmls
        download_btn = WebDriverWait(driver, 300).until(
            EC.element_to_be_clickable((By.ID, "MainContent_cphMainContent_DownloadXml_btnDownloadSelected"))
        )
        download_btn.click()
        # Procure e clique no botão de fechar o modal
        close_btn = download_btn = WebDriverWait(driver, 300).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".close"))
        )
        close_btn.click()
    # Caso não seja possível abrir o site, retorne um erro
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":

    # Listar as empresas cujas notas devem ser baixadas
    empresas = {
        "AGM": "31052550000269",
        "AAM": "32071287000137",
        "BMM": "38138373000104",
        "MHR": "12281561000195",
        "EFP": "52449407000102",
        "ERO": "43290340000107",
        "DR": "49938005000159",
        "Gasparetto": "50116836000124",
        "VCA": "36277100000107",
        "VPF": "36311404000143",
        "Cleidy": "59117186000106",
        "Frz": "63786592000139"
    }

    # Definir uma função para obter os dados fornecidos e baixas as notas
    def main_script():
        # Obter o mês da competência
        mes = combo_meses.get()
        # Obter o ano da competência
        ano = combo_anos.get()
        # Obter o diretório para downloads
        path = path_entry.get()
        # Destruir a janela da interface
        root.destroy()
        # Iniciar o driver
        driver = webdriver.Firefox()
        # Obter um url e rodas a função de organizar arquivos para cada item do dicionário
        for key, value in empresas.items():
            # Mudar o diretório para o escolhido
            os.chdir(path)
            # Montar a url de casa empresa
            url = "https://cofre.sieg.com/lista-xml?cnpjdes=" + value + "&year=" + ano + "&month=" + mes + "&ordertype=4"
            # Executar a função para baixar e organizar arquivos
            organizar_arquivos(url, key, mes, ano, driver)
        
    # Navegar entre diretórios para escolher o desejado
    def browse_path():
        selected_path = filedialog.askdirectory(
            initialdir=r"C:\Users\Conape03\Downloads"
        )
        if selected_path:
            path_variable.set(selected_path)

    # Criar uma lista com 12 meses
    meses = [i for i in range(1,13)]
    # Criar uma lista com anos de 2026 a 2031
    anos = [i for i in range(2026, 2032)]

    # Cria um widget para mostrar os campos desejados pelo usuário
    root = tk.Tk()
    root.title("Valores")
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
    # Criar o widget do mês
    meses_label = ttk.Label(root, text="Mês competência")
    meses_label.pack(pady=5)
    combo_meses = ttk.Combobox(root, values=meses, state="readonly")
    combo_meses.pack(padx=10)
    # Criar o widget do ano
    anos_label = ttk.Label(root, text="Ano")
    anos_label.pack(pady=5)
    combo_anos = ttk.Combobox(root, values=anos, state="readonly")
    combo_anos.pack(padx=10)
    # Criar o botão para obter os dados fornecidos e rodão a função
    btn = tk.Button(root, text="Confirmar", command=main_script)
    btn.pack(padx=10, pady=10)
    # Iniciar o widget
    root.mainloop()