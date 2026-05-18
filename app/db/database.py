import os
from databases import Database
from dotenv import load_dotenv

# chargement automatique du fichier .env

load_dotenv()

# Lit DATABASE_URL depuis l'environnement

DATABASE_URL = os.getenv("DATABASE_URL")

# Creer l'object de connnection a la base de donnee (pas encore connectee ici)

database = Database(DATABASE_URL)

