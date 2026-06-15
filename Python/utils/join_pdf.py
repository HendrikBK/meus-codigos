from pypdf import PdfWriter
import os

def join_pdfs(nome):
    files = os.listdir()
    pdfs = []
    for file in files:
        if file.endswith(".pdf"):
            pdfs.append(file)
    merger = PdfWriter()
    if len(pdfs) > 1:
        for pdf in pdfs:
            merger.append(pdf)
    else:
        pass

    merger.write(nome + ".pdf")
    merger.close()
    