# Importation de la session et du moteur définis dans base.py
from base import Base, engine, session

# Importation de tous les modèles
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

# Importation de Faker pour générer des données fictives en français
from faker import Faker
# Importation du module random pour effectuer des choix aléatoires
import random

# Initialisation du générateur Faker avec la locale française
fake = Faker("fr_FR")

# Définition d'une graine pour obtenir des résultats reproductibles
random.seed(42)
Faker.seed(42)

# Création des tables si elles n'existent pas encore
Base.metadata.create_all(engine)

# Vérification préalable : on évite de réinsérer si la base contient déjà des données
if session.query(Patient).first() is not None:
    print("La base contient déjà des données. Supprimez centre_medical.db avant de relancer.")
    session.close()
    raise SystemExit

# =============================================================================
# 1. ETABLISSEMENTS
# =============================================================================

# Liste des types d'établissements possibles
types_etablissement = ["Clinique", "Antenne", "Cabinet", "Hôpital"]

# Initialisation de la liste locale des établissements
etablissements = []

# Boucle de création de 5 établissements avec des données aléatoires
for _ in range(5):
    e = Etablissement(
        nom=fake.company(),
        type=random.choice(types_etablissement),
        adresse=fake.address(),
        telephone=fake.phone_number(),
    )
    etablissements.append(e)

# Ajout groupé dans la session et validation
session.add_all(etablissements)
session.commit()

# Vérification en base du nombre d'établissements insérés
nb = session.query(Etablissement).count()
assert nb == len(etablissements), f"[ECHEC] Etablissements : attendu {len(etablissements)}, trouvé {nb}"
print(f"[OK] Etablissements insérés : {nb}")

# =============================================================================
# 2. MEDECINS
# =============================================================================

# Liste des spécialités médicales disponibles
specialites = [
    "Généraliste", "Cardiologue", "Dermatologue", "Pédiatre", "Neurologue",
    "Ophtalmologue", "Gynécologue", "Orthopédiste", "Psychiatre", "Radiologue"
]

# Initialisation de la liste locale des médecins
medecins = []

# Boucle de création de 20 médecins avec des données aléatoires
for _ in range(20):
    m = Medecin(
        nom=fake.last_name(),
        prenom=fake.first_name(),
        specialite=random.choice(specialites),
        email=fake.unique.email(),
    )
    medecins.append(m)

# Ajout groupé dans la session et validation
session.add_all(medecins)
session.commit()

# Vérification en base du nombre de médecins insérés
nb = session.query(Medecin).count()
assert nb == len(medecins), f"[ECHEC] Medecins : attendu {len(medecins)}, trouvé {nb}"
print(f"[OK] Médecins insérés : {nb}")

# =============================================================================
# 3. PATIENTS
# =============================================================================

# Initialisation de la liste locale des patients
patients = []

# Boucle de création de 200 patients avec des données aléatoires
for _ in range(200):
    numero_secu = str(fake.unique.random_number(digits=13, fix_len=True))
    p = Patient(
        nom=fake.last_name(),
        prenom=fake.first_name(),
        date_naissance=fake.date_of_birth(minimum_age=1, maximum_age=90),
        genre=random.choice(["M", "F"]),
        adresse=fake.address(),
        numero_securite_sociale=numero_secu,
    )
    patients.append(p)

# Ajout groupé dans la session et validation
session.add_all(patients)
session.commit()

# Vérification en base du nombre de patients insérés
nb = session.query(Patient).count()
assert nb == len(patients), f"[ECHEC] Patients : attendu {len(patients)}, trouvé {nb}"
print(f"[OK] Patients insérés : {nb}")

# =============================================================================
# 4. ASSOCIATIONS MEDECIN ↔ ETABLISSEMENT
# =============================================================================

# Compteur pour la vérification
nb_liens = 0

# Pour chaque médecin, affiliation à 1 ou 2 établissements choisis aléatoirement
for medecin in medecins:
    etabs_associes = random.sample(etablissements, k=random.randint(1, 2))
    for etab in etabs_associes:
        lien = MedecinEtablissement(
            id_medecin=medecin.id,
            id_etablissement=etab.id,
        )
        session.add(lien)
        nb_liens += 1

