# Importation de declarative_base, create_engine et sessionmaker pour créer l'environnement de travail et la connexion avec la base de données
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from datetime import datetime, date

from sqlalchemy import create_engine, text

# 1. Bloc qui crée une base de donnée MySQL si elle n'existe pas
engine_init = create_engine("mysql+pymysql://userB24:motdepasseB5um6@dockerepu1.pedagogie.sandbox.univ-tours.fr:32769/")


db_name = "centre_medical"

with engine_init.connect() as conn:
    result = conn.execute(
        text("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = :db"), {"db": db_name}).fetchone()

    if result:
        print(f"La base de données '{db_name}' existe déjà.")
    else:
        conn.execute(text(f"CREATE DATABASE `{db_name}`"))
        print(f"Base de données '{db_name}' créée avec succès.")

# 2. Connexion avec la base cible
engine = create_engine(f"mysql+pymysql://userB24:motdepasseB5um6@dockerepu1.pedagogie.sandbox.univ-tours.fr:32769/{db_name}", echo=False)

# 3. verification de la connexion
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        print("Connexion réussie")
except Exception as e:
    print(f"Échec de la connexion : {e}")


### Création de la session
Session = sessionmaker(bind=engine)
session = Session()