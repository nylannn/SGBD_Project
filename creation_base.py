################################################################################
##
# @file creation_base.py
# @brief Création physique de toutes les tables en base de données
#
# @details
# Importe tous les modèles puis appelle Base.metadata.create_all()
# pour générer les tables dans le bon ordre (dépendances FK respectées).
#
# **Projet:** Projet SGBD - Centre Médical
# **Formation:** Polytech Tours
# **Auteur:** Leo NOUHOUANG
# **Date:** Mai 2026
#
################################################################################

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
# SQLAlchemy génère les CREATE TABLE dans le bon ordre selon les dépendances entre clés étrangères
Base.metadata.create_all(engine)