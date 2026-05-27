################################################################################
##
# @file model_patient.py
# @brief Modèle SQLAlchemy pour la table PATIENT
#
# @details
# Définit la classe Patient avec une contrainte CHECK sur le genre
# et ses relations vers Consultation, RendezVous, Examen et Facture.
#
# **Projet:** Projet SGBD - Centre Médical
# **Formation:** Polytech Tours
# **Auteur:** Leo NOUHOUANG
# **Date:** Mai 2026
#
################################################################################

# Importation de la base déclarative partagée
from base import Base
# Importation des types de colonnes nécessaires
from sqlalchemy import Column, Integer, String, Date, Text, CheckConstraint
# Importation de relationship pour déclarer les liens vers d'autres modèles
from sqlalchemy.orm import relationship

class Patient(Base):
    # Nom physique de la table en base de données
    __tablename__ = "patient"

    id = Column(Integer, primary_key=True, autoincrement=True) # Clé primaire auto-incrémentée
    nom = Column(String(100), nullable=False) # Nom de famille, obligatoire
    prenom = Column(String(100), nullable=False) # Prénom, obligatoire
    date_naissance = Column(Date, nullable=False) # Date de naissance, obligatoire
    genre = Column(String(1), nullable=True) # Genre : M ou F
    adresse = Column(Text, nullable=True) # Adresse postale, optionnelle
    numero_securite_sociale = Column(String(15),  nullable=False, unique=True) # Numéro de sécu unique et obligatoire

    # Contrainte CHECK : le genre ne peut prendre que les valeurs M ou F
    __table_args__ = (
        CheckConstraint("genre IN ('M', 'F')", name="check_genre"),
    )

    # Relation vers les consultations du patient
    consultations = relationship("Consultation", back_populates="patient")
    # Relation vers les rendez-vous du patient
    rendezvous = relationship("RendezVous", back_populates="patient")
    # Relation vers les examens du patient
    examens = relationship("Examen", back_populates="patient")
    # Relation vers les factures du patient
    factures = relationship("Facture", back_populates="patient")