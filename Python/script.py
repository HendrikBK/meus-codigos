# Importar bibliotecas necessárias
import pandas as pd
from xml.etree import ElementTree as Xet
import os
import sys
import subprocess
import pyexcel

def tipo_nota(file):

    # Processar o arquivo XML
    tree = Xet.parse(file)
    root = tree.getroot()

    # Iterar os nódulos filhos
    for elem in tree.iter():
        tag_elements = elem.tag.split("}")
        
        # Remover namespaces e atributos
        elem.tag = tag_elements[1]
        elem.attrib.clear()


    tipo = root.find(".//ide/mod").text
    if (tipo == "65"):
        xml_para_csv_nfce(file)
    else:
        xml_para_csv(file)


def xml_para_csv_nfce(file):
    
    nome_arquivo = file.replace(".xml", "") # Será utilizado para nomear o arquivo CSV no final

    # Processar o arquivo XML
    tree = Xet.parse(file)
    root = tree.getroot()

    # Iterar os nódulos filhos
    for elem in tree.iter():
        tag_elements = elem.tag.split("}")
        
        # Remover namespaces e atributos
        elem.tag = tag_elements[1]
        elem.attrib.clear()

    itens = root.findall(".//det")

    cols = ["cProd", "xProd", "CFOP"]
    rows = []

    for i in itens:
        for j in i.findall("./prod"):
            cProd = "=\"" + j.find("cProd").text + "\""
            xProd = j.find("xProd").text
            cfop = "=\"" + j.find("CFOP").text + "=\""

        rows.append({
                "cProd": cProd,
                "xProd": xProd,
                "CFOP": cfop})
        
        #print(pDif[0])

    df = pd.DataFrame(rows, columns=cols)

    # Escrever o arquivo csv
    df.index = pd.RangeIndex(1, len(df.index) + 1) # Definir que o índice comece com '1'

    df.to_csv(nome_arquivo + '.csv', sep=';') # Definir que ';' seja o separador ao invés de ','

