# Fichier : db_transactions.py
# Description : Fonctions de lecture/écriture dans la base (annonceurs, produits, vues, clics, etc.)

from modeles_donnees import (
    SessionLocal,
    Annonceur,
    Produit,
    Utilisateur,
    ClicProduit,
    VueProduit,
    FavoriProduit,
    LogSysteme,
    Categorie,
)
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from datetime import datetime
from typing import List, Optional, Dict

# Ouverture de session
def get_session():
    return SessionLocal()

# 🔍 Récupération des annonceurs actifs
def get_annonceurs_actifs() -> List[Annonceur]:
    session = get_session()
    annonceurs = session.query(Annonceur).filter(Annonceur.actif == True).all()
    session.close()
    return annonceurs

# 🔎 Récupération de tous les produits visibles
def get_produits_visibles(limit: int = 100) -> List[Produit]:
    session = get_session()
    produits = (
        session.query(Produit)
        .filter(Produit.visible == True)
        .order_by(Produit.score.desc(), Produit.date_publication.desc())
        .limit(limit)
        .all()
    )
    session.close()
    return produits

# 🔎 Récupération d’un produit par ID
def get_produit_by_id(prod_id: int) -> Optional[Produit]:
    session = get_session()
    produit = session.query(Produit).filter(Produit.id == prod_id).first()
    session.close()
    return produit

# 🔎 Recherche de produits par mot-clé (dans le nom ou la description)
def rechercher_produits(mot_cle: str, limit: int = 50) -> List[Produit]:
    session = get_session()
    pattern = f"%{mot_cle.lower()}%"
    produits = (
        session.query(Produit)
        .filter(
            Produit.visible == True,
            func.lower(Produit.nom).like(pattern) | func.lower(Produit.description).like(pattern)
        )
        .limit(limit)
        .all()
    )
    session.close()
    return produits

# 🔎 Récupération des produits d’un annonceur donné
def get_produits_par_annonceur(nom_annonceur: str) -> List[Produit]:
    session = get_session()
    produits = (
        session.query(Produit)
        .join(Annonceur)
        .filter(Annonceur.nom == nom_annonceur, Produit.visible == True)
        .order_by(Produit.score.desc())
        .all()
    )
    session.close()
    return produits

# 🔎 Récupération des catégories disponibles
def get_categories() -> List[str]:
    session = get_session()
    categories = session.query(Categorie.nom).all()
    session.close()
    return [c[0] for c in categories]# 🖱️ Enregistrement d’un clic sur un produit
def enregistrer_clic(produit_id: int, utilisateur_id: Optional[int], ip: str):
    session = get_session()
    clic = ClicProduit(
        produit_id=produit_id,
        utilisateur_id=utilisateur_id,
        ip=ip,
    )
    session.add(clic)
    session.commit()
    session.close()

# 👁️ Enregistrement d’une vue
def enregistrer_vue(produit_id: int, user_agent: str, referer: str = ""):
    session = get_session()
    vue = VueProduit(
        produit_id=produit_id,
        user_agent=user_agent[:300],
        referer=referer[:300],
    )
    session.add(vue)
    session.commit()
    session.close()

# ➕ Ajouter un produit manuellement
def ajouter_produit(data: Dict) -> Optional[Produit]:
    session = get_session()
    try:
        produit = Produit(**data)
        session.add(produit)
        session.commit()
        return produit
    except Exception as e:
        print(f"Erreur ajout produit : {e}")
        session.rollback()
        return None
    finally:
        session.close()

# ⭐ Ajouter aux favoris
def ajouter_favori(utilisateur_id: int, produit_id: int):
    session = get_session()
    favori = FavoriProduit(utilisateur_id=utilisateur_id, produit_id=produit_id)
    session.add(favori)
    session.commit()
    session.close()

# ❌ Retirer des favoris
def retirer_favori(utilisateur_id: int, produit_id: int):
    session = get_session()
    favori = session.query(FavoriProduit).filter_by(
        utilisateur_id=utilisateur_id,
        produit_id=produit_id
    ).first()
    if favori:
        session.delete(favori)
        session.commit()
    session.close()