# Validation de la transaction
session.commit()

# Vérification en base du nombre de liens insérés
nb = session.query(MedecinEtablissement).count()
assert nb == nb_liens, f"[ECHEC] Affiliations : attendu {nb_liens}, trouvé {nb}"
print(f"[OK] Affiliations médecin-établissement insérées : {nb}")

# =============================================================================
# 5. CONSULTATIONS
# =============================================================================

# Liste des motifs de consultation possibles
motifs = [
    "Fièvre", "Douleur thoracique", "Contrôle annuel", "Toux persistante",
    "Maux de tête", "Fatigue", "Douleur abdominale", "Suivi traitement", "Bilan sanguin"
]

# Initialisation de la liste locale des consultations
consultations = []

# Boucle de création de 400 consultations dans les 5 dernières années
for _ in range(400):
    patient = random.choice(patients)
    medecin = random.choice(medecins)
    c = Consultation(
        date_consultation=fake.date_time_between(start_date="-5y", end_date="now"),
        motif=random.choice(motifs),
        id_patient=patient.id,
        id_medecin=medecin.id,
    )
    consultations.append(c)

# Ajout groupé dans la session et validation
session.add_all(consultations)
session.commit()

# Vérification en base du nombre de consultations insérées
nb = session.query(Consultation).count()
assert nb == len(consultations), f"[ECHEC] Consultations : attendu {len(consultations)}, trouvé {nb}"
print(f"[OK] Consultations insérées : {nb}")

# =============================================================================
# 6. PRESCRIPTIONS
# =============================================================================

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

# Initialisation de la liste locale des prescriptions
prescriptions = []

# 60% des consultations génèrent une prescription
for consultation in consultations:
    if random.random() < 0.6:
        p = Prescription(
            date=consultation.date_consultation.date(),
            description=random.choice(descriptions),
            id_consultation=consultation.id,
        )
        prescriptions.append(p)

# Ajout groupé dans la session et validation
session.add_all(prescriptions)
session.commit()

# Vérification en base du nombre de prescriptions insérées
nb = session.query(Prescription).count()
assert nb == len(prescriptions), f"[ECHEC] Prescriptions : attendu {len(prescriptions)}, trouvé {nb}"
print(f"[OK] Prescriptions insérées : {nb}")

# =============================================================================
# 7. RENDEZ-VOUS
# =============================================================================

# Liste des statuts possibles pour les rendez-vous
statuts_rdv = ["Planifié", "Effectué", "Annulé"]

# Initialisation de la liste locale des rendez-vous
rendezvous = []

# Boucle de création de 300 rendez-vous entre -2 ans et +1 an
for _ in range(300):
    patient = random.choice(patients)
    medecin = random.choice(medecins)
    etabs_medecin = [lien.etablissement for lien in medecin.etablissements]
    etablissement = random.choice(etabs_medecin) if etabs_medecin else random.choice(etablissements)
    rdv = RendezVous(
        date_heure=fake.date_time_between(start_date="-2y", end_date="+1y"),
        statut=random.choice(statuts_rdv),
        id_patient=patient.id,
        id_medecin=medecin.id,
        id_etablissement=etablissement.id,
    )
    rendezvous.append(rdv)

# Ajout groupé dans la session et validation
session.add_all(rendezvous)
session.commit()

# Vérification en base du nombre de rendez-vous insérés
nb = session.query(RendezVous).count()
assert nb == len(rendezvous), f"[ECHEC] RendezVous : attendu {len(rendezvous)}, trouvé {nb}"
print(f"[OK] Rendez-vous insérés : {nb}")

# =============================================================================
# 8. EXAMENS
# =============================================================================

# Liste des types d'examen disponibles
types_examen = [
    "Radiographie", "IRM", "Échographie", "Prise de sang",
    "Electrocardiogramme", "Scanner", "Audiogramme"
]

