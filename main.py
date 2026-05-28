################################################################################
##
# @file main.py
# @brief Point d'entrée principal du projet SGBD - Centre Médical
#
# @details
# Ce module centralise l'exécution des différentes parties du projet :
# création et insertion des données, extraction des données et création des graphiques.
#
# **Projet:** Projet SGBD - Centre Médical
# **Formation:** Polytech Tours
# **Auteur:** Leo NOUHOUANG - Mohamed Yassine BEN ABDA
# **Date:** Mai 2026
#
################################################################################

def main():
    print("=== Projet SGBD - Centre Médical ===")

    print("\n[1/3] Création de la base et insertion des données...")
    import insertion_donnees as insertion_donnees
    insertion_donnees.run()

    print("\n[2/3] Extraction des données et export CSV...")
    import visualisation_CSV as partie4
    partie4.run()

    print("\n[3/3] Création des graphiques...")
    import creation_graphe as partie5
    partie5.run()

    print("\n=== Fin du traitement ===")


if __name__ == "__main__":
    main()