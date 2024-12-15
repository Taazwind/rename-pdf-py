"""
Cette application permet d'extraire des données d'un fichier PDF et de renommer le fichier en utilisant les données extraites.

Fonctionnement de l'application :
1. Cliquez sur le bouton "Browse" pour sélectionner un fichier PDF.
2. Le chemin du fichier sélectionné sera affiché dans le champ de texte.
3. Cliquez sur le bouton "Extract Data and Rename PDF" pour extraire les données du fichier PDF et le renommer.
4. Un message de succès s'affichera avec le nouveau nom du fichier, ou un message d'erreur s'affichera en cas de problème.
5. Cliquez sur le bouton "Quit" pour fermer l'application.
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
from os import rename

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
            text: "Cette application permet d'extraire des données d'un fichier PDF et de renommer le fichier en utilisant les données extraites.\\n\\nFonctionnement de l'application :\\n1. Cliquez sur le bouton 'Naviguer' pour sélectionner un fichier PDF.\\n2. Le chemin du fichier sélectionné sera affiché dans le champ de texte.\\n3. Cliquez sur le bouton 'Extraire et renommer le PDF' pour extraire les données du fichier PDF et le renommer.\\n4. Un message de succès s'affichera avec le nouveau nom du fichier, ou un message d'erreur s'affichera en cas de problème.\\n5. Cliquez sur le bouton 'Quitter' pour fermer l'application."
            halign: "left"
            size_hint_y: None
            height: self.texture_size[1]

        MDTextField:
            id: file_path
            hint_text: "Lien vers le PDF"
            readonly: True

        MDRaisedButton:
            text: "Naviguer"
            on_release: app.file_manager_open()

        MDRaisedButton:
            text: "Extraire et renommer le PDF"
            on_release: app.extract_and_rename()

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
        )
        self.selected_file_path = None
        return Builder.load_string(KV)

    def file_manager_open(self):
        # Lien de base pour la navigation
        self.file_manager.show('/')  

    def select_path(self, path):
        self.root.get_screen('main').ids.file_path.text = path
        self.selected_file_path = path
        self.exit_manager()

    def exit_manager(self, *args):
        self.file_manager.close()

    def extract_and_rename(self):
        if not self.selected_file_path:
            self.show_dialog("Erreur", "Veuillez sélectionner un fichier PDF")
            return

        try:
            # Extraire les données du fichier PDF
            pdf_data = extract_pdf_data(self.selected_file_path)
            
            # Remplacer les espaces par des underscores
            pdf_data = pdf_data.replace(" ", "_")
            
            # Renommer le fichier PDF
            new_file_path = "data/" + pdf_data + ".pdf"
            rename(self.selected_file_path, new_file_path)
            
            self.show_dialog("Succès", f"Fichier renommé en: {new_file_path}")
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