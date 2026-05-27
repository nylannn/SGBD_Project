################################################################################
##
# @file model_etablissement.py
# @brief Modèle SQLAlchemy pour la table ETABLISSEMENT
#
# @details
# Définit la classe Etablissement et ses relations vers
# MedecinEtablissement et RendezVous.
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

class Etablissement(Base):
    # Nom physique de la table en base de données
    __tablename__ = "etablissement"

    id = Column(Integer, primary_key=True, autoincrement=True) # Clé primaire
    nom = Column(String(100), nullable=False) # Nom de l'établissement
    type = Column(String(50), nullable=False) # Type
    adresse = Column(Text, nullable=False) # Adresse complète
    telephone = Column(String(20), nullable=True) # Numéro de téléphone, optionnel

    # Relation vers la table d'association (un établissement accueille plusieurs médecins)
    medecins = relationship("MedecinEtablissement", back_populates="etablissement")
    # Relation vers les rendez-vous hébergés dans cet établissement
    rendezvous = relationship("RendezVous", back_populates="etablissement")