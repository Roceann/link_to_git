# python 3.12.3

# problème gestion nom des fichier (le nom du dépot se met au dubut du nom du fichier)
# problème création des dossier (les dossier ne sont pas créer)

import os
from github import Github, GithubException

# initialisation des variables à vérifé avant de lancer le script
token = ""
nom_repo = "patrouil/bia_boond_kpi"
chemin_initiale = r"C:\Users\RaphaelMALET\OneDrive - BIA GROUPE\Documents\test envoie vers git"
chemin_depot = input("chemin dans le dépot pour vous fichiers (exemple : src/bond/), ne rien mettre pour la racine : ")


# Fonction pour publier un fichier sur le dépôt
def publier(contenu, chemin_fichier):
    # Création du message de commit possibilité de le modifier
    commit_message = "Ajout de " + contenu

    # Connexion au dépôt
    g = Github(token)
    repo = g.get_repo(nom_repo)

    # Lire le contenu du fichier local et le stocker dans une variable
    with open(chemin_fichier, "r", encoding="utf-8") as file:
        content = file.read()

    # Créer le chemin du fichier sur le dépôt
    # la methode replace est utile uniquement si le code est utilisé sur windows
    nom_final = os.path.relpath(chemin_fichier, chemin_initiale).replace("\\", "/")

    try:
        contenu_fichier = repo.get_contents(nom_final)

        # Si le fichier existe, le supprimer
        repo.delete_file(nom_final, "Suppression de l'ancien fichier", contenu_fichier.sha)
    except GithubException:
        pass

    # Créer le fichier sur le dépôt
    repo.create_file(nom_final, commit_message, content)

    print(f"Le fichier {nom_final} a été publié avec succès !")


# Fonction pour parcourir les fichiers et les dossiers
def parcourir(chemin_fichier):
    # parcourir les fichiers et les dossiers dans le chemin
    for contenu in os.listdir(chemin_fichier):

        # on ajoute au chemain le dossier dans lequel on se trouve
        chemin_complet = os.path.join(chemin_fichier, contenu)

        # Si le contenu est un fichier, le publier
        if os.path.isfile(chemin_complet):
            publier(contenu, chemin_complet)

        else:
            # Si le contenu est un dossier, parcourir le dossier
            parcourir(chemin_complet)


parcourir(chemin_initiale)
print("Fin du script")
