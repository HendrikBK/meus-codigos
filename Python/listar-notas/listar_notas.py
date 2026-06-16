# Script para processar e listar em uma tabela os dados de uma ou mais notas fiscais em arquivos XML
# Recebe como argumentos o nome do arquivo mais os campos desejados como kwargs

# Importar bibliotecas necessárias
from xml.etree import ElementTree as Xet
import os
import csv
import tkinter as tk
import pyexcel
from datetime import datetime

# Crie um classe para gerar o widget das opções
class Checkbox:

    # Crie um dicionário vazio para guardar as opções desejadas
    opcoes = {}

    # Crie um instância do objeto com a root do widget, duas listas com os campos e um dicionário com o texto dos campos
    def __init__(self, root, campos_1, campos_2, dict_1):
        self.root = root        

        # Cria um checkbox para cada item dos campos possíveis da nota
        for campo in campos_1:
            # Cria um objeto BooleanVar
            self.var = tk.BooleanVar(value=True)
            # Cria um objeto de checkbox
            self.cb = tk.Checkbutton(root, text=dict_1[campo], variable=self.var)
            # Coloque a checkbox no widget
            self.cb.pack(anchor='w')
            # Aloque a variável de casa campo para um item no dicionário "opções"
            self.opcoes[campo] = self.var

        # Crie uma variável para armazenar o estado da opção "produtos"
        self.produtos_var = tk.BooleanVar(value=False)
        # Crie um botão que habilite ou desabilite as opções de produto
        self.produtos_check = tk.Checkbutton(root, text="Produtos", variable=self.produtos_var, command=self.toggle_children)
        # Coloque a checkbox no widget
        self.produtos_check.pack(anchor='w')
        # Crie um item no dicionário com a opção "produtos"
        self.opcoes["produtos"] = self.produtos_var
        
        # Crie um subelement para armazenar as opções do produto, mais à esquerda da principal
        self.child_frame = tk.Frame(root)
        self.child_frame.pack(anchor="w", padx=30)

        # Itere as opções do campo do produto
        for campo in campos_2:
            # Cria um objeto BooleanVar
            self.var = tk.BooleanVar()
            # Cria um objeto de checkbox
            self.cb = tk.Checkbutton(self.child_frame, text=dict_1[campo], variable=self.var)
            # Coloque a checkbox no widget
            self.cb.pack(anchor='w')
            # Aloque a variável de casa campo para um item no dicionário "opções"
            self.opcoes[campo] = self.var
        
        # Crie um botão para chamar a função principal de gerar a planilha
        btn = tk.Button(root, text="Submit", command=escrever_planilha)
        btn.pack()

        # Rode a função de desabilitar as opções de produto na inicialização da classe
        self.toggle_children()

    def toggle_children(self):
        if self.produtos_var.get():
            for widget in self.child_frame.winfo_children():
                try:
                    widget.config(state="normal")
                except tk.TclError:
                    pass
        else:
            for widget in self.child_frame.winfo_children():
                try:
                    widget.config(state="disabled")
                except tk.TclError:
                    pass
        
    def get_dict(self):
        return self.opcoes
        

