# Importar bibliotecas necessárias
from xml.etree import ElementTree as Xet
import os

def arrumar_cfop(file):

    Xet.register_namespace("", "http://www.portalfiscal.inf.br/nfe")

    cfop_5102 = ["CFOP5949-55","CFOP5949-88","CFOP5949-90","CFOP5949-92", "2", "5", "8","9", "10", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25","26", "27", "35", "34", "40", "44","45","51","52","57","58","59","60","62", "66","75", "76","77","78","80", "81", "84", "93","98","107", "115", "114","123", "124", "128", "129","130","136","143","144", "175", "176", "177","178","179","180","181","183","194","202","203","204", "205", "209", "9120002","9120003", "9120004", "9120006", "9120005"]

    cfop_5405 = ["1","3","4","6","28","29","30","31","32","33","36","37","38","39","41","42","46","48","49","50","53","54","55","56","61","63","64","65","66","68","69","70","71","72","73","74","79","82","83","85","86","87","88","89","90","91","92","94","95","96","97","98","99","100","101","102","103","104","105","106","108","109","110","111","112","116","117","118","119","120","121","123","125","127", "131","132","133","134","135","138","139","140","141","142","146","147","148","149","150","151","152","153","154","155","156","157","160","162","163","165","166","170","171","172","174","185","186","189","190","191","192","193","194","195","196","197","198","200", "201", "207", "208", "210", "211", "212", "213"]
    
    # Processar o arquivo XML
    tree = Xet.parse(file)
    nome_documento = file
    root = tree.getroot()

    nfe = root.find("{http://www.portalfiscal.inf.br/nfe}NFe")

    infNFE = nfe.find("{http://www.portalfiscal.inf.br/nfe}infNFe")
    
    itens = root.findall(".//{*}det/{*}prod")

    for i in itens:
        prod = i.find("{http://www.portalfiscal.inf.br/nfe}cProd").text
        prod_node = i.find("{http://www.portalfiscal.inf.br/nfe}cProd")
        prod_nome = i.find("{http://www.portalfiscal.inf.br/nfe}xProd").text
        prod_nome_node = i.find("{http://www.portalfiscal.inf.br/nfe}xProd").text
        cfop = i.find("{http://www.portalfiscal.inf.br/nfe}CFOP").text
        cfop_node = i.find("{http://www.portalfiscal.inf.br/nfe}CFOP")
        if (prod in cfop_5102 and cfop == "5405"):
            cfop_node.text = "5102"
        elif (prod in cfop_5405 and cfop == "5102"):
            cfop_node.text = "5405"
        elif ((prod in cfop_5102) and (prod in cfop_5405)):
            print("Produto duplicado: " + prod + ": " + prod_nome)
        elif (not(prod in cfop_5102) and not(prod in cfop_5405)):
            print("Produto não achado nas arrays: " + prod + ": " + prod_nome)
            

    tree.write(nome_documento, default_namespace=None)

if __name__ == "__main__":
    path = os.getcwd()
    files = os.listdir(path)
    for filename in files:
        if filename.endswith(".xml"):
            arrumar_cfop(filename)