################################################################################
##
# @file creation_graphe.py
# @brief Création des graphiques à partir des CSV générés par la partie 4 (visualisation_CSV.py)
#
# @details
# Ce module lit les fichiers CSV extraits de la base de données
# et produit des visualisations avec Matplotlib.
#
# **Projet:** Projet SGBD - Centre Médical
# **Formation:** Polytech Tours
# **Auteur:** Leo NOUHOUANG - Mohamed Yassine BEN ABDA
# **Date:** Mai 2026
#
################################################################################

import pandas as pd
import matplotlib.pyplot as plt


def run():
    # Chargement des fichiers CSV générés à la partie 4
    df_medecins = pd.read_csv("consultations_par_medecin_et_annee.csv")
    df_etabs = pd.read_csv("rendezvous_par_etablissement_et_annee.csv")
    df_patients = pd.read_csv("consultations_par_patient_5_ans.csv")

    ################################################################################
    # 1. Surcharge des médecins sur toutes les années
    ################################################################################

    # Agrégation des consultations par médecin
    df_agrege1 = df_medecins.groupby("nom_medecin")["nb_consultations"].sum()

    # Préparation des axes
    x = df_agrege1.index.astype(str)
    y = df_agrege1.values

    plt.figure(figsize=(10, 5))
    plt.bar(x, y, color="steelblue")
    plt.title("Nombre total de consultations par médecin")
    plt.xlabel("Médecin")
    plt.ylabel("Nombre de consultations")
    plt.grid(axis="y")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

    ################################################################################
    # 2. Établissements les plus fréquents
    ################################################################################

    # Agrégation des rendez-vous par établissement
    df_agrege2 = df_etabs.groupby("nom_etablissement")["nb_rendezvous"].sum()

    # Préparation des axes
    x = df_agrege2.index.astype(str)
    y = df_agrege2.values

    plt.figure(figsize=(10, 5))
    plt.bar(x, y, color="darkorange")
    plt.title("Établissements les plus fréquents")
    plt.xlabel("Établissement")
    plt.ylabel("Nombre de rendez-vous")
    plt.grid(axis="y")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

    ################################################################################
    # 3. Activité médicale des patients sur les cinq dernières années
    ################################################################################

    # Agrégation des consultations par patient
    df_agrege3 = (
        df_patients.groupby(["nom_patient", "prenom_patient"])["nb_consultations"]
        .sum()
        .sort_values(ascending=False)
    )

    # Préparation des axes
    x = [f"{nom} {prenom}" for nom, prenom in df_agrege3.index]
    y = df_agrege3.values

    plt.figure(figsize=(12, 6))
    plt.bar(x, y, color="seagreen")
    plt.title("Activité médicale des patients sur les cinq dernières années")
    plt.xlabel("Patient")
    plt.ylabel("Nombre de consultations")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    run()