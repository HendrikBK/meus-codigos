# Importar bibliotecas necessárias
import pandas as pd
from xml.etree import ElementTree as Xet
import os
import csv

def nota(file):

    # Processar o arquivo XML
    tree = Xet.parse(file)
    root = tree.getroot()



    # Iterar os nódulos filhos
    for elem in tree.iter():
        tag_elements = elem.tag.split("}")
        
        # Remover namespaces e atributos
        elem.tag = tag_elements[1]
        #elem.attrib.clear()

    versao = root.find(".//NFSe").get('versao')
    print(versao)

    data = root.find(".//dCompet").text
    numero = root.find(".//infNFSe/nNFSe").text
    descricao = root.find(".//xDescServ").text
    valor = root.find(".//vServ").text
    if root.find(".//tribISSQN").text == '1':
        iss = root.find(".//vISSQN").text
    else:
        iss = 0

    dados = [data, numero, descricao, valor, iss]

    with open("planilha.csv", mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(dados)



if __name__ == "__main__":
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'XMLS')
    os.chdir(path)
    files = os.listdir(path)
    cabecalho = ["Data", "Número", "Descrição", "Valor", "ISS"]
    with open("planilha.csv", mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(cabecalho)
        pass
    for filename in files:
        if filename.endswith(".xml"):
            nota(filename)
    sheet = pd.read_csv("planilha.csv", encoding="cp1252", delimiter=";")
    sheet.to_excel("planilha.xlsx", index=False)