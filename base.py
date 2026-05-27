################################################################################
##
# @file base.py
# @brief Initialisation du moteur SQLAlchemy, de la session et de la base déclarative
#        Version SQLite pour tests
#
# @details
# Ce module est importé par tous les modèles et tous les scripts.
# Il centralise la connexion à la base de données SQLite du centre médical.
#
# **Projet:** Projet SGBD - Centre Médical
# **Formation:** Polytech Tours
# **Auteur:** Leo NOUHOUANG - Mohamed Yassine BEN ABDA
# **Date:** Mai 2026
#
################################################################################

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

# PARAMETRES DE CONNEXION (SQLite)

# Nom du fichier de base de données SQLite
S_DB_NAME = "centre_medical.db"

# Connexion SQLite (fichier local)
S_DB_URL = f"sqlite:///{S_DB_NAME}"

if os.path.exists(S_DB_NAME):
    os.remove(S_DB_NAME)


# Moteur de connexion vers la base cible
engine = create_engine(S_DB_URL, echo=False, future=True)

# Activation des clés étrangères à chaque connexion (SQLite)
event.listen(engine, "connect",
    lambda dbapi_conn, conn_record: dbapi_conn.execute("PRAGMA foreign_keys=1"))

# Vérification de la connexion au démarrage
try:
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        result.scalar()
    print("[OK] Connexion réussie à SQLite.")
except Exception as e:
    print(f"[ECHEC] Connexion impossible : {e}")


Base = declarative_base()
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
session = Session()