# Importar bibliotecas necessárias
from pathlib import Path
import xml.etree.ElementTree as Xet
import os
import re

def remover_ns(file):
    with open(file, 'r', encoding="utf-8", errors="replace") as source:
         data = source.read()
    
    new_data = data.replace(' xmlns="http://www.abrasf.org.br/nfse.xsd"', '').replace(' xmlns="http://www.sped.fazenda.gov.br/nfse"', '')
    
    with open(file, 'w', encoding="utf-8") as source:               
        source.write(new_data)

def consertar_notas(file):

    tree = Xet.parse(file)
    
    root = tree.getroot()

    if root.find('.//NFSe') is not None:
        nota = root.find('.//NFSe')
    else:
        nota = root.find('.//Nfse')

    if nota is not None:
        new_tree = Xet.ElementTree(nota)
        path = os.path.join('..','Notas', file)
        new_tree.write(path, encoding='utf-8')


if __name__ == "__main__":
    dir = os.path.join(os.getcwd(), 'XMLS')
    os.chdir(dir)
    print(dir)
    files = os.listdir(dir)
    os.makedirs('../Notas', exist_ok=True)
    for filename in files:
        if filename.endswith(".xml"):
            remover_ns(filename)
    for filename in files:
        if filename.endswith(".xml"):
            consertar_notas(filename)