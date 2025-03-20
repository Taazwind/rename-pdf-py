# Rename PDF Application

Cette application permet d'extraire des données spécifiques de fichiers PDF dans un dossier et de renommer automatiquement chaque fichier en fonction des données extraites.

---

## Fonctionnalités

1. **Sélection de dossier** :
   - Cliquez sur le bouton **"Naviguer"** pour sélectionner un dossier contenant des fichiers PDF.

2. **Extraction et renommage** :
   - Cliquez sur le bouton **"Renommer les PDFs"** pour extraire les données de chaque fichier PDF et les renommer automatiquement.

3. **Messages d'état** :
   - Un message de succès s'affiche avec les nouveaux noms des fichiers.
   - En cas de problème, un message d'erreur s'affiche.

4. **Quitter l'application** :
   - Cliquez sur le bouton **"Quitter"** pour fermer l'application.

---

## Installation

### Prérequis
- **Python 3.8 ou supérieur** doit être installé sur votre machine.
- Les dépendances nécessaires sont listées dans le fichier `requirements.txt`.

### Étapes d'installation
1. Clonez ce dépôt ou téléchargez les fichiers :
   ```bash
   git clone <url_du_dépôt>
   cd rename-pdf-py

2. Créez un environnement virtuel (recommandé): 
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Sur Windows
   source .venv/bin/activate  # Sur macOS/Linux

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt

4. Lancez l'application :
   ```bash
   python main.py

---

## Utilisation

1. Lancer l'application :
   Exécutez le fichier main.py ou utilisez l'exécutable généré (voir section "Création d'un exécutable").

2. Naviguer vers un dossier :
   Cliquez sur le bouton "Naviguer" pour sélectionner un dossier contenant des fichiers PDF.

3. Renommer les fichiers PDF :
   Cliquez sur le bouton "Renommer les PDFs" pour lancer le processus d'extraction et de renommage.

4. Quitter l'application :
   Cliquez sur le bouton "Quitter" pour fermer l'application.

---

## Dépendances

-**Kivy** : Framework pour créer des interfaces utilisateur.\n
-**KivyMD** : Extension de Kivy pour des composants Material Design.\n
-**pdfquery** : Extraction de données à partir de fichiers PDF.\n
-**PyInstaller** : Création d'exécutables pour distribuer l'application.\n

Pour voir la liste complète des dépendances, consultez le fichier requirements.txt.

---

## Problèmes connus

1. Caractères non valides dans les noms de fichiers :
   Les caractères non valides pour les systèmes de fichiers (par exemple, :, /, \) sont automatiquement remplacés par des underscores (_).

2. Problèmes avec PyInstaller :
   Si des fichiers de ressources manquent dans l'exécutable, modifiez le fichier .spec pour inclure les fichiers nécessaires.