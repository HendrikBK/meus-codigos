# Importar bibliotecas necessárias
import pandas as pd
from xml.etree import ElementTree as Xet
import os
import csv
import pyexcel

def nota(file):

    # Processar o arquivo XML
    tree = Xet.parse(file)
    root = tree.getroot()

    # Iterar os nódulos filhos
    for elem in tree.iter():
        tag_elements = elem.tag.split("}")
        
        # Remover namespaces e atributos
        elem.tag = tag_elements[1]
        elem.attrib.clear()

    numero = root.find(".//InfNfse/Numero").text
    data = root.find(".//Competencia").text
    descricao = root.find(".//Discriminacao").text
    valor = root.find(".//ValorServicos").text
    if root.find(".//Servico/IssRetido").text == '1':
        iss = root.find(".//ValorIss").text
    else:
        iss = 0

    dados = [numero, data, descricao, valor, iss]

    with open("planilha.csv", mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(dados)



if __name__ == "__main__":
    path = os.getcwd()
    with open("planilha.csv", mode='w', newline='') as file:
        pass
    files = os.listdir(path)
    for filename in files:
        if filename.endswith(".xml"):
            nota(filename)
    sheet = pyexcel.get_sheet(file_name="planilha.csv", delimiter=";")
    sheet.save_as("planilha.xlsx")