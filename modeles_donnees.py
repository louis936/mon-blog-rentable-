# Fichier : modeles_donnees.py
# Description : Modèles de données SQLAlchemy pour annonceurs, produits, utilisateurs et interactions

from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    create_engine,
    Text,
    Enum,
    UniqueConstraint,
    Table,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional

Base = declarative_base()

# Type de compte utilisateur
class UserType(PyEnum):
    ADMIN = "admin"
    UTILISATEUR = "utilisateur"
    PARTENAIRE = "partenaire"

# Modèle Utilisateur
class Utilisateur(Base):
    __tablename__ = "utilisateurs"
    id = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    mot_de_passe = Column(String(256), nullable=False)
    type_utilisateur = Column(Enum(UserType), default=UserType.UTILISATEUR)
    date_creation = Column(DateTime, default=datetime.utcnow)
    actif = Column(Boolean, default=True)

    produits = relationship("Produit", back_populates="proprietaire")

# Modèle Annonceur
class Annonceur(Base):
    __tablename__ = "annonceurs"
    id = Column(Integer, primary_key=True)
    nom = Column(String(120), nullable=False, unique=True)
    pays = Column(String(5), default="FR")
    categorie = Column(String(100))
    commission = Column(Float)
    site = Column(String(300))
    actif = Column(Boolean, default=True)
    date_ajout = Column(DateTime, default=datetime.utcnow)

    produits = relationship("Produit", back_populates="annonceur_ref")

# Modèle Produit
class Produit(Base):
    __tablename__ = "produits"
    id = Column(Integer, primary_key=True)
    nom = Column(String(200), nullable=False)
    description = Column(Text)
    prix = Column(Float)
    url = Column(String(512))
    image = Column(String(512))
    epc = Column(Float, default=0.0)
    ctr = Column(Float, default=0.0)
    score = Column(Float, default=0.0)
    slug = Column(String(100), unique=True)
    date_publication = Column(DateTime, default=datetime.utcnow)

    annonceur_id = Column(Integer, ForeignKey("annonceurs.id"))
    annonceur_ref = relationship("Annonceur", back_populates="produits")

    user_id = Column(Integer, ForeignKey("utilisateurs.id"))
    proprietaire = relationship("Utilisateur", back_populates="produits")

    categorie = Column(String(100))
    visible = Column(Boolean, default=True)# Modèle : Historique des clics utilisateurs sur un produit
class ClicProduit(Base):
    __tablename__ = "clics_produit"
    id = Column(Integer, primary_key=True)
    produit_id = Column(Integer, ForeignKey("produits.id"))
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip = Column(String(45))

    produit = relationship("Produit")
    utilisateur = relationship("Utilisateur")

# Modèle : Vues produits
class VueProduit(Base):
    __tablename__ = "vues_produit"
    id = Column(Integer, primary_key=True)
    produit_id = Column(Integer, ForeignKey("produits.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_agent = Column(String(300))
    referer = Column(String(300))

# Modèle : Produit Favori (relation utilisateur ↔ produit)
class FavoriProduit(Base):
    __tablename__ = "favoris_produit"
    id = Column(Integer, primary_key=True)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id"))
    produit_id = Column(Integer, ForeignKey("produits.id"))
    date_ajout = Column(DateTime, default=datetime.utcnow)

    utilisateur = relationship("Utilisateur")
    produit = relationship("Produit")

# Modèle : Logs système et erreurs
class LogSysteme(Base):
    __tablename__ = "logs_systeme"
    id = Column(Integer, primary_key=True)
    niveau = Column(String(20))
    message = Column(Text)
    origine = Column(String(100))
    timestamp = Column(DateTime, default=datetime.utcnow)

# Modèle : Catégories produits (avec hiérarchie simple)
class Categorie(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    nom = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    sous_categories = relationship("Categorie", remote_side=[id])# Configuration de la base de données locale
DATABASE_URL = "sqlite:///database/comparateur.db"
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

# Création des tables si elles n’existent pas
def init_db():
    Base.metadata.create_all(bind=engine)

# Ajout conditionnel d’annonceurs partenaires (évite doublons)
def seed_annonceurs():
    from sqlalchemy.exc import IntegrityError
    session = SessionLocal()
    annonceurs_data = [
        {"nom": "Petit Bateau DE", "categorie": "Enfants", "commission": 0.06, "site": "https://www.petit-bateau.de", "pays": "DE"},
        {"nom": "Petit Bateau IT", "categorie": "Enfants", "commission": 0.05, "site": "https://www.petit-bateau.it", "pays": "IT"},
        {"nom": "Pierre et Vacances UK", "categorie": "Vacances", "commission": 0.06, "site": "https://www.pierreetvacances.co.uk", "pays": "UK"},
        {"nom": "Polène Paris Global", "categorie": "Sacs à main", "commission": 0.10, "site": "https://www.polene-paris.com", "pays": "GLOBAL"},
        {"nom": "Rimowa EU", "categorie": "Bagages", "commission": 0.08, "site": "https://www.rimowa.com", "pays": "EU"},
        {"nom": "Singulart", "categorie": "Art", "commission": 0.15, "site": "https://www.singulart.com", "pays": "GLOBAL"},
    ]
    for data in annonceurs_data:
        try:
            annonceur = Annonceur(**data)
            session.add(annonceur)
            session.commit()
        except IntegrityError:
            session.rollback()
    session.close()

# Initialisation complète à l’exécution
def initialiser_base():
    init_db()
    seed_annonceurs()

# Exécution directe si lancé seul
if __name__ == "__main__":
    initialiser_base()