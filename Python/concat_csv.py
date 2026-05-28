# Importar bibliotecas necessárias
from xml.etree import ElementTree as Xet
import os
import csv
import pyexcel

def concat_csv(file):

    with open(file, mode='r') as file:
        planilha = csv.reader(file, delimiter=';')

        notas = []

        for row in planilha:
            if not(any(row[0] in sublist for sublist in notas)):
                notas.append([row[0], float(row[1])])
            else:
                for i, sublist in enumerate(notas):
                    if row[0] in sublist:
                        notas[i][1] += float(row[1])
                        break

    with open("planilha.csv", mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(notas)



if __name__ == "__main__":
    path = os.getcwd()
    files = os.listdir(path)
    cabecalho = ["Nota", "Valor"]
    with open("planilha.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(cabecalho)
        pass
    for filename in files:
        if filename.endswith("teste.csv"):
            concat_csv(filename)