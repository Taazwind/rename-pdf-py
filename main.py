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
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from src.pdf_data import extract_pdf_data
from os import rename, listdir
from os.path import isfile, join

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
            text: "Cette application permet d'extraire des données de tous les fichiers PDF dans un dossier et de renommer chaque fichier en utilisant les données extraites.\\n\\nFonctionnement de l'application :\\n1. Cliquez sur le bouton 'Naviguer' pour sélectionner un dossier contenant des fichiers PDF.\\n2. Le chemin du dossier sélectionné sera affiché dans le champ de texte.\\n3. Cliquez sur le bouton 'Renommer les PDFs' pour extraire les données de chaque fichier PDF et les renommer.\\n4. Un message de succès s'affichera avec les nouveaux noms des fichiers, ou un message d'erreur s'affichera en cas de problème.\\n5. Cliquez sur le bouton 'Quitter' pour fermer l'application."
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
        return Builder.load_string(KV)

    def file_manager_open(self):
        # Ouvrir le gestionnaire de fichiers pour sélectionner un dossier
        self.file_manager.show('/')  

    def select_path(self, path):
        self.root.get_screen('main').ids.folder_path.text = path
        self.selected_folder_path = path
        self.exit_manager()

    def exit_manager(self, *args):
        self.file_manager.close()

    def extract_and_rename_all(self):
        if not self.selected_folder_path:
            self.show_dialog("Erreur", "Veuillez sélectionner un dossier")
            return

        try:
            # Parcourir tous les fichiers PDF dans le dossier sélectionné
            for filename in listdir(self.selected_folder_path):
                if filename.endswith(".pdf"):
                    file_path = join(self.selected_folder_path, filename)
                    
                    # Extraire les données du fichier PDF
                    pdf_data = extract_pdf_data(file_path)
                    
                    # Remplacer les espaces par des underscores
                    pdf_data = pdf_data.replace(" ", "_")
                    
                    # Renommer le fichier PDF
                    new_file_path = join(self.selected_folder_path, pdf_data + ".pdf")
                    rename(file_path, new_file_path)
            
            self.show_dialog("Succès", "Tous les fichiers PDF ont été renommés avec succès")
        except Exception as e:
            self.show_dialog("Erreur", str(e))

    def quit_app(self):
        self.stop()

    def show_dialog(self, title, text):
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