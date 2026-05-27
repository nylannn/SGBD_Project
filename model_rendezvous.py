################################################################################
##
# @file model_rendezvous.py
# @brief Modèle SQLAlchemy pour la table RENDEZVOUS
#
# @details
# Définit la classe RendezVous et ses relations vers
# Patient, Medecin et Etablissement.
#
# **Projet:** Projet SGBD - Centre Médical
# **Formation:** Polytech Tours
# **Auteur:** Leo NOUHOUANG
# **Date:** Mai 2026
#
################################################################################

# Importation de la base déclarative partagée
from base import Base

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class RendezVous(Base):
    # Nom physique de la table en base de données
    __tablename__ = "rendezvous"

    id = Column(Integer, primary_key=True, autoincrement=True) # Clé primaire auto-incrémentée
    date_heure = Column(DateTime, nullable=False) # Date et heure, obligatoire
    statut = Column(String(50), nullable=False) # Statut : planifié, annulé, effectué
    id_patient = Column(Integer, ForeignKey("patient.id"), nullable=False) # Clé étrangère vers PATIENT
    id_medecin = Column(Integer, ForeignKey("medecin.id"), nullable=False) # Clé étrangère vers MEDECIN
    id_etablissement = Column(Integer, ForeignKey("etablissement.id"), nullable=False) # Clé étrangère vers ETABLISSEMENT

    # Relation vers le patient concerné par ce rendez-vous
    patient = relationship("Patient", back_populates="rendezvous")
    # Relation vers le médecin qui assure ce rendez-vous
    medecin = relationship("Medecin", back_populates="rendezvous")
    # Relation vers l'établissement qui héberge ce rendez-vous
    etablissement = relationship("Etablissement", back_populates="rendezvous")