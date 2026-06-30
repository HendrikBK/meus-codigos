from brazilfiscalreport.danfe import Danfe
from brazilfiscalreport.danfse import Danfse
from utils.limpar_arquivo import limpar_arquivo
import os

def converter_nota_pdf(xml_file):

    filename = xml_file.replace('xml', 'pdf')

    limpar_arquivo(xml_file)

    with open(xml_file, 'r', encoding='utf-8', errors='replace') as file:
        content = file.read()

    danfe = Danfe(xml=content)
    danfe.output(filename)

def converter_nfse_pdf(xml_file):

    filename = xml_file.replace('xml', 'pdf')

    limpar_arquivo(xml_file)

    with open(xml_file, 'r', encoding='utf-8', errors='replace') as file:
        content = file.read()

    danfe = Danfse(xml=content)
    danfe.output(filename)

if __name__ == '__main__':
    files = os.listdir(os.getcwd())
    for file in files:
        if file.endswith(".xml"):
            converter_nfse_pdf(file)