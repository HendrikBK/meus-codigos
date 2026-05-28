# Importar bibliotecas necessárias
from xml.etree import ElementTree as Xet
import os
import csv
import pyexcel
import tkinter as tk
from tkinter import ttk

def listar_notas(file, **kwargs):

    # Processar o arquivo XML
    tree = Xet.parse(file)
    root = tree.getroot()

    dados = []

    # Iterar os nódulos filhos
    for elem in tree.iter():
        tag_elements = elem.tag.split("}")
        
        # Remover namespaces e atributos
        elem.tag = tag_elements[1]
        elem.attrib.clear()

    if kwargs.get("natOp"):
        natOp = root.find(".//natOp").text
        dados.append(natOp)

    if kwargs.get("data"):
        data = root.find(".//dhEmi").text.split("T")[0]
        dados.append(data)

    if kwargs.get("infComp"):
        if root.find(".//infCpl") is None:
            infComp = ""
        else:
            infComp = root.find(".//infCpl").text
        dados.append(infComp)

    if kwargs.get("numero"):
        numero = root.find(".//nNF").text
        dados.append(numero)

    if kwargs.get("valor"):
        valor = root.find(".//vNF").text
        dados.append(valor)

    with open("planilha.csv", mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(dados)



if __name__ == "__main__":
    path = os.path.join(os.getcwd(), 'Python/XMLS')
    os.chdir(path)

    root = tk.Tk()

    campos = ["data", "natOP", "infComp", "numero", "valor"]
    campos_verbose = {
        "data": "Data",
        "natOP": "Natureza da Operação",
        "infComp": "Inf. Comp.",
        "numero": "Número",
        "valor": "Valor"
    }
    opcoes = {}

    def escrever_planilha():
        cabecalho = []
        for key, value in opcoes.items():
            if value.get():
                cabecalho.append(campos_verbose.get(key))
        
        with open("planilha.csv", mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(cabecalho)
            pass

        files = os.listdir(path)
        for filename in files:
            if filename.endswith(".xml"):
                listar_notas(filename, **opcoes)
        sheet = pyexcel.get_sheet(file_name="planilha.csv", delimiter=";")
        sheet.save_as("planilha.xlsx")
        root.destroy()

    for campo in campos:
        var = tk.BooleanVar()
        cb = tk.Checkbutton(root, text=campos_verbose[campo], variable=var)
        cb.pack(anchor='w')
        opcoes[campo] = var

    btn = tk.Button(root, text="Submit", command=escrever_planilha)
    btn.pack()

    root.mainloop()