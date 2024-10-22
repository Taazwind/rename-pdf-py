import pdfquery

def extract_pdf_data(url_pdf):
    # Lecture du .pdf
    pdf = pdfquery.PDFQuery(url_pdf, laparams={"all_texts": True})
    pdf.load()

    # Extraction des données
    pdf_lines = pdf.pq('LTTextLineHorizontal')
    lines = [t.text.strip() for t in pdf_lines]

    # Liste pour stocker les lignes
    stored_lines = []

    for line in lines:
        stored_lines.append(line)
        if "Nom :" in line:
            break
    
    stored_lines.pop(3)
    stored_lines.pop(2)

    # Convertir la liste en une chaîne de caractères
    result_string = "_".join(stored_lines)

    return result_string
