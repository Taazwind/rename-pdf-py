import os
import subprocess
import sys

def check_python():
    """Vérifie si Python est installé."""
    try:
        subprocess.run(["python", "--version"], check=True)
    except FileNotFoundError:
        print("[ERREUR] Python n'est pas installé ou pas dans le PATH.")
        sys.exit(1)

def create_virtual_env(project_name):
    """Crée un environnement virtuel."""
    env_folder = f"{project_name}-env"
    if not os.path.exists(env_folder):
        print("[INFO] Création de l'environnement virtuel...")
        subprocess.run(["python", "-m", "venv", env_folder], check=True)
    else:
        print("[INFO] L'environnement virtuel existe déjà.")
    return env_folder

def activate_virtual_env(env_folder):
    """Active l'environnement virtuel."""
    activate_script = os.path.join(env_folder, "Scripts", "activate")
    if os.name == "nt":
        activate_script += ".bat"
    return activate_script

def install_dependencies(env_folder):
    """Installe les dépendances nécessaires."""
    print("[INFO] Installation des dépendances...")
    subprocess.run([os.path.join(env_folder, "Scripts", "pip"), "install", "--upgrade", "pip", "wheel", "setuptools"], check=True)
    subprocess.run([os.path.join(env_folder, "Scripts", "pip"), "install", "kivy", "kivymd"], check=True)

def main():
    project_name = "kivy_project"
    check_python()
    env_folder = create_virtual_env(project_name)
    install_dependencies(env_folder)
    print("[SUCCESS] Installation terminée avec succès !")
    print(f"[INFO] Pour activer l'environnement virtuel, utilisez :")
    print(f"  call {os.path.join(env_folder, 'Scripts', 'activate.bat')}")

if __name__ == "__main__":
    main()
