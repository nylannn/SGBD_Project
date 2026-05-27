################################################################################
##
# @file model_prescription.py
# @brief Modèle SQLAlchemy pour la table PRESCRIPTION
#
# @details
# Définit la classe Prescription et sa relation vers Consultation.
# Une prescription est toujours issue d'une consultation.
#
# **Projet:** Projet SGBD - Centre Médical
# **Formation:** Polytech Tours
# **Auteur:** Leo NOUHOUANG
# **Date:** Mai 2026
#
################################################################################

# Importation de la base déclarative partagée
from base import Base

from sqlalchemy import Column, Integer, Date, Text, ForeignKey
from sqlalchemy.orm import relationship

class Prescription(Base):
    # Nom physique de la table en base de données
    __tablename__ = "prescription"

    id = Column(Integer, primary_key=True, autoincrement=True) # Clé primaire auto-incrémentée
    date = Column(Date, nullable=False) # Date de prescription, obligatoire
    description = Column(Text, nullable=True) # Détail des médicaments, optionnel
    id_consultation = Column(Integer, ForeignKey("consultation.id"), nullable=False)   # Clé étrangère vers CONSULTATION

    # Relation vers la consultation dont est issue cette prescription
    consultation = relationship("Consultation", back_populates="prescriptions")