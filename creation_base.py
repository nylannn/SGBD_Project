from base import Base, engine

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

# Création de toutes les tables dans le bon ordre
Base.metadata.create_all(engine)