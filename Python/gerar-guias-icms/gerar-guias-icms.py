# Script para gerar guia do ICMS-RS para multiplas empresas. Busca dados da planilha "Guias.xlsx".

# Importar bibliotecas necessárias
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import time
import pyautogui
import os
import pandas as pd

# Valide se o número possui um caractere. Será usado mais adiante para inserir um zero a mais para números com um caractere
def validar_numero(num):
    if len(str(num)) == 1:
        return True
    
# Valide a IE
def validar_ie(ie):
    if len(str(ie)) == 10:
        return str(ie)
    else:
        while len(str(ie)) < 10:
            ie = "0" + str(ie)
        return str(ie)

def gerar_guia_icms(desc, ie, dia, mes, ano, valor, empresa):

    # Gera o mês para pagamento, incrementando em um o mês da competência. Se o mês da competência for dezembro (12), declare o mês de pagamento como janeiro (1)
    if int(mes) == 12:
        mes_pagamento = 1
    else:
        mes_pagamento = int(mes) + 1

    ie = validar_ie(ie)
    
    # Valide o número de caracteres do mês de pagamento
    if validar_numero(int(mes_pagamento)):
        mes_pagamento = "0" + str(mes_pagamento)

    # Valide o dia do pagamento
    if validar_numero(dia):
        dia_str = "0" + str(dia)
    else:
        dia_str = str(dia)

    # Valide o mês da competência
    if validar_numero(mes):
        mes_str = "0" + str(mes)
    else:
        mes_str = str(mes)

    if int(mes) == 12:
        ano_str = str(int(ano) + 1)
    else:
        ano_str = str(ano)

    # Crie uma string com a data do pagamento
    data_pagamento = dia_str + "/" + mes_pagamento + "/" + ano_str

    # Inicie o driver
    driver = webdriver.Firefox()
    # Vá para página de gerar guias
    driver.get("https://www.sefaz.rs.gov.br/cobranca/arrecadacao/guiaicms")
    
    # Selecione o elemento adequado do tipo de ICMS
    Select(driver.find_element(By.ID, "TiposAgrupamentoClasArrec_Codigo")).select_by_value("1")
    Keys.TAB

    # Selecione o código correto do ICMS (221)
    Select(driver.find_element(By.ID, "ItensAgrupamentoClasArrec_Codigo")).select_by_value("3")
    Keys.TAB

    # Localize o elemento com a data de pagamento 
    data_input = WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.ID, "DataPagamento"))
    )
    # Limpe a data de pagamento, se houver valor
    data_input.clear()
    # Insira a data
    data_input.send_keys(data_pagamento + Keys.TAB)

    # Selecione o mês da competência
    Select(driver.find_element(By.ID, "Meses_Codigo")).select_by_value(str(mes))
    
    time.sleep(1)

    # Selecione o ano da competência
    Select(driver.find_element(By.ID, "Anos_Codigo")).select_by_value(ano_str)
    
    time.sleep(1)

    # Desmarque e marque novamente a opção de contribuinte cadastrado no estado
    checkbox = WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.ID, "RdbIndContribEmitInscritoNoRs2"))
        )    
    checkbox.click()
    checkbox = WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.ID, "RdbIndContribEmitInscritoNoRs1"))
        )    
    checkbox.click()

    # Preencha a IE do contribuinte
    ie_input = WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.ID, "ContribuinteEmit_InscricaoEstadual"))
    )
    ie_input.clear()
    for char in str(ie):
        ie_input.send_keys(char)
        time.sleep(0.1)

    time.sleep(1)

    # Clique no botão de avançar
    avancar = WebDriverWait(driver, 300).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-sm.btn-theme.btn-primary.col-sm-2"))
    )
    avancar.click()

    # Preencha o valoe de pagamento
    valor_pagamento = WebDriverWait(driver, 300).until(
        EC.element_to_be_clickable((By.ID, "OutrosCriterios_Valor"))
    )
    valor = str(f"{valor:.2f}").replace(".", ",")
    valor_pagamento.clear()
    for char in str(valor):
        valor_pagamento.send_keys(char)
        time.sleep(0.1)

    # Preencha a observação na primeira linha
    observacao = WebDriverWait(driver, 300).until(
        EC.element_to_be_clickable((By.ID, "OutrosCriterios_ObservacoesContribuinte_Linha1"))
    )
    observacao.clear()
    observacao.send_keys(desc)

    # Clique no botão de avançar
    avancar = WebDriverWait(driver, 300).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-sm.btn-theme.btn-primary.col-sm-2"))
    )
    avancar.click()

    # Clique no botão de download
    download_btn = WebDriverWait(driver, 300).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-sm.btn-theme.btn-primary.col-sm-3"))
    )
    download_btn.click()

    time.sleep(5)

    # Alterne para a aba com o PDF aberto
    tabs = driver.window_handles
    if len(tabs) > 1:
        driver.switch_to.window(tabs[-1])
    
    # Baixe o pdf
    download_btn = WebDriverWait(driver, 300).until(
        EC.element_to_be_clickable((By.ID, "downloadButton"))
    )
    download_btn.click()

    time.sleep(2)

    # Crie o nome do arquivo e renomeie a guia baixada
    nome_arquivo = empresa + " guia ICMS " + desc + " ref. " + mes_str + "." + str(ano)
    pyperclip.copy(nome_arquivo)
    time.sleep(1)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)

    # Feche o navegador
    driver.quit()


if __name__ == "__main__":
    # Mude o diretório para o local do script
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    # Crie um dataframe usando o modelo do excel com os dados
    df = pd.read_excel('Guias.xlsx')
    # Crie um dicionário com o dataframe
    data = df.to_dict(orient='records')

    # Aloque os valores do dicionário de cada linha para uma variável e chame a função principal uma vez por linha
    for i in data:
        desc = i.get("Observação")
        ie = i.get("IE")
        dia = i.get("Dia pagamento")
        mes = i.get("Mês Referência")
        ano = i.get("Ano referência")
        valor = i.get("Valor ICMS")
        empresa = i.get("Empresa")
        gerar_guia_icms(desc, ie, dia, mes, ano, valor, empresa)