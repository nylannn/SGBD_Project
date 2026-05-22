# Importation de la base déclarative et du moteur définis dans base.py
from base import Base, engine

# Importation de tous les modèles pour que SQLAlchemy les enregistre avant la création des tables
from models import (
    Etablissement,
    Medecin,
    Patient,
    MedecinEtablissement,
    Consultation,
    Prescription,
    RendezVous,
    Examen,
    Facture,
    Utilisateur,
)
Base.metadata.create_all(engine)