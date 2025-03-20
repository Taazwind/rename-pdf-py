import pdfquery

def extract_pdf_data(url_pdf):
    # Charger uniquement la première page pour accélérer le traitement
    pdf = pdfquery.PDFQuery(url_pdf, laparams={"all_texts": True})
    pdf.load(0)  # Charger uniquement la première page

    # Extraction des données
    pdf_lines = pdf.pq('LTTextLineHorizontal')
    lines = [t.text.strip() for t in pdf_lines]

    # Reste du traitement...
    stored_lines = []
    for line in lines:
        stored_lines.append(line)
        if "Nom :" in line:
            break

    stored_lines.pop(3)
    stored_lines.pop(2)

    result_string = "_".join(stored_lines).replace(" ", "_")
    return result_string