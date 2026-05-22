# Importation de declarative_base, create_engine et sessionmaker pour créer l'environnement de travail et la connexion avec la base de données
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

# Création de la classe de base dont héritent tous les modèles
Base = declarative_base()

# Création du moteur SQLite ; la base sera stockée dans le fichier centre_medical.db
engine = create_engine("sqlite:///centre_medical.db", echo=True)

# Activation de l'intégrité référentielle sur SQLite (désactivée par défaut)
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Exécution du PRAGMA pour activer les vérifications de clés étrangères
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Création d'une fabrique de sessions associée au moteur
Session = sessionmaker(bind=engine)

# Instanciation d'une session pour interagir avec la base de données
session = Session()