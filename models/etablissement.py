# Importation de la base déclarative partagée
from base import Base
# Importation des types de colonnes nécessaires
from sqlalchemy import Column, Integer, String, Text
# Importation de relationship pour déclarer les liens vers d'autres modèles
from sqlalchemy.orm import relationship

class Etablissement(Base):
    # Nom physique de la table en base de données
    __tablename__ = "etablissement"

    id = Column(Integer, primary_key=True, autoincrement=True) # Clé primaire auto-incrémentée
    nom = Column(String(100), nullable=False) # Nom de l'établissement, obligatoire
    type = Column(String(50), nullable=False) # Type : clinique, antenne, etc.
    adresse = Column(Text, nullable=False) # Adresse complète, obligatoire
    telephone = Column(String(20), nullable=True) # Numéro de téléphone, optionnel

    # Relation vers la table d'association (un établissement accueille plusieurs médecins)
    medecins = relationship("MedecinEtablissement", back_populates="etablissement")
    # Relation vers les rendez-vous hébergés dans cet établissement
    rendezvous = relationship("RendezVous", back_populates="etablissement")