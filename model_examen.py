################################################################################
##
# @file model_examen.py
# @brief Modèle SQLAlchemy pour la table EXAMEN
#
# @details
# Définit la classe Examen et sa relation vers Patient.
# Un examen est toujours associé à un patient.
#
# **Projet:** Projet SGBD - Centre Médical
# **Formation:** Polytech Tours
# **Auteur:** Leo NOUHOUANG
# **Date:** Mai 2026
#
################################################################################

# Importation de la base déclarative partagée
from base import Base

from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship

class Examen(Base):
    # Nom physique de la table en base de données
    __tablename__ = "examen"

    id = Column(Integer, primary_key=True, autoincrement=True) # Clé primaire auto-incrémentée
    type_examen = Column(String(100), nullable=False) # Type de l'examen, obligatoire
    resultat = Column(Text, nullable=True) # Résultat de l'examen, optionnel
    date = Column(Date, nullable=False) # Date de l'examen, obligatoire
    id_patient = Column(Integer, ForeignKey("patient.id"), nullable=False)  # Clé étrangère vers PATIENT

    # Relation vers le patient qui passe cet examen
    patient = relationship("Patient", back_populates="examens")