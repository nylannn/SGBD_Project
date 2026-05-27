# Importation de la base déclarative, du moteur et de la session définis dans base.py
from base import Base, engine, session
# Importation de Faker pour générer des données fictives cohérentes
from faker import Faker
import random

fake = Faker("fr_FR")


# Import de chaque modèle pour que SQLAlchemy les enregistre
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


# Création des tables si elles n'existent pas encore
Base.metadata.create_all(engine)

# Définition d'une graine aléatoire pour obtenir des résultats reproductibles
random.seed(42)
Faker.seed(42)

# Vérification préalable : on évite de réinsérer les données si la base contient déjà des patients
if session.query(Patient).first() is not None:
    print("La base contient déjà des données. Suppression ou nouvelle base recommandée avant réinsertion.")
    session.close()
    raise SystemExit

# ================================================================================
# 1. Génération des établissements
# ================================================================================

# Liste des types d'établissements possibles
types_etablissement = ["Clinique", "Antenne", "Cabinet", "Hôpital"]

etablissements = []

# Boucle de création de 5 établissements
for _ in range(5):
    # Instanciation d'un établissement avec des données générées aléatoirement
    e = Etablissement(
        nom=fake.company(),
        type=random.choice(types_etablissement),
        adresse=fake.address(),
        telephone=fake.phone_number(),
    )
    etablissements.append(e)

# Ajout groupé des établissements dans la session
session.add_all(etablissements)
session.commit()

# ================================================================================
# 2. Génération des médecins
# ================================================================================

# Liste des spécialités médicales disponibles
specialites = [
    "Généraliste", "Cardiologue", "Dermatologue", "Pédiatre", "Neurologue",
    "Ophtalmologue", "Gynécologue", "Orthopédiste", "Psychiatre", "Radiologue"
]

medecins = []

# Boucle de création de 20 médecins
for _ in range(20):
    # Instanciation d'un médecin avec des données générées aléatoirement
    m = Medecin(
        nom=fake.last_name(),
        prenom=fake.first_name(),
        specialite=random.choice(specialites),
        email=fake.unique.email(),
    )
    medecins.append(m)

# Ajout groupé des médecins dans la session
session.add_all(medecins)
session.commit()

# ================================================================================
# 3. Génération des patients
# ================================================================================

# Initialisation de la liste locale des patients
patients = []

# Boucle de création de 200 patients
for _ in range(200):
    # Génération d'un numéro de sécurité sociale unique sur 13 chiffres
    numero_secu = str(fake.unique.random_number(digits=13, fix_len=True))
    # Instanciation d'un patient avec des données générées aléatoirement
    p = Patient(
        nom=fake.last_name(),
        prenom=fake.first_name(),
        date_naissance=fake.date_of_birth(minimum_age=1, maximum_age=90),
        genre=random.choice(["M", "F"]),
        adresse=fake.address(),
        numero_securite_sociale=numero_secu,
    )
    patients.append(p)

# Ajout groupé des patients dans la session
session.add_all(patients)
session.commit()

# ================================================================================
# 4. Association médecins ↔ établissements
# ================================================================================

# Pour chaque médecin, création de 1 ou 2 affiliations à des établissements
for medecin in medecins:
    # Sélection aléatoire d'un ou deux établissements distincts
    etabs_associes = random.sample(etablissements, k=random.randint(1, 2))
    for etab in etabs_associes:
        # Création d'un lien entre le médecin et l'établissement
        lien = MedecinEtablissement(
            id_medecin=medecin.id,
            id_etablissement=etab.id,
        )
        session.add(lien)

session.commit()

# ================================================================================
# 5. Génération des consultations
# ================================================================================

# Liste des motifs de consultation possibles
motifs = [
    "Fièvre", "Douleur thoracique", "Contrôle annuel", "Toux persistante",
    "Maux de tête", "Fatigue", "Douleur abdominale", "Suivi traitement", "Bilan sanguin"
]
consultations = []

# Boucle de création de 400 consultations passées
for _ in range(400):
    patient = random.choice(patients)
    medecin = random.choice(medecins)
    # Instanciation d'une consultation cohérente dans les 5 dernières années
    c = Consultation(
        date_consultation=fake.date_time_between(start_date="-5y", end_date="now"),
        motif=random.choice(motifs),
        id_patient=patient.id,
        id_medecin=medecin.id,
    )
    consultations.append(c)

# Ajout groupé des consultations dans la session
session.add_all(consultations)
session.commit()

# ================================================================================
# 6. Génération des prescriptions
# ================================================================================

# Liste des descriptions de prescription possibles
descriptions = [
    "Paracétamol 500mg - 3 fois par jour pendant 5 jours",
    "Ibuprofène 400mg - 2 fois par jour pendant 7 jours",
    "Amoxicilline 1g - 2 fois par jour pendant 10 jours",
    "Oméprazole 20mg - 1 fois par jour pendant 1 mois",
    "Ventoline - en cas de crise",
    "Metformine 500mg - 2 fois par jour",
    "Doliprane 1g - selon la douleur",
]
prescriptions = []

for consultation in consultations:
    # Tirage aléatoire pour décider si la consultation produit une prescription
    if random.random() < 0.6:
        # Création de la prescription liée à la consultation
        p = Prescription(
            date=consultation.date_consultation.date(),
            description=random.choice(descriptions),
            id_consultation=consultation.id,
        )
        prescriptions.append(p)

