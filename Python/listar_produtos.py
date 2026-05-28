# Importar bibliotecas necessárias
from xml.etree import ElementTree as Xet
import os
import csv
import pyexcel

def listar_produtos(file):

    Xet.register_namespace("", "http://www.portalfiscal.inf.br/nfe")
    
    # Processar o arquivo XML
    tree = Xet.parse(file)
    root = tree.getroot()

    nfe = root.find("{http://www.portalfiscal.inf.br/nfe}NFe")

    tipo = root.find(".//{*}mod").text

    no_nfe = root.find(".//{*}nNF").text
    
    itens = root.findall(".//{*}det/{*}prod")

    if tipo == '55':

        for i in itens:
            nome = i.find("{*}xProd").text
            cfop = i.find("{*}CFOP").text
            ncm = i.find("{*}NCM").text
            qtd = i.find("{*}qCom").text
            vlrUn = i.find("{*}vUnCom").text
            vlrTotal = i.find("{*}vProd").text
            dados = [no_nfe, nome, cfop, ncm, qtd, vlrUn, vlrTotal]
                
            with open("produtos.csv", mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(dados)

if __name__ == "__main__":
    path = os.getcwd()
    files = os.listdir(path)
    cabecalho = ["Nota", "Produto", "CFOP", "NCM" , "Quantidade", "Valor Unitário", "Valor Total"]
    with open("produtos.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(cabecalho)
        pass
    for filename in files:
        if filename.endswith(".xml"):
            listar_produtos(filename)
    sheet = pyexcel.get_sheet(file_name="produtos.csv", delimiter=";")
    sheet.save_as("produtos.xlsx")