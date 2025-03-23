import re
import fitz  # PyMuPDF

def extract_pdf_data(file_path):
    """Extraction du Nom et Prénom pour renommer le fichier PDF."""
    doc = fitz.open(file_path)
    text = doc[0].get_text("text")
    doc.close()

    nom_match = re.search(r"Nom\s*:\s*(.+)", text)
    prenom_match = re.search(r"Prénom\s*:\s*(.+)", text)

    # Récupérer les valeurs trouvées ou mettre un texte par défaut
    nom = nom_match.group(1).strip() if nom_match else "Nom_Inconnu"
    prenom = prenom_match.group(1).strip() if prenom_match else "Prénom_Inconnu"

    result_string = f"{nom}_{prenom}"

    # Supprimer les caractères interdits pour un nom de fichier valide
    result_string = re.sub(r'[\/\\:*?"<>|]', '_', result_string)

    return result_string
