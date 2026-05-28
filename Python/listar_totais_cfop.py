# Importar bibliotecas necessárias
from xml.etree import ElementTree as Xet
import os
import csv
import pyexcel

def arrumar_cfop(file):

    Xet.register_namespace("", "http://www.portalfiscal.inf.br/nfe")
    
    # Processar o arquivo XML
    tree = Xet.parse(file)
    root = tree.getroot()

    nfe = root.find("{http://www.portalfiscal.inf.br/nfe}NFe")

    no_nfe = root.find(".//{*}nNF").text
    
    itens = root.findall(".//{*}det/{*}prod")

    cfop_5102 = 0

    cfop_5152 = 0

    for i in itens:
        cfop = i.find("{http://www.portalfiscal.inf.br/nfe}CFOP").text
        valor = i.find("{http://www.portalfiscal.inf.br/nfe}vProd").text
        if cfop == '5102':
            cfop_5102 = cfop_5102 + float(valor)
        elif cfop == '5152':
            cfop_5152 = cfop_5152 + float(valor)

    dados = [no_nfe,str(cfop_5102), str(cfop_5152)]
            
    with open("planilha.csv", mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(dados)

if __name__ == "__main__":
    path = os.getcwd()
    files = os.listdir(path)
    cabecalho = ["Nota", "5102", "5152"]
    with open("planilha.csv", mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(cabecalho)
        pass
    for filename in files:
        if filename.endswith(".xml"):
            arrumar_cfop(filename)
    sheet = pyexcel.get_sheet(file_name="planilha.csv", delimiter=";")
    sheet.save_as("planilha.xlsx")