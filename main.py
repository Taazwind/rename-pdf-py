"""
Cette application permet d'extraire des données de tous les fichiers PDF dans un dossier et de renommer chaque fichier en utilisant les données extraites.

Fonctionnement de l'application :
1. Cliquez sur le bouton "Naviguer" pour sélectionner un dossier contenant des fichiers PDF.
2. Le chemin du dossier sélectionné sera affiché dans le champ de texte.
3. Cliquez sur le bouton "Extraire et renommer les PDFs" pour extraire les données de chaque fichier PDF et les renommer.
4. Un message de succès s'affichera avec les nouveaux noms des fichiers, ou un message d'erreur s'affichera en cas de problème.
5. Cliquez sur le bouton "Quitter" pour fermer l'application.
"""

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from src.pdf_data import extract_pdf_data
from os import rename, listdir
from os.path import isfile, join
import threading
from concurrent.futures import ThreadPoolExecutor
import os
import subprocess
import sys

def install_dependencies():
    """Installer les dépendances à partir de requirements.txt si nécessaire."""
    try:
        # Vérifier si les dépendances sont installées
        import kivy
        import kivymd
        import pdfquery
    except ImportError:
        print("Installation des dépendances...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

# Appeler la fonction pour installer les dépendances
install_dependencies()

KV = '''
ScreenManager:
    MainScreen:

<MainScreen>:
    name: 'main'
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)

        MDLabel:
            text: "Cette application permet d'extraire des données de tous les fichiers PDF dans un dossier et de renommer chaque fichier en utilisant les données extraites.\\n\\n\\nFonctionnement de l'application :\\n\\n1. Cliquez sur le bouton 'Naviguer' pour sélectionner un dossier contenant des fichiers PDF.\\n\\n2. Le chemin du dossier sélectionné sera affiché dans le champ de texte.\\n\\n3. Cliquez sur le bouton 'Renommer les PDFs' pour extraire les données de chaque fichier PDF et les renommer.\\n\\n4. Un message de succès s'affichera avec les nouveaux noms des fichiers, ou un message d'erreur s'affichera en cas de problème.\\n\\n5. Cliquez sur le bouton 'Quitter' pour fermer l'application."
            halign: "left"
            size_hint_y: None
            height: self.texture_size[1]

        MDBoxLayout:
            orientation: 'horizontal'
            spacing: dp(10)

            MDTextField:
                id: folder_path
                hint_text: "Lien vers le dossier"
                readonly: True

            MDRaisedButton:
                text: "Naviguer"
                on_release: app.file_manager_open()

        MDRaisedButton:
            text: "Renommer les PDFs"
            on_release: app.extract_and_rename_all()

        MDRaisedButton:
            text: "Quitter"
            on_release: app.quit_app()
'''

class MainScreen(Screen):
    pass

class RenommagePDFApp(MDApp):
    def build(self):
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=False
        )
        self.selected_folder_path = None
        self.loading_dialog = None
        return Builder.load_string(KV)


    def file_manager_open(self):
        # Ouvrir le gestionnaire de fichiers pour sélectionner un dossier
        self.file_manager.show('/Users/tzvetan/')  

    def select_path(self, path):
        # Mettre à jour le chemin du dossier sélectionné dans le champ de texte
        self.root.get_screen('main').ids.folder_path.text = path
        self.selected_folder_path = path
        self.exit_manager()

    def exit_manager(self, *args):
        self.file_manager.close()
    
    def extract_and_rename_all(self):
        if not self.selected_folder_path:
            self.show_dialog("Erreur", "Veuillez sélectionner un dossier")
            return

        # Afficher un message "Extraction en cours..."
        self.loading_dialog = MDDialog(
            title="Veuillez patienter",
            text="Renommage des fichiers en cours...",
        )
        self.loading_dialog.open()

        # Exécuter l'extraction dans un thread séparé
        threading.Thread(target=self._extract_and_rename_all_thread).start()


    def _extract_and_rename_all_thread(self):
        try:
            files = [f for f in listdir(self.selected_folder_path) if f.endswith(".pdf")]

            # Utiliser un ThreadPoolExecutor pour traiter les fichiers en parallèle
            with ThreadPoolExecutor() as executor:
                futures = []
                for filename in files:
                    file_path = join(self.selected_folder_path, filename)
                    futures.append(executor.submit(self._process_file, file_path))

                # Attendre que tous les fichiers soient traités
                for future in futures:
                    future.result()

            # Planifier l'affichage du message de succès sur le thread principal
            Clock.schedule_once(lambda dt: self._on_extraction_complete("Succès", "Tous les fichiers PDF ont été renommés avec succès"))
        except Exception as e:
            # Planifier l'affichage du message d'erreur sur le thread principal
            Clock.schedule_once(lambda dt: self._on_extraction_complete("Erreur", str(e)))

    def _process_file(self, file_path):
        """Traiter un fichier PDF individuel."""
        with open(file_path, 'rb') as pdf_file:
            pdf_data = extract_pdf_data(pdf_file)

        # Remplacer les espaces par des underscores
        pdf_data = pdf_data.replace(" ", "_")

        # Renommer le fichier PDF
        new_file_path = join(self.selected_folder_path, pdf_data + ".pdf")
        rename(file_path, new_file_path)

    def _on_extraction_complete(self, title, message):
        # Fermer le dialog de chargement
        if self.loading_dialog:
            self.loading_dialog.dismiss()
            self.loading_dialog = None

        # Afficher le message de succès ou d'erreur
        self.show_dialog(title, message)

    def quit_app(self):
        self.stop()

    def show_dialog(self, title, text):
        # Afficher une boîte de dialogue avec un titre et un texte
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                ),
            ],
        )
        dialog.open()

if __name__ == '__main__':
    RenommagePDFApp().run()