# 📌 Vérifier si un produit est dans les favoris
def est_dans_favoris(utilisateur_id: int, produit_id: int) -> bool:
    session = get_session()
    favori = session.query(FavoriProduit).filter_by(
        utilisateur_id=utilisateur_id,
        produit_id=produit_id
    ).first()
    session.close()
    return favori is not None# 📊 Statistiques : total clics pour un produit
def get_clics_produit(produit_id: int) -> int:
    session = get_session()
    total = session.query(ClicProduit).filter_by(produit_id=produit_id).count()
    session.close()
    return total

# 📊 Statistiques : total vues pour un produit
def get_vues_produit(produit_id: int) -> int:
    session = get_session()
    total = session.query(VueProduit).filter_by(produit_id=produit_id).count()
    session.close()
    return total

# 📊 Estimation simple du EPC (gain par clic) pour un produit
def calculer_epc(produit_id: int, commission: float = 0.05) -> float:
    clics = get_clics_produit(produit_id)
    vues = get_vues_produit(produit_id)
    if clics == 0:
        return 0.0
    taux_conversion = clics / vues if vues else 0.1
    return round(commission * taux_conversion, 3)

# 📝 Enregistrer un log système
def ajouter_log(niveau: str, message: str, origine: str):
    session = get_session()
    log = LogSysteme(niveau=niveau, message=message, origine=origine)
    session.add(log)
    session.commit()
    session.close()

# 🛠️ Modifier la visibilité d’un produit
def activer_produit(produit_id: int, actif: bool = True):
    session = get_session()
    produit = session.query(Produit).filter_by(id=produit_id).first()
    if produit:
        produit.visible = actif
        session.commit()
    session.close()

# 🗑 Supprimer un produit
def supprimer_produit(produit_id: int):
    session = get_session()
    produit = session.query(Produit).filter_by(id=produit_id).first()
    if produit:
        session.delete(produit)
        session.commit()
    session.close()

# 📄 Export produit simplifié
def exporter_produit(produit_id: int) -> Optional[dict]:
    session = get_session()
    p = session.query(Produit).filter_by(id=produit_id).first()
    session.close()
    if not p:
        return None
    return {
        "nom": p.nom,
        "prix": p.prix,
        "description": p.description,
        "categorie": p.categorie,
        "url": p.url,
        "image": p.image,
        "score": p.score,
        "annonceur": p.annonceur_ref.nom if p.annonceur_ref else "",
    }# 🔐 Authentification basique par email/mot de passe (non chiffré ici)
def verifier_connexion(email: str, mot_de_passe: str) -> Optional[int]:
    session = get_session()
    user = session.query(Utilisateur).filter_by(email=email, mot_de_passe=mot_de_passe).first()
    session.close()
    return user.id if user else None

# 🔎 Récupérer un utilisateur par email
def get_utilisateur_par_email(email: str) -> Optional[Utilisateur]:
    session = get_session()
    user = session.query(Utilisateur).filter_by(email=email).first()
    session.close()
    return user

# 📥 Créer un nouvel utilisateur
def creer_utilisateur(nom: str, email: str, mot_de_passe: str) -> Optional[Utilisateur]:
    session = get_session()
    try:
        user = Utilisateur(nom=nom, email=email, mot_de_passe=mot_de_passe)
        session.add(user)
        session.commit()
        return user
    except:
        session.rollback()
        return None
    finally:
        session.close()

# 🛑 Désactiver un utilisateur
def desactiver_utilisateur(user_id: int):
    session = get_session()
    user = session.query(Utilisateur).filter_by(id=user_id).first()
    if user:
        user.actif = False
        session.commit()
    session.close()

# 🔍 Récupérer tous les produits favoris d’un utilisateur
def get_favoris_utilisateur(user_id: int) -> List[dict]:
    session = get_session()
    favoris = (
        session.query(FavoriProduit)
        .filter_by(utilisateur_id=user_id)
        .join(Produit)
        .options(joinedload(FavoriProduit.produit))
        .all()
    )
    session.close()
    return [exporter_produit(fav.produit_id) for fav in favoris if fav.produit_id]

# 📡 Simuler une réponse API JSON rapide (exemple export produit)
def api_export_produit(prod_id: int) -> dict:
    produit = exporter_produit(prod_id)
    if not produit:
        return {"status": "error", "message": "Produit introuvable"}
    return {"status": "ok", "produit": produit}