# Importation de la base déclarative partagée
from base import Base

from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

class Utilisateur(Base):
    # Nom physique de la table en base de données
    __tablename__ = "utilisateur"

    id = Column(Integer, primary_key=True, autoincrement=True) # Clé primaire auto-incrémentée
    login = Column(String(100), nullable=False, unique=True) # Identifiant unique, obligatoire
    mot_de_passe = Column(String(255), nullable=False) # Mot de passe hashé, obligatoire
    role = Column(String(50),  nullable=False) # Rôle : Admin, Secretaire, MedecinUser
    medecin_id = Column(Integer, ForeignKey("medecin.id"), nullable=True) # Clé étrangère vers MEDECIN, nullable

    # Contrainte CHECK : le rôle doit appartenir à la liste des rôles autorisés
    __table_args__ = (
        CheckConstraint("role IN ('Admin', 'Secretaire', 'MedecinUser')", name="check_role"),
    )

    # Relation vers le médecin lié à ce compte (uniquement pour le rôle MedecinUser)
    medecin = relationship("Medecin", back_populates="utilisateur")