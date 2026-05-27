################################################################################
##
# @file insert.py
# @brief Génération et insertion des données dans la base de données
#
# @details
# Ce module génère des données fictives à l'aide de la librairie Faker
# et les insère dans la base de données SQLite du centre médical.
# Les insertions sont vérifiées après chaque bloc via des assertions.
#
# **Projet:** Projet SGBD - Centre Médical
# **Formation:** Polytech Tours
# **Auteur:** Leo NOUHOUANG
# **Date:** Mai 2026
#
# @section order_sec Ordre d'insertion
# 1. Etablissements
# 2. Médecins
# 3. Patients
# 4. Associations médecin ↔ établissement
# 5. Consultations
# 6. Prescriptions
# 7. Rendez-vous
# 8. Examens
# 9. Factures
# 10. Utilisateurs
#
################################################################################

from base import Base, engine, session

from model_etablissement import Etablissement
from model_medecin import Medecin
from model_patient import Patient
from model_medecin_etablissement import MedecinEtablissement
from model_consultation import Consultation
from model_prescription import Prescription
from model_rendezvous import RendezVous
from model_examen import Examen
from model_facture import Facture
from model_utilisateur import Utilisateur

from faker import Faker
import random

def count_rows(model):
    return session.execute(select(func.count()).select_from(model)).scalar()

def first_patient():
    return session.execute(select(Patient)).first()