# Ajout groupé des prescriptions dans la session
session.add_all(prescriptions)
session.commit()

# ================================================================================
# 7. Génération des rendez-vous
# ================================================================================

# Liste des statuts possibles pour les rendez-vous
statuts_rdv = ["Planifié", "Effectué", "Annulé"]
rendezvous = []

# Boucle de création de 300 rendez-vous répartis dans le passé et le futur
for _ in range(300):
    patient = random.choice(patients)
    medecin = random.choice(medecins)
    etabs_medecin = [lien.etablissement for lien in medecin.etablissements]
    etablissement = random.choice(etabs_medecin) if etabs_medecin else random.choice(etablissements) # Sélection d'un établissement cohérent avec le médecin ; fallback sur tous les établissements si besoin
    # Création du rendez-vous avec une date entre -2 ans et +1 an
    rdv = RendezVous(
        date_heure=fake.date_time_between(start_date="-2y", end_date="+1y"),
        statut=random.choice(statuts_rdv),
        id_patient=patient.id,
        id_medecin=medecin.id,
        id_etablissement=etablissement.id,
    )
    rendezvous.append(rdv)

# Ajout groupé des rendez-vous dans la session
session.add_all(rendezvous)
session.commit()

# ================================================================================
# 8. Génération des examens
# ================================================================================

# Liste des types d'examen disponibles
types_examen = [
    "Radiographie", "IRM", "Échographie", "Prise de sang",
    "Electrocardiogramme", "Scanner", "Audiogramme"
]

# Liste des résultats possibles pour un examen
resultats = [
    "Normal", "Anomalie détectée", "En attente d'interprétation",
    "Résultat positif", "Résultat négatif"
]

# Initialisation de la liste locale des examens
examens = []

# Boucle de création de 250 examens
for _ in range(250):
    # Sélection aléatoire d'un patient
    patient = random.choice(patients)
    # Création d'un examen daté dans les 5 dernières années
    e = Examen(
        type_examen=random.choice(types_examen),
        resultat=random.choice(resultats),
        date=fake.date_between(start_date="-5y", end_date="today"),
        id_patient=patient.id,
    )
    # Ajout de l'examen dans la liste locale
    examens.append(e)

# Ajout groupé des examens dans la session
session.add_all(examens)
# Validation de la transaction
session.commit()

# ================================================================================
# 9. Génération des factures
# ================================================================================

# Liste des statuts possibles pour les factures
statuts_facture = ["Payée", "En attente", "Annulée"]

# Initialisation de la liste locale des factures
factures = []

# Parcours des patients pour créer une facture pour une partie d'entre eux
for patient in patients:
    # Tirage aléatoire pour décider si le patient reçoit une facture
    if random.random() < 0.7:
        # Création de la facture associée au patient
        f = Facture(
            montant=round(random.uniform(20.0, 500.0), 2),
            date=fake.date_between(start_date="-2y", end_date="today"),
            statut=random.choice(statuts_facture),
            id_patient=patient.id,
        )
        # Ajout de la facture dans la liste locale
        factures.append(f)

# Ajout groupé des factures dans la session
session.add_all(factures)
session.commit()

# ================================================================================
# 10. Génération des utilisateurs
# ================================================================================

# Création du compte administrateur principal
admin = Utilisateur(
    login="admin",
    mot_de_passe=fake.sha256(),
    role="Admin",
    medecin_id=None,
)

# Ajout de l'administrateur dans la session
session.add(admin)

# Boucle de création de 3 comptes secrétaires
for i in range(3):
    # Création d'un compte secrétaire
    secretaire = Utilisateur(
        login=f"secretaire{i + 1}",
        mot_de_passe=fake.sha256(),
        role="Secretaire",
        medecin_id=None,
    )
    # Ajout du compte secrétaire dans la session
    session.add(secretaire)

# Boucle de création d'un compte MedecinUser pour chaque médecin
for medecin in medecins:
    # Construction d'un login simple à partir du nom et de l'identifiant du médecin
    login_medecin = f"dr.{medecin.nom.lower().replace(' ', '')}{medecin.id}"
    # Création du compte utilisateur médecin
    utilisateur_medecin = Utilisateur(
        login=login_medecin,
        mot_de_passe=fake.sha256(),
        role="MedecinUser",
        medecin_id=medecin.id,
    )
    # Ajout du compte utilisateur dans la session
    session.add(utilisateur_medecin)

# Validation finale de la transaction
session.commit()

# ================================================================================
# RECAPITULATIF FINAL
# ================================================================================

# Affichage d'un récapitulatif des données insérées
print("\\n=== Données insérées avec succès ===")
print(f"Établissements : {len(etablissements)}")
print(f"Médecins       : {len(medecins)}")
print(f"Patients       : {len(patients)}")
print(f"Consultations  : {len(consultations)}")
print(f"Prescriptions  : {len(prescriptions)}")
print(f"Rendez-vous    : {len(rendezvous)}")
print(f"Examens        : {len(examens)}")
print(f"Factures       : {len(factures)}")
print(f"Utilisateurs   : {1 + 3 + len(medecins)}")

# Fermeture propre de la session
session.close()