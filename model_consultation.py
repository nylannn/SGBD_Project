# Importation de la base déclarative partagée
from base import Base

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Consultation(Base):
    # Nom physique de la table en base de données
    __tablename__ = "consultation"

    id = Column(Integer, primary_key=True, autoincrement=True) # Clé primaire auto-incrémentée
    date_consultation = Column(DateTime, nullable=False) # Date et heure, obligatoire
    motif = Column(String(255), nullable=True) # Motif, optionnel
    id_patient = Column(Integer, ForeignKey("patient.id"), nullable=False)  # Clé étrangère vers PATIENT
    id_medecin = Column(Integer, ForeignKey("medecin.id"), nullable=False)  # Clé étrangère vers MEDECIN

    # Relation vers le patient concerné par cette consultation
    patient = relationship("Patient", back_populates="consultations")
    # Relation vers le médecin qui réalise cette consultation
    medecin = relationship("Medecin", back_populates="consultations")
    # Relation vers les prescriptions issues de cette consultation
    prescriptions = relationship("Prescription", back_populates="consultation")