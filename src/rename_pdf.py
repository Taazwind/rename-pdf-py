from pdf_data import extract_pdf_data
from os import rename

def rename_pdf(url_pdf):
    # URL du fichier .pdf
    pdf_data = extract_pdf_data(url_pdf)

    # Renommer le fichier
    rename(url_pdf, "data/" + pdf_data + ".pdf")