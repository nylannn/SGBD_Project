################################################################################
##
# @file model_medecin.py
# @brief Modèle SQLAlchemy pour la table MEDECIN
#
# @details
# Définit la classe Medecin et ses relations vers
# MedecinEtablissement, Consultation, RendezVous et Utilisateur.
#
# **Projet:** Projet SGBD - Centre Médical
# **Formation:** Polytech Tours
# **Auteur:** Leo NOUHOUANG - Mohamed Yassine BEN ABDA
# **Date:** Mai 2026
#
################################################################################

# Importation de la base déclarative partagée
from base import Base

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Medecin(Base):
    # Nom physique de la table en base de données
    __tablename__ = "medecin"

    id = Column(Integer, primary_key=True, autoincrement=True) # Clé primaire auto-incrémentée
    nom = Column(String(100), nullable=False) # Nom de famille, obligatoire
    prenom = Column(String(100), nullable=False) # Prénom, obligatoire
    specialite = Column(String(100), nullable=False) # Spécialité médicale, obligatoire
    email = Column(String(150), nullable=False, unique=True) # Email unique et obligatoire

    # Relation vers la table d'association (un médecin peut être affilié à plusieurs établissements)
    etablissements = relationship("MedecinEtablissement", back_populates="medecin")
    # Relation vers les consultations réalisées par ce médecin
    consultations = relationship("Consultation", back_populates="medecin")
    # Relation vers les rendez-vous assurés par ce médecin
    rendezvous = relationship("RendezVous", back_populates="medecin")
    # Relation vers le compte utilisateur associé à ce médecin (un seul compte possible)
    utilisateur = relationship("Utilisateur", back_populates="medecin", uselist=False)