def xml_para_csv(file):

    nome_arquivo = file.replace(".xml", "") # Será utilizado para nomear o arquivo CSV no final

    # Processar o arquivo XML
    tree = Xet.parse(file)
    root = tree.getroot()

    # Iterar os nódulos filhos
    for elem in tree.iter():
        tag_elements = elem.tag.split("}")
        
        # Remover namespaces e atributos
        elem.tag = tag_elements[1]
        elem.attrib.clear()

    itens = root.findall(".//det")

    cols = ["cProd", "cEAN", "xProd", "NCM", "CFOP", "uCom", "qCom", "vUnCom", "vProd", "cEANTrib", "uTrib", "qTrib", "vUnTrib", "indTot", "orig", "CST", "modBC", "pRedBC", "vBC", "pICMS", "vICMS", "pDif", "vICMSDif", "CSTIPI", "vBCIPI", "pIPI", "vIPI", "CSTPIS", "vBCPIS", "pPIS", "vPIS", "CSTCOFINS", "vBCCOFINS", "pCOFINS", "vCOFINS"]
    rows = []

    for k in itens:
        for i in k.findall("./prod"):
            cProd = "=\"" + i.find("cProd").text + "\""
            cEAN = "=\"" + i.find("cEAN").text + "\""
            xProd = i.find("xProd").text
            ncm = i.find("NCM").text
            cfop = i.find("CFOP").text
            uCom = i.find("uCom").text
            qCom = i.find("qCom").text
            vUnCom = i.find("vUnCom").text
            vProd = i.find("vProd").text
            cEANTrib = "=\"" + i.find("cEANTrib").text + "\""
            uTrib = i.find("uTrib").text
            qTrib = i.find("qTrib").text
            vUnTrib = i.find("vUnTrib").text
            indTot = i.find("indTot").text

            # Realizar teste lógico para verificar se há ou não substituição tributária no ICMS
            
            if (k.find(".//ICMS/ICMS51")): 

                for i in k.findall(".//ICMS/*"):
                    orig = i.find("orig").text,
                    cst = "=\"" + i.find("CST").text + "\"",
                    modBC = i.find("modBC").text,
                    pRedBC = i.find("pRedBC").text,
                    vBC = i.find("vBC").text,
                    pICMS = i.find("pICMS").text,
                    vICMS = i.find("vICMS").text,
                    pDif = i.find("pDif").text,
                    vICMSDif = i.find("vICMSDif").text
            else:

                for i in k.findall(".//ICMS/*"):
                    orig = i.find("orig").text,
                    cst = i.find("CST").text if (i.find("CST") is not None) else "",
                    modBC = i.find("modBC").text if i.find("modBC") is not None else "",
                    pRedBC = "",
                    vBC = i.find("vBC").text if i.find("vBC") is not None else "",
                    pICMS = i.find("pICMS").text if i.find("pICMS") is not None else "",
                    vICMS = i.find("vICMS").text if i.find("vICMS") is not None else "",
                    pDif = "",
                    vICMSDif = ""

                    if (k.find(".//IPITrib")):

                        for i in k.findall(".//IPITrib"):
                            cstipi = i.find("CST").text,
                            vBCIPI = i.find("vBC").text,
                            pIPI = i.find("pIPI").text,
                            vIPI = i.find("vIPI").text
                            
                    else:

                        for i in k.findall(".//IPINT"):
                            cstipi = i.find("CST").text,
                            vBCIPI = "",
                            pIPI = "",
                            vIPI = ""

        for i in k.findall(".//PISAliq"):
            cstpis = i.find("CST").text if i.find("CST") is not None else "",
            vbcpis = i.find("vBC").text,
            ppis = i.find("pPIS").text,
            vpis = i.find("vPIS").text

        for i in k.findall(".//COFINSAliq"):
            cstcofins = "=\"" + i.find("CST").text + "\"",
            vbccofins = i.find("vBC").text,
            pcofins = i.find("pCOFINS").text,
            vcofins = i.find("vCOFINS").text

        rows.append({
            "cProd": cProd,
            "cEAN": cEAN,
            "xProd":  xProd,
            "NCM":  ncm,
            "CFOP":  cfop,
            "uCom":  uCom,
            "qCom":  qCom,
            "vUnCom":  vUnCom,
            "vProd":  vProd,
            "cEANTrib":  cEANTrib,
            "uTrib":  uTrib,
            "qTrib":  qTrib,
            "vUnTrib":  vUnTrib,
            "indTot":  indTot,
            "orig": orig[0],
            "CST": cst[0],
            "modBC": modBC[0],
            "pRedBC": pRedBC[0],
            "vBC": vBC[0],
            "pICMS": pICMS[0],
            "vICMS": vICMS[0],
            "pDif":  pDif[0],
            "vICMSDif": vICMSDif,
            "CSTIPI": cstipi[0],
            "vBCIPI": vBCIPI[0],
            "pIPI": pIPI[0],
            "vIPI": vIPI,
            "CSTPIS": cstpis[0],
            "vBCPIS": vbcpis[0],
            "pPIS": ppis[0],
            "vPIS": vpis,
            "CSTCOFINS": cstcofins[0],
            "vBCCOFINS": vbccofins[0],
            "pCOFINS": pcofins[0],
            "vCOFINS": vcofins})
        
        # Algumas variáveis então sendo interpretadas como tuple, verificar o motivo
        
    #print(pDif[0])

    df = pd.DataFrame(rows, columns=cols)

    # Escrever o arquivo csv
    df.index = pd.RangeIndex(1, len(df.index) + 1) # Definir que o índice comece com '1'

    df.to_csv(nome_arquivo + '.csv', sep=';') # Definir que ';' seja o separador ao invés de ','

if __name__ == "__main__":
    path = os.getcwd()
    files = os.listdir(path)
    for filename in files:
        if filename.endswith(".xml"):
            tipo_nota(filename)
            sheet = pyexcel.get_sheet(file_name=filename, delimiter=";")
            sheet.save_as(filename + ".xlsx")