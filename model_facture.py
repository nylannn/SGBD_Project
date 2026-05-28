################################################################################
##
# @file model_facture.py
# @brief Modèle SQLAlchemy pour la table FACTURE
#
# @details
# Définit la classe Facture et sa relation vers Patient.
# Une facture est toujours adressée à un patient.
#
# **Projet:** Projet SGBD - Centre Médical
# **Formation:** Polytech Tours
# **Auteur:** Leo NOUHOUANG - Mohamed Yassine BEN ABDA
# **Date:** Mai 2026
#
################################################################################

# Importation de la base déclarative partagée
from base import Base

from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship

class Facture(Base):
    # Nom physique de la table en base de données
    __tablename__ = "facture"

    id = Column(Integer, primary_key=True, autoincrement=True) # Clé primaire auto-incrémentée
    montant = Column(Float, nullable=False) # Montant de la facture, obligatoire
    date = Column(Date, nullable=False) # Date d'émission, obligatoire
    statut = Column(String(50), nullable=False) # Statut : payée, en attente, etc.
    id_patient = Column(Integer, ForeignKey("patient.id"), nullable=False)    # Clé étrangère vers PATIENT

    # Relation vers le patient à qui est adressée cette facture
    patient = relationship("Patient", back_populates="factures")