def run():
        
    # Initialisation du générateur Faker avec la locale française
    fake = Faker("fr_FR")
    
    # Graine fixe pour garantir la reproductibilité des données générées
    random.seed(42)
    Faker.seed(42)
    
    # Création des tables si elles n'existent pas encore
    Base.metadata.create_all(engine)
    
    # Vérification préalable : on évite de réinsérer si la base contient déjà des données
    if first_patient() is not None:
        print("La base contient déjà des données. Supprimez centre_medical.db avant de relancer.")
        session.close()
        raise SystemExit
    
    ################################################################################
    # 1. ETABLISSEMENTS
    ################################################################################
    
    # Types d'établissements possibles
    liste_types_etablissement = ["Clinique", "Antenne", "Cabinet", "Hôpital"]
    
    liste_etablissements = []
    
    for _ in range(5):
        o_etablissement = Etablissement(
            nom=fake.company(),
            type=random.choice(liste_types_etablissement),
            adresse=fake.address(),
            telephone=fake.phone_number(),
        )
        liste_etablissements.append(o_etablissement)
    
    session.add_all(liste_etablissements)
    session.commit()
    
    # Vérification en base
    i_nb = count_rows(Etablissement)
    assert i_nb == len(liste_etablissements), f"[ECHEC] Etablissements : attendu {len(liste_etablissements)}, trouvé {i_nb}"
    print(f"[OK] Etablissements insérés : {i_nb}")
    
    ################################################################################
    # 2. MEDECINS
    ################################################################################
    
    # Spécialités médicales disponibles
    liste_specialites = [
        "Généraliste", "Cardiologue", "Dermatologue", "Pédiatre", "Neurologue",
        "Ophtalmologue", "Gynécologue", "Orthopédiste", "Psychiatre", "Radiologue"
    ]
    
    liste_medecins = []
    
    for _ in range(20):
        o_medecin = Medecin(
            nom=fake.last_name(),
            prenom=fake.first_name(),
            specialite=random.choice(liste_specialites),
            email=fake.unique.email(),
        )
        liste_medecins.append(o_medecin)
    
    session.add_all(liste_medecins)
    session.commit()
    
    # Vérification en base
    i_nb = count_rows(Medecin)
    assert i_nb == len(liste_medecins), f"[ECHEC] Medecins : attendu {len(liste_medecins)}, trouvé {i_nb}"
    print(f"[OK] Médecins insérés : {i_nb}")
    
    ################################################################################
    # 3. PATIENTS
    ################################################################################
    
    liste_patients = []
    
    for _ in range(200):
        # Numéro de sécurité sociale unique à 13 chiffres
        s_numero_secu = str(fake.unique.random_number(digits=13, fix_len=True))
        o_patient = Patient(
            nom=fake.last_name(),
            prenom=fake.first_name(),
            date_naissance=fake.date_of_birth(minimum_age=1, maximum_age=90),
            genre=random.choice(["M", "F"]),
            adresse=fake.address(),
            numero_securite_sociale=s_numero_secu,
        )
        liste_patients.append(o_patient)
    
    session.add_all(liste_patients)
    session.commit()
    
    # Vérification en base
    i_nb = count_rows(Patient)
    assert i_nb == len(liste_patients), f"[ECHEC] Patients : attendu {len(liste_patients)}, trouvé {i_nb}"
    print(f"[OK] Patients insérés : {i_nb}")
    
    ################################################################################
    # 4. ASSOCIATIONS MEDECIN <-> ETABLISSEMENT
    ################################################################################
    
    i_nb_liens = 0
    
    # Chaque médecin est affilié à 1 ou 2 établissements aléatoires
    for o_medecin in liste_medecins:
        liste_etabs_associes = random.sample(liste_etablissements, k=random.randint(1, 2))
        for o_etab in liste_etabs_associes:
            o_lien = MedecinEtablissement(
                id_medecin=o_medecin.id,
                id_etablissement=o_etab.id,
            )
            session.add(o_lien)
            i_nb_liens += 1
    
    session.commit()
    
    # Vérification en base
    i_nb = count_rows(MedecinEtablissement)
    assert i_nb == i_nb_liens, f"[ECHEC] Affiliations : attendu {i_nb_liens}, trouvé {i_nb}"
    print(f"[OK] Affiliations médecin-établissement insérées : {i_nb}")
    
    ################################################################################
    # 5. CONSULTATIONS
    ################################################################################
    
    # Motifs de consultation possibles
    liste_motifs = [
        "Fièvre", "Douleur thoracique", "Contrôle annuel", "Toux persistante",
        "Maux de tête", "Fatigue", "Douleur abdominale", "Suivi traitement", "Bilan sanguin"
    ]
    
    liste_consultations = []
    
    # 400 consultations dans les 5 dernières années
    for _ in range(400):
        o_patient = random.choice(liste_patients)
        o_medecin = random.choice(liste_medecins)
        o_consultation = Consultation(
            date_consultation=fake.date_time_between(start_date="-5y", end_date="now"),
            motif=random.choice(liste_motifs),
            id_patient=o_patient.id,
            id_medecin=o_medecin.id,
        )
        liste_consultations.append(o_consultation)
    
    session.add_all(liste_consultations)
    session.commit()
    
    # Vérification en base
    i_nb = count_rows(Consultation)
    assert i_nb == len(liste_consultations), f"[ECHEC] Consultations : attendu {len(liste_consultations)}, trouvé {i_nb}"
    print(f"[OK] Consultations insérées : {i_nb}")
    
    ################################################################################
    # 6. PRESCRIPTIONS
    ################################################################################
    
    # Descriptions de prescription possibles
    liste_descriptions = [
        "Paracétamol 500mg - 3 fois par jour pendant 5 jours",
        "Ibuprofène 400mg - 2 fois par jour pendant 7 jours",
        "Amoxicilline 1g - 2 fois par jour pendant 10 jours",
        "Oméprazole 20mg - 1 fois par jour pendant 1 mois",
        "Ventoline - en cas de crise",
        "Metformine 500mg - 2 fois par jour",
        "Doliprane 1g - selon la douleur",
    ]
    
    liste_prescriptions = []
    
    # 60% des consultations génèrent une prescription
    for o_consultation in liste_consultations:
        if random.random() < 0.6:
            o_prescription = Prescription(
                date=o_consultation.date_consultation.date(),
                description=random.choice(liste_descriptions),
                id_consultation=o_consultation.id,
            )
            liste_prescriptions.append(o_prescription)
    
    session.add_all(liste_prescriptions)
    session.commit()
    
    # Vérification en base
    i_nb = count_rows(Prescription)
    assert i_nb == len(liste_prescriptions), f"[ECHEC] Prescriptions : attendu {len(liste_prescriptions)}, trouvé {i_nb}"
    print(f"[OK] Prescriptions insérées : {i_nb}")
    
    ################################################################################
    # 7. RENDEZ-VOUS
    ################################################################################
    
    # Statuts de rendez-vous possibles
    liste_statuts_rdv = ["Planifié", "Effectué", "Annulé"]
    
    liste_rendezvous = []
    
    # 300 rendez-vous entre -2 ans et +1 an (passé et futur)
    for _ in range(300):
        o_patient = random.choice(liste_patients)
        o_medecin = random.choice(liste_medecins)
        # Sélection d'un établissement cohérent avec le médecin via ses affiliations
        liste_etabs_medecin = [lien.etablissement for lien in o_medecin.etablissements]
        o_etablissement = random.choice(liste_etabs_medecin) if liste_etabs_medecin else random.choice(liste_etablissements)
        o_rdv = RendezVous(
            date_heure=fake.date_time_between(start_date="-2y", end_date="+1y"),
            statut=random.choice(liste_statuts_rdv),
            id_patient=o_patient.id,
            id_medecin=o_medecin.id,
            id_etablissement=o_etablissement.id,
        )
        liste_rendezvous.append(o_rdv)
    
    session.add_all(liste_rendezvous)
    session.commit()
    
    # Vérification en base
    i_nb = count_rows(RendezVous)
    assert i_nb == len(liste_rendezvous), f"[ECHEC] RendezVous : attendu {len(liste_rendezvous)}, trouvé {i_nb}"
    print(f"[OK] Rendez-vous insérés : {i_nb}")
    
    ################################################################################
    # 8. EXAMENS
    ################################################################################
    
    # Types d'examen disponibles
    liste_types_examen = [
        "Radiographie", "IRM", "Échographie", "Prise de sang",
        "Electrocardiogramme", "Scanner", "Audiogramme"
    ]
    
    # Résultats possibles pour un examen
    liste_resultats = [
        "Normal", "Anomalie détectée", "En attente d'interprétation",
        "Résultat positif", "Résultat négatif"
    ]
    
    liste_examens = []
    
    # 250 examens dans les 5 dernières années
    for _ in range(250):
        o_patient = random.choice(liste_patients)
        o_examen = Examen(
            type_examen=random.choice(liste_types_examen),
            resultat=random.choice(liste_resultats),
            date=fake.date_between(start_date="-5y", end_date="today"),
            id_patient=o_patient.id,
        )
        liste_examens.append(o_examen)
    
    session.add_all(liste_examens)
    session.commit()
    
    # Vérification en base
    i_nb = count_rows(Examen)
    assert i_nb == len(liste_examens), f"[ECHEC] Examens : attendu {len(liste_examens)}, trouvé {i_nb}"
    print(f"[OK] Examens insérés : {i_nb}")
    
    ################################################################################
    # 9. FACTURES
    ################################################################################
    
    # Statuts de facture possibles
    liste_statuts_facture = ["Payée", "En attente", "Annulée"]
    
    liste_factures = []
    
    # 70% des patients reçoivent une facture
    for o_patient in liste_patients:
        if random.random() < 0.7:
            o_facture = Facture(
                montant=round(random.uniform(20.0, 500.0), 2),
                date=fake.date_between(start_date="-2y", end_date="today"),
                statut=random.choice(liste_statuts_facture),
                id_patient=o_patient.id,
            )
            liste_factures.append(o_facture)
    
    session.add_all(liste_factures)
    session.commit()
    
    # Vérification en base
    i_nb = count_rows(Facture)
    assert i_nb == len(liste_factures), f"[ECHEC] Factures : attendu {len(liste_factures)}, trouvé {i_nb}"
    print(f"[OK] Factures insérées : {i_nb}")
    
    ################################################################################
    # 10. UTILISATEURS
    ################################################################################
    
    # Compte administrateur principal
    o_admin = Utilisateur(
        login="admin",
        mot_de_passe=fake.sha256(),
        role="Admin",
        medecin_id=None,
    )
    session.add(o_admin)
    
    # 3 comptes secrétaires
    for i in range(3):
        o_secretaire = Utilisateur(
            login=f"secretaire{i + 1}",
            mot_de_passe=fake.sha256(),
            role="Secretaire",
            medecin_id=None,
        )
        session.add(o_secretaire)
    
    # Un compte MedecinUser par médecin
    for o_medecin in liste_medecins:
        s_login = f"dr.{o_medecin.nom.lower().replace(' ', '')}{o_medecin.id}"
        o_utilisateur = Utilisateur(
            login=s_login,
            mot_de_passe=fake.sha256(),
            role="MedecinUser",
            medecin_id=o_medecin.id,
        )
        session.add(o_utilisateur)
    
    session.commit()
    
    # Vérification en base
    i_nb_attendu = 1 + 3 + len(liste_medecins)
    i_nb = count_rows(Utilisateur)
    assert i_nb == i_nb_attendu, f"[ECHEC] Utilisateurs : attendu {i_nb_attendu}, trouvé {i_nb}"
    print(f"[OK] Utilisateurs insérés : {i_nb}")
    
    ################################################################################
    # RECAPITULATIF FINAL
    ################################################################################
    
    print("\n=== Insertion terminée avec succès ===")
    print(f"  Etablissements   : {count_rows(Etablissement)}")
    print(f"  Médecins         : {count_rows(Medecin)}")
    print(f"  Patients         : {count_rows(Patient)}")
    print(f"  Affiliations     : {count_rows(MedecinEtablissement)}")
    print(f"  Consultations    : {count_rows(Consultation)}")
    print(f"  Prescriptions    : {count_rows(Prescription)}")
    print(f"  Rendez-vous      : {count_rows(RendezVous)}")
    print(f"  Examens          : {count_rows(Examen)}")
    print(f"  Factures         : {count_rows(Facture)}")
    print(f"  Utilisateurs     : {count_rows(Utilisateur)}")
    
    session.close()

if __name__ == "__main__":
    run()