# Liste des résultats possibles
resultats = [
    "Normal", "Anomalie détectée", "En attente d'interprétation",
    "Résultat positif", "Résultat négatif"
]

# Initialisation de la liste locale des examens
examens = []

# Boucle de création de 250 examens dans les 5 dernières années
for _ in range(250):
    patient = random.choice(patients)
    e = Examen(
        type_examen=random.choice(types_examen),
        resultat=random.choice(resultats),
        date=fake.date_between(start_date="-5y", end_date="today"),
        id_patient=patient.id,
    )
    examens.append(e)

# Ajout groupé dans la session et validation
session.add_all(examens)
session.commit()

# Vérification en base du nombre d'examens insérés
nb = session.query(Examen).count()
assert nb == len(examens), f"[ECHEC] Examens : attendu {len(examens)}, trouvé {nb}"
print(f"[OK] Examens insérés : {nb}")

# =============================================================================
# 9. FACTURES
# =============================================================================

# Liste des statuts possibles pour les factures
statuts_facture = ["Payée", "En attente", "Annulée"]

# Initialisation de la liste locale des factures
factures = []

# 70% des patients reçoivent une facture
for patient in patients:
    if random.random() < 0.7:
        f = Facture(
            montant=round(random.uniform(20.0, 500.0), 2),
            date=fake.date_between(start_date="-2y", end_date="today"),
            statut=random.choice(statuts_facture),
            id_patient=patient.id,
        )
        factures.append(f)

# Ajout groupé dans la session et validation
session.add_all(factures)
session.commit()

# Vérification en base du nombre de factures insérées
nb = session.query(Facture).count()
assert nb == len(factures), f"[ECHEC] Factures : attendu {len(factures)}, trouvé {nb}"
print(f"[OK] Factures insérées : {nb}")

# =============================================================================
# 10. UTILISATEURS
# =============================================================================

# Création du compte administrateur principal
admin = Utilisateur(
    login="admin",
    mot_de_passe=fake.sha256(),
    role="Admin",
    medecin_id=None,
)
session.add(admin)

# Boucle de création de 3 comptes secrétaires
for i in range(3):
    secretaire = Utilisateur(
        login=f"secretaire{i + 1}",
        mot_de_passe=fake.sha256(),
        role="Secretaire",
        medecin_id=None,
    )
    session.add(secretaire)

# Boucle de création d'un compte MedecinUser pour chaque médecin
for medecin in medecins:
    login_medecin = f"dr.{medecin.nom.lower().replace(' ', '')}{medecin.id}"
    utilisateur_medecin = Utilisateur(
        login=login_medecin,
        mot_de_passe=fake.sha256(),
        role="MedecinUser",
        medecin_id=medecin.id,
    )
    session.add(utilisateur_medecin)

# Validation finale de la transaction
session.commit()

# Vérification en base du nombre total d'utilisateurs insérés
nb_attendu = 1 + 3 + len(medecins)
nb = session.query(Utilisateur).count()
assert nb == nb_attendu, f"[ECHEC] Utilisateurs : attendu {nb_attendu}, trouvé {nb}"
print(f"[OK] Utilisateurs insérés : {nb}")

# =============================================================================
# RECAPITULATIF FINAL
# =============================================================================

print("\\n=== Insertion terminée avec succès ===")
print(f"  Etablissements   : {session.query(Etablissement).count()}")
print(f"  Médecins         : {session.query(Medecin).count()}")
print(f"  Patients         : {session.query(Patient).count()}")
print(f"  Affiliations     : {session.query(MedecinEtablissement).count()}")
print(f"  Consultations    : {session.query(Consultation).count()}")
print(f"  Prescriptions    : {session.query(Prescription).count()}")
print(f"  Rendez-vous      : {session.query(RendezVous).count()}")
print(f"  Examens          : {session.query(Examen).count()}")
print(f"  Factures         : {session.query(Facture).count()}")
print(f"  Utilisateurs     : {session.query(Utilisateur).count()}")

# Fermeture propre de la session
session.close()