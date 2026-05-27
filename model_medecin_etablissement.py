# Importation de la base déclarative partagée
from base import Base

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class MedecinEtablissement(Base):
    # Nom physique de la table d'association en base de données
    __tablename__ = "medecin_etablissement"

    id_medecin = Column(Integer, ForeignKey("medecin.id"), primary_key=True) # Clé étrangère vers la table MEDECIN, constitue la première partie de la clé primaire composite
    id_etablissement = Column(Integer, ForeignKey("etablissement.id"), primary_key=True) # Clé étrangère vers la table ETABLISSEMENT, constitue la seconde partie de la clé primaire composite

    medecin = relationship("Medecin", back_populates="etablissements")  # Relation vers le médecin associé à ce lien
    etablissement = relationship("Etablissement", back_populates="medecins") # Relation vers l'établissement associé à ce lien