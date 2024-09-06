import os
from github import Github, Auth
import requests

# Initialisation des variables
fichiers = []
deja_fait = False

# Chemin local où seront téléchargés les fichiers du dépôt à modifié avant la première utilisation du script
chemin_local = r"C:\Users\RaphaelMALET\OneDrive - BIA GROUPE\Documents\1sysd"

# Utiliser un token avec suffisamment de permissions pour accéder au dépôt
token = ""
auth = Auth.Token(token)

# Instance Github avec l'authentification
g = Github(auth=auth)

# Accéder au dépôt
repo = g.get_repo("patrouil/bia_boond_kpi")

# Test de la connexion au dépôt
print(repo.full_name)

# Récupération des commits du dépôt pour la branche main
commits = repo.get_commits(sha="main")
for commit in commits:
    commit = repo.get_commit(commit.sha)

    # Parcours des fichiers modifiés dans le commit
    for file in commit.files:

        # gestion des exceptions
        if os.path.dirname(file.filename) != "bia_boond_kpi/src/conf" and os.path.dirname(
                file.filename) != "bia_boond_kpi/src/log":

            # code pour évité les doublons, on prend la dernire mise à jour donc le premier commit qui viens à nous
            for fichier in fichiers:
                if file.filename == fichier:
                    deja_fait = True

            # si le fichier n'a pas déjà été téléchargé
            if not deja_fait:
                fichiers.append(file.filename)

                # nom du fichier (chemain du fichier + nom) et url du fichier (grace auquel on peut le télécharger)
                nom_fichier = os.path.join(chemin_local, file.filename)
                fichier_url = file.raw_url

                # si le fichier existe déjà, on le supprime
                if os.path.exists(nom_fichier):
                    os.remove(nom_fichier)
                # création du dossier si il n'existe pas
                os.makedirs(os.path.dirname(nom_fichier), exist_ok=True)

                # requête de téléchargement du fichier
                response = requests.get(fichier_url)

                # si le fichier est téléchargé avec succès, statut code 200 = ok
                if response.status_code == 200:

                    # écriture du fichier
                    with open(nom_fichier, 'wb') as f:
                        f.write(response.content)
                    print(f"Fichier téléchargé : {nom_fichier}")
                else:
                    print(f"Erreur lors du téléchargement du fichier : {nom_fichier}, statut : {response.status_code}")

            # réinitialisation de la variable deja_fait pour le prochain fichier
            deja_fait = False

print("Fin du script")