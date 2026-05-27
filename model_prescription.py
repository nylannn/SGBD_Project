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