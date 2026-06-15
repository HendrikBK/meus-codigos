from brazilfiscalreport.danfe import Danfe
import os
import sys
import chardet
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
from consertar_notas import limpar_arquivo

def converter_nota_pdf(xml_file):

    filename = xml_file.replace('xml', 'pdf')

    limpar_arquivo(xml_file)

    with open(xml_file, 'r', encoding='utf-8', errors='replace') as file:
        content = file.read()

    danfe = Danfe(xml=content)
    danfe.output(filename)

if __name__ == "__main__":
    converter_nota_pdf("43260524660863000153550020000038921000064184.xml")