def listar_notas(file, **kwargs):

    opcoes = kwargs

    #for key, value in opcoes.items():
    #    print(type(value.get()))

    # Processar o arquivo XML
    tree = Xet.parse(file)
    root = tree.getroot()

    # Criar um lista vazia para guardar os dados da linha
    dados = []

    linhas = []

    # Iterar os nódulos filhos
    for elem in tree.iter():
        tag_elements = elem.tag.split("}")
        
        # Remover namespaces e atributos
        elem.tag = tag_elements[1]
        elem.attrib.clear()

    # Buscar a data da nota
    if opcoes.get("data").get():
        data = root.find(".//dhEmi").text.split("T")[0]
        data_objeto = datetime.strptime(data, "%Y-%m-%d")
        data = data_objeto.strftime("%d/%m/%Y")
        dados.append(data)

    # Buscar a natureza da operação
    if opcoes.get("natOp").get():
        natOp = root.find(".//natOp").text
        dados.append(natOp)

    # Buscar informações complementares da nota
    if opcoes.get("infComp").get():
        if root.find(".//infCpl") is None:
            infComp = ""
        else:
            infComp = root.find(".//infCpl").text
        dados.append(infComp)

    # Buscar o número da nota
    if opcoes.get("numero").get():
        numero = root.find(".//nNF").text
        dados.append(numero)

    # Buscar o valor da nota
    if opcoes.get("valor").get():
        valor = root.find(".//vNF").text
        dados.append(valor)

    # Busque a nota referenciada, caso haja
    if opcoes.get("refNFe").get():
        if root.find(".//refNFe") is not None:
            valor = "'" + root.find(".//refNFe").text
        else:
            valor = ""
        dados.append(valor)

    # Busca o nome do emitente, caso haja
    if opcoes.get("emit").get():
        if root.find(".//emit/xNome") is not None:
            valor = root.find(".//emit/xNome").text
        else:
            valor = ""
        dados.append(valor)

    # Busca o documento (CPF ou CNPJ) do emitente, caso haja
    if opcoes.get("doc_emit").get():
        if root.find(".//emit/CPF") is not None:
            valor = root.find(".//emit/CPF").text
        elif root.find(".//emit/CNPJ") is not None:
            valor = "'" + root.find(".//emit/CNPJ").text
        else:
            valor= ""
        dados.append(valor)

    # Busca o nome do destinatário, caso haja
    if opcoes.get("dest").get():
        if root.find(".//dest/xNome") is not None:
            valor = root.find(".//dest/xNome").text
        else:
            valor = ""
        dados.append(valor)

    # Busca o documento do destinatário (CPF ou CNPJ), caso haja
    if opcoes.get("doc_dest").get():
        if root.find(".//dest/CPF") is not None:
            valor = root.find(".//dest/CPF").text
        elif root.find(".//dest/CNPJ") is not None:
            valor = "'" + root.find(".//dest/CNPJ").text
        else:
            valor= ""
        dados.append(valor)

    # Verifica se a opção "produtos" foi selecionada, caso sim, busca os campos selecionados
    if opcoes.get("produtos").get():
        # Cria uma lista com todos os produtos da nota
        itens = root.findall(".//det/prod")

        # Itera todos os produtos achados
        for i in itens:

            # Cria uma lista vazia com os dados de cada produto
            produtos = []

            # Busca a descrição do produto
            if opcoes.get("xProd").get():
                valor = i.find("./xProd").text
                produtos.append(valor)

            # Busca o CFOP do produto
            if opcoes.get("CFOP").get():
                valor = i.find("./CFOP").text
                produtos.append(valor)

            # Busca o NCM do produto
            if opcoes.get("NCM").get():
                valor = i.find("./NCM").text
                produtos.append(valor)

            # Busca a quantidade do produto
            if opcoes.get("qCom").get():
                valor = i.find("./qCom").text
                produtos.append(valor)
                
            # Busca o valor unitário do produto
            if opcoes.get("vUnCom").get():
                valor = i.find("./vUnCom").text
                produtos.append(valor)

            # Busca o valor do produto
            if opcoes.get("vProd").get():
                valor = i.find("./vProd").text
                produtos.append(valor)

            # Cria uma lista com os dados da nota e do produto
            linha = dados + produtos
            # Apende a linha completa em uma matriz
            linhas.append(linha)

    # Caso a opção "produtos" não tenha sido selecionada, a linha será apenas os dados da nota
    else:
        linha = dados
        linhas.append(dados)

    # Escrever os dados em uma nova linha da planilha
    with open("planilha.csv", mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        for linha in linhas:
            writer.writerow(linha)

# Executar o script
if __name__ == "__main__":

    # Obter o diretório que guarda os arquivos XML
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'XMLS')
    # Mude o diretório para onde estão os XMLS
    os.chdir(path)

    # Cria um widget para mostrar os campos desejados pelo usuário
    root = tk.Tk()
    root.title("Campos desejados:")

    # Define os campos possíveis, usando o nome dos nódulos dos arquivos XML
    campos = ["data", "natOp", "infComp", "numero", "valor", "refNFe", "emit", "doc_emit", "dest", "doc_dest"]

    # Defina como este campos aparecem na planilha e no widget
    campos_verbose = {
        "data": "Data",
        "natOp": "Natureza da Operação",
        "infComp": "Inf. Comp.",
        "numero": "Número",
        "valor": "Valor",
        "refNFe": "Chave NF referenciada",
        "emit": "Emitente",
        "doc_emit": "Documento emitente",
        "dest": "Destinário",
        "doc_dest": "Documento destinatário",
        "xProd": "Descrição do produto",
        "CFOP": "CFOP",
        "NCM": "NCM",
        "qCom": "Quantidade",
        "vUnCom": "Valor unitário",
        "vProd": "Valor do produto"
    }

    # Dados produtos
    # Os produtos estão em uma lista distinta das opções gerais para melhor gerar o código de criação das checkboxes do widget
    produtos = ["xProd", "CFOP", "NCM", "qCom", "vUnCom", "vProd"]

    # Defina uma função para chamar a função principal para cada arquivo XML
    def escrever_planilha():

        # Cria um dicionário com as opções selecionadas
        opcoes = app.get_dict()

        # Define uma lista vazia guardar os campos escolhidos
        cabecalho = []
        # Adicione os campos escolhidos na lista
        for key, value in opcoes.items():
            if key == "produtos":
                pass
            elif value.get():
                cabecalho.append(campos_verbose.get(key))
        
        # Abra a planilha e escreva o cabeçalho na primeira linha
        with open("planilha.csv", mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(cabecalho)
            pass

        # Obtenha uma lista de arquivos no diretório adequado
        files = os.listdir(path)

        # Chame a função principal para cada arquivo XML da pasta
        for filename in files:
            if filename.endswith(".xml"):
                listar_notas(filename, **opcoes)
        
        sheet = pyexcel.get_sheet(file_name="planilha.csv", delimiter=";")
        # Também salve a planilha CSV como XLSX 
        sheet.save_as("planilha.xlsx")
        # Termine o processo da interface de seleção de campos
        root.destroy()

    # Cria a instância do objeto da checkbox
    app = Checkbox(root, campos, produtos, campos_verbose)

    # Rode o widget principal
    root.mainloop()