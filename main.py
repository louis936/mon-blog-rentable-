from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4

app = FastAPI()

# CORS pour permettre au frontend d'accéder à l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# Modèles de données
# -----------------------

class Produit(BaseModel):
    id: str
    nom: str
    prix: float
    image: Optional[str]
    categorie: str
    annonceur: str
    url: Optional[str]

class Utilisateur(BaseModel):
    id: int
    nom: str
    email: str
    is_admin: bool

# -----------------------
# Base de données fictive
# -----------------------

produits: List[Produit] = [
    Produit(
        id=str(uuid4()),
        nom="Body coton bio",
        prix=19.90,
        image="https://via.placeholder.com/300x200?text=Petit+Bateau+DE",
        categorie="Enfants",
        annonceur="Petit Bateau DE",
        url="https://exemple.com/produit/body-bio"
    ),
    Produit(
        id=str(uuid4()),
        nom="Pyjama rayé doux",
        prix=24.99,
        image="https://via.placeholder.com/300x200?text=Petit+Bateau+IT",
        categorie="Enfants",
        annonceur="Petit Bateau IT",
        url="https://exemple.com/produit/pyjama-doux"
    ),
    Produit(
        id=str(uuid4()),
        nom="Séjour 7 nuits à la mer",
        prix=799.00,
        image="https://via.placeholder.com/300x200?text=Pierre+et+Vacances+UK",
        categorie="Vacances",
        annonceur="Pierre & Vacances UK",
        url="https://exemple.com/sejour/7nuits-mer"
    ),
    Produit(
        id=str(uuid4()),
        nom="Sac Numéro Un Mini",
        prix=350.00,
        image="https://via.placeholder.com/300x200?text=Polène+Paris+Global",
        categorie="Sacs à main",
        annonceur="Polène Paris Global",
        url="https://exemple.com/sac/numero-un-mini"
    )
]produits += [
    Produit(
        id=str(uuid4()),
        nom="Valise cabine Essential",
        prix=550.00,
        image="https://via.placeholder.com/300x200?text=Rimowa+EU",
        categorie="Bagages",
        annonceur="Rimowa EU",
        url="https://exemple.com/produit/valise-essential"
    ),
    Produit(
        id=str(uuid4()),
        nom="Peinture abstraite grand format",
        prix=1200.00,
        image="https://via.placeholder.com/300x200?text=Singulart",
        categorie="Art",
        annonceur="Singulart",
        url="https://exemple.com/produit/peinture-abstraite"
    ),
    Produit(
        id=str(uuid4()),
        nom="T-shirt rayures marines",
        prix=29.90,
        image="https://via.placeholder.com/300x200?text=Petit+Bateau+DE",
        categorie="Enfants",
        annonceur="Petit Bateau DE",
        url="https://exemple.com/produit/tshirt-marines"
    ),
    Produit(
        id=str(uuid4()),
        nom="Sac en cuir Polène",
        prix=410.00,
        image="https://via.placeholder.com/300x200?text=Polène+Paris+Global",
        categorie="Sacs à main",
        annonceur="Polène Paris Global",
        url="https://exemple.com/produit/sac-cuir"
    )
]

utilisateurs = {
    1: Utilisateur(id=1, nom="Admin", email="admin@example.com", is_admin=True)
}

# -----------------------
# Endpoints utilisateur
# -----------------------

@app.get("/utilisateur/{user_id}")
def get_utilisateur(user_id: int):
    user = utilisateurs.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return {"utilisateur": user}

# -----------------------
# Endpoints admin – produits
# -----------------------

@app.get("/admin/produits")
def get_produits():
    return {"produits": produits}@app.post("/admin/produit")
def ajouter_produit(produit: Produit):
    if not produit.id:
        produit.id = str(uuid4())
    produits.append(produit)
    return {"message": "Produit ajouté", "produit": produit}

@app.delete("/admin/produit/{produit_id}")
def supprimer_produit(produit_id: str):
    for p in produits:
        if p.id == produit_id:
            produits.remove(p)
            return {"message": "Produit supprimé"}
    raise HTTPException(status_code=404, detail="Produit non trouvé")

@app.put("/admin/produit/{produit_id}")
def modifier_produit(produit_id: str, nouveau: Produit):
    for i, p in enumerate(produits):
        if p.id == produit_id:
            produits[i] = nouveau
            return {"message": "Produit modifié", "produit": nouveau}
    raise HTTPException(status_code=404, detail="Produit non trouvé")

# -----------------------
# Endpoints publics
# -----------------------

@app.get("/catalogue")
def catalogue():
    return {"produits": produits}

@app.get("/catalogue/categorie/{nom_categorie}")
def produits_par_categorie(nom_categorie: str):
    filtres = [p for p in produits if p.categorie.lower() == nom_categorie.lower()]
    return {"produits": filtres}

@app.get("/catalogue/annonceur/{nom_annonceur}")
def produits_par_annonceur(nom_annonceur: str):
    filtres = [p for p in produits if p.annonceur.lower() == nom_annonceur.lower()]
    return {"produits": filtres}# -----------------------
# Filtrage avancé (optionnel)
# -----------------------

@app.get("/catalogue/recherche/")
def recherche_produits(
    categorie: Optional[str] = None,
    annonceur: Optional[str] = None,
    min_prix: Optional[float] = None,
    max_prix: Optional[float] = None
):
    resultat = produits
    if categorie:
        resultat = [p for p in resultat if p.categorie.lower() == categorie.lower()]
    if annonceur:
        resultat = [p for p in resultat if p.annonceur.lower() == annonceur.lower()]
    if min_prix:
        resultat = [p for p in resultat if p.prix >= min_prix]
    if max_prix:
        resultat = [p for p in resultat if p.prix <= max_prix]
    return {"produits": resultat}

# -----------------------
# Génération massive de produits factices pour atteindre 10 000 lignes
# -----------------------

noms_exemples = [
    "Chapeau de paille", "Tapisserie artisanale", "Valise aluminium",
    "Peinture moderne", "Ensemble été enfant", "Pyjama coton doux",
    "Sac bandoulière", "Tableau contemporain", "Box vacances nature",
    "Valise rigide", "Sac en tissu recyclé", "Séjour montagne",
    "Illustration encadrée", "T-shirt côtelé", "Cabas cuir", "Poster galerie"
]

annonceurs_exemples = [
    ("Petit Bateau DE", "Enfants"),
    ("Petit Bateau IT", "Enfants"),
    ("Pierre & Vacances UK", "Vacances"),
    ("Polène Paris Global", "Sacs à main"),
    ("Rimowa EU", "Bagages"),
    ("Singulart", "Art")
]

import random

for i in range(200):
    nom = random.choice(noms_exemples)
    annonceur, categorie = random.choice(annonceurs_exemples)
    produits.append(
        Produit(
            id=str(uuid4()),
            nom=f"{nom} {i+1}",
            prix=round(random.uniform(15.0, 1200.0), 2),
            image=f"https://via.placeholder.com/300x200?text={annonceur.replace(' ', '+')}",
            categorie=categorie,
            annonceur=annonceur,
            url=f"https://exemple.com/produit/{nom.lower().replace(' ', '-')}-{i+1}"
        )
    )# -----------------------
# Statistiques globales (bonus)
# -----------------------

@app.get("/stats")
def statistiques():
    total = len(produits)
    par_categorie = {}
    par_annonceur = {}

    for p in produits:
        par_categorie[p.categorie] = par_categorie.get(p.categorie, 0) + 1
        par_annonceur[p.annonceur] = par_annonceur.get(p.annonceur, 0) + 1

    return {
        "total_produits": total,
        "par_categorie": par_categorie,
        "par_annonceur": par_annonceur
    }

# -----------------------
# Page d'accueil (sanity check)
# -----------------------

@app.get("/")
def accueil():
    return {"message": "API FastAPI e-commerce opérationnelle 🎉"}

# -----------------------
# Produit par ID
# -----------------------

@app.get("/produit/{produit_id}")
def get_produit_id(produit_id: str):
    for p in produits:
        if p.id == produit_id:
            return {"produit": p}
    raise HTTPException(status_code=404, detail="Produit introuvable")# -----------------------
# Endpoint pour lister toutes les catégories uniques
# -----------------------

@app.get("/categories")
def get_categories():
    categories_uniques = list(set([p.categorie for p in produits]))
    return {"categories": sorted(categories_uniques)}

# -----------------------
# Endpoint pour lister tous les annonceurs uniques
# -----------------------

@app.get("/annonceurs")
def get_annonceurs():
    annonceurs_uniques = list(set([p.annonceur for p in produits]))
    return {"annonceurs": sorted(annonceurs_uniques)}

# -----------------------
# Endpoint pour compter le nombre de produits par annonceur
# -----------------------

@app.get("/stats/annonceurs")
def stats_par_annonceur():
    resultats = {}
    for produit in produits:
        if produit.annonceur in resultats:
            resultats[produit.annonceur] += 1
        else:
            resultats[produit.annonceur] = 1
    return {"repartition": resultats}

# -----------------------
# Endpoint pour compter le nombre de produits par catégorie
# -----------------------

@app.get("/stats/categories")
def stats_par_categorie():
    resultats = {}
    for produit in produits:
        if produit.categorie in resultats:
            resultats[produit.categorie] += 1
        else:
            resultats[produit.categorie] = 1
    return {"repartition": resultats}# -----------------------
# Endpoint de recherche par mot-clé (dans nom)
# -----------------------

@app.get("/catalogue/search/{mot_cle}")
def recherche_mot_cle(mot_cle: str):
    filtres = [p for p in produits if mot_cle.lower() in p.nom.lower()]
    return {"resultats": filtres}

# -----------------------
# Endpoint de mise à jour du prix d’un produit
# -----------------------

@app.patch("/admin/produit/{produit_id}/prix")
def maj_prix(produit_id: str, nouveau_prix: float):
    for produit in produits:
        if produit.id == produit_id:
            produit.prix = nouveau_prix
            return {"message": "Prix mis à jour", "produit": produit}
    raise HTTPException(status_code=404, detail="Produit introuvable")

# -----------------------
# Endpoint pour récupérer tous les produits d'une catégorie précise
# mais triés par prix croissant
# -----------------------

@app.get("/catalogue/categorie/{nom_categorie}/tri/prix")
def produits_par_categorie_tri(nom_categorie: str):
    tri = sorted(
        [p for p in produits if p.categorie.lower() == nom_categorie.lower()],
        key=lambda x: x.prix
    )
    return {"produits": tri}

# -----------------------
# Endpoint de test santé
# -----------------------

@app.get("/health")
def health_check():
    return {"status": "ok", "produits_actuels": len(produits)}# -----------------------
# Endpoint pour changer l’annonceur d’un produit
# -----------------------

@app.patch("/admin/produit/{produit_id}/annonceur")
def maj_annonceur(produit_id: str, nouvel_annonceur: str):
    for produit in produits:
        if produit.id == produit_id:
            produit.annonceur = nouvel_annonceur
            return {"message": "Annonceur mis à jour", "produit": produit}
    raise HTTPException(status_code=404, detail="Produit introuvable")

# -----------------------
# Endpoint pour changer la catégorie d’un produit
# -----------------------

@app.patch("/admin/produit/{produit_id}/categorie")
def maj_categorie(produit_id: str, nouvelle_categorie: str):
    for produit in produits:
        if produit.id == produit_id:
            produit.categorie = nouvelle_categorie
            return {"message": "Catégorie mise à jour", "produit": produit}
    raise HTTPException(status_code=404, detail="Produit introuvable")

# -----------------------
# Endpoint pour modifier le lien d’un produit
# -----------------------

@app.patch("/admin/produit/{produit_id}/url")
def maj_url(produit_id: str, nouvelle_url: str):
    for produit in produits:
        if produit.id == produit_id:
            produit.url = nouvelle_url
            return {"message": "Lien mis à jour", "produit": produit}
    raise HTTPException(status_code=404, detail="Produit introuvable")

# -----------------------
# Endpoint pour modifier l’image d’un produit
# -----------------------

@app.patch("/admin/produit/{produit_id}/image")
def maj_image(produit_id: str, nouvelle_image: str):
    for produit in produits:
        if produit.id == produit_id:
            produit.image = nouvelle_image
            return {"message": "Image mise à jour", "produit": produit}
    raise HTTPException(status_code=404, detail="Produit introuvable")# -----------------------
# Endpoint pour modifier le nom d’un produit
# -----------------------

@app.patch("/admin/produit/{produit_id}/nom")
def maj_nom(produit_id: str, nouveau_nom: str):
    for produit in produits:
        if produit.id == produit_id:
            produit.nom = nouveau_nom
            return {"message": "Nom mis à jour", "produit": produit}
    raise HTTPException(status_code=404, detail="Produit introuvable")

# -----------------------
# Endpoint pour rechercher un produit par nom exact
# -----------------------

@app.get("/produit/nom/{nom_exact}")
def recherche_par_nom(nom_exact: str):
    resultat = next((p for p in produits if p.nom.lower() == nom_exact.lower()), None)
    if resultat:
        return {"produit": resultat}
    raise HTTPException(status_code=404, detail="Produit introuvable")

# -----------------------
# Endpoint pour récupérer les N produits les plus chers
# -----------------------

@app.get("/catalogue/top_prix/{n}")
def top_produits_par_prix(n: int = 5):
    tries = sorted(produits, key=lambda x: x.prix, reverse=True)
    return {"top_produits": tries[:n]}

# -----------------------
# Endpoint pour supprimer tous les produits d’un annonceur
# -----------------------

@app.delete("/admin/annonceur/{nom_annonceur}")
def supprimer_tous_produits_annonceur(nom_annonceur: str):
    global produits
    produits = [p for p in produits if p.annonceur.lower() != nom_annonceur.lower()]
    return {"message": f"Produits de '{nom_annonceur}' supprimés"}# -----------------------
# Endpoint pour rechercher tous les produits dans un intervalle de prix
# -----------------------

@app.get("/catalogue/plage_prix")
def produits_dans_intervalle(min: float = 0.0, max: float = 1000.0):
    filtres = [p for p in produits if min <= p.prix <= max]
    return {"produits": filtres}

# -----------------------
# Endpoint pour cloner un produit par ID
# -----------------------

@app.post("/admin/produit/clone/{produit_id}")
def cloner_produit(produit_id: str):
    for produit in produits:
        if produit.id == produit_id:
            clone = Produit(
                id=str(uuid4()),
                nom=produit.nom + " (copie)",
                prix=produit.prix,
                image=produit.image,
                categorie=produit.categorie,
                annonceur=produit.annonceur,
                url=produit.url
            )
            produits.append(clone)
            return {"message": "Produit cloné", "produit": clone}
    raise HTTPException(status_code=404, detail="Produit non trouvé")

# -----------------------
# Endpoint pour retourner tous les produits triés par nom
# -----------------------

@app.get("/catalogue/tri/nom")
def tri_par_nom():
    return {"produits": sorted(produits, key=lambda x: x.nom.lower())}

# -----------------------
# Endpoint de recherche booléenne (mot clé + annonceur)
# -----------------------

@app.get("/catalogue/recherche/avancee")
def recherche_avancee(mot_cle: str, annonceur: Optional[str] = None):
    resultat = [p for p in produits if mot_cle.lower() in p.nom.lower()]
    if annonceur:
        resultat = [p for p in resultat if p.annonceur.lower() == annonceur.lower()]
    return {"resultats": resultat}# -----------------------
# Endpoint pour exporter tous les produits en JSON brut
# -----------------------

@app.get("/export/json")
def exporter_produits():
    return {"export": [p.dict() for p in produits]}

# -----------------------
# Endpoint pour renvoyer les 10 derniers produits ajoutés
# -----------------------

@app.get("/catalogue/derniers")
def derniers_produits():
    return {"produits": produits[-10:]}

# -----------------------
# Endpoint pour trier les produits d'une catégorie par prix décroissant
# -----------------------

@app.get("/catalogue/categorie/{categorie}/prix/desc")
def tri_descendant_par_prix(categorie: str):
    items = [p for p in produits if p.categorie.lower() == categorie.lower()]
    tries = sorted(items, key=lambda x: x.prix, reverse=True)
    return {"produits": tries}

# -----------------------
# Endpoint pour filtrer par multiple catégories
# -----------------------

@app.post("/catalogue/categorie/multiples")
def par_plusieurs_categories(categories: List[str]):
    filtrés = [p for p in produits if p.categorie in categories]
    return {"produits": filtrés}

# -----------------------
# Endpoint pour modifier tous les prix d’un annonceur (+% ou -%)
# -----------------------

@app.patch("/admin/annonceur/{nom_annonceur}/prix")
def ajuster_prix_annonceur(nom_annonceur: str, pourcentage: float):
    compteur = 0
    for p in produits:
        if p.annonceur.lower() == nom_annonceur.lower():
            p.prix += p.prix * (pourcentage / 100)
            compteur += 1
    return {"message": f"{compteur} produits mis à jour", "annonceur": nom_annonceur}# -----------------------
# Endpoint pour filtrer les produits d’un annonceur dans une fourchette de prix
# -----------------------

@app.get("/annonceur/{nom_annonceur}/prix")
def produits_annonceur_dans_plage(nom_annonceur: str, min: float = 0.0, max: float = 1000.0):
    filtres = [
        p for p in produits
        if p.annonceur.lower() == nom_annonceur.lower() and min <= p.prix <= max
    ]
    return {"produits": filtres}

# -----------------------
# Endpoint pour supprimer tous les produits d’une catégorie
# -----------------------

@app.delete("/admin/categorie/{nom_categorie}")
def supprimer_par_categorie(nom_categorie: str):
    global produits
    produits = [p for p in produits if p.categorie.lower() != nom_categorie.lower()]
    return {"message": f"Produits de la catégorie '{nom_categorie}' supprimés"}

# -----------------------
# Endpoint pour faire un mapping nom -> prix
# -----------------------

@app.get("/catalogue/prix/noms")
def map_nom_prix():
    return {"prix_par_produit": {p.nom: p.prix for p in produits}}

# -----------------------
# Endpoint pour retourner tous les produits dont le nom contient un chiffre
# -----------------------

import re

@app.get("/catalogue/nom/chiffres")
def produits_avec_chiffre():
    pattern = re.compile(r".*\d+.*")
    return {"produits": [p for p in produits if pattern.match(p.nom)]}

# -----------------------
# Endpoint pour générer un résumé des produits sous forme de texte
# -----------------------

@app.get("/resume/textuel")
def resume_textuel():
    lignes = [
        f"- {p.nom} ({p.categorie}) – {p.prix}€ chez {p.annonceur}"
        for p in produits[:50]
    ]
    return {"resume": "\n".join(lignes)}# -----------------------
# Endpoint pour calculer la moyenne des prix par catégorie
# -----------------------

@app.get("/stats/prix/moyenne/categories")
def moyenne_par_categorie():
    stats = {}
    for p in produits:
        stats.setdefault(p.categorie, []).append(p.prix)

    moyennes = {cat: round(sum(prix) / len(prix), 2) for cat, prix in stats.items()}
    return {"moyenne_par_categorie": moyennes}

# -----------------------
# Endpoint pour calculer la moyenne des prix par annonceur
# -----------------------

@app.get("/stats/prix/moyenne/annonceurs")
def moyenne_par_annonceur():
    stats = {}
    for p in produits:
        stats.setdefault(p.annonceur, []).append(p.prix)

    moyennes = {ann: round(sum(prix) / len(prix), 2) for ann, prix in stats.items()}
    return {"moyenne_par_annonceur": moyennes}

# -----------------------
# Endpoint pour simuler une pagination simple
# -----------------------

@app.get("/catalogue/page/{page}")
def pagination(page: int = 1, taille: int = 20):
    debut = (page - 1) * taille
    fin = debut + taille
    total = len(produits)
    pages = (total // taille) + (1 if total % taille else 0)
    return {
        "page": page,
        "pages_totales": pages,
        "resultats": produits[debut:fin]
    }

# -----------------------
# Endpoint pour générer des statistiques sur les prix
# -----------------------

@app.get("/stats/prix")
def stats_prix():
    prix = [p.prix for p in produits]
    return {
        "min": min(prix),
        "max": max(prix),
        "moyenne": round(sum(prix)/len(prix), 2)
    }# -----------------------
# Endpoint pour regrouper les produits par annonceur (avec liste)
# -----------------------

@app.get("/groupes/annonceurs")
def groupes_par_annonceur():
    groupes = {}
    for p in produits:
        groupes.setdefault(p.annonceur, []).append(p)
    return {"groupes_par_annonceur": groupes}

# -----------------------
# Endpoint pour regrouper les produits par catégorie (avec liste)
# -----------------------

@app.get("/groupes/categories")
def groupes_par_categorie():
    groupes = {}
    for p in produits:
        groupes.setdefault(p.categorie, []).append(p)
    return {"groupes_par_categorie": groupes}

# -----------------------
# Endpoint pour renvoyer tous les produits triés par prix puis nom
# -----------------------

@app.get("/catalogue/tri/prix_nom")
def tri_prix_et_nom():
    tries = sorted(produits, key=lambda p: (p.prix, p.nom.lower()))
    return {"produits": tries}

# -----------------------
# Endpoint pour afficher le catalogue résumé (nom + prix seulement)
# -----------------------

@app.get("/catalogue/legers")
def produits_leger():
    resume = [{"nom": p.nom, "prix": p.prix} for p in produits]
    return {"resume_catalogue": resume}

# -----------------------
# Endpoint pour vérifier si un produit existe selon son nom
# -----------------------

@app.get("/produit/existe/{nom}")
def produit_existe(nom: str):
    existe = any(p.nom.lower() == nom.lower() for p in produits)
    return {"existe": existe}# -----------------------
# Endpoint pour retourner l’annonceur qui propose le plus de produits
# -----------------------

@app.get("/stats/annonceur/top")
def annonceur_le_plus_actif():
    compteur = {}
    for p in produits:
        compteur[p.annonceur] = compteur.get(p.annonceur, 0) + 1
    if not compteur:
        return {"annonceur": None}
    top = max(compteur.items(), key=lambda x: x[1])
    return {"annonceur": top[0], "produits": top[1]}

# -----------------------
# Endpoint pour retourner les catégories triées par nombre de produits
# -----------------------

@app.get("/stats/categories/tri")
def categories_par_volume():
    volume = {}
    for p in produits:
        volume[p.categorie] = volume.get(p.categorie, 0) + 1
    tries = sorted(volume.items(), key=lambda x: x[1], reverse=True)
    return {"classement_categories": tries}

# -----------------------
# Dernier petit endpoint fun
# -----------------------

@app.get("/easter-egg")
def easter_egg():
    return {
        "message": "Tu as trouvé l’œuf caché 🥚",
        "hint": "✨ Continue à coder avec passion, Louis ✨"
    }from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Si ce n’est pas déjà fait
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exemple de chargement depuis un fichier JSON local
def charger_produits():
    with open("data/produits.json", "r", encoding="utf-8") as f:
        return json.load(f)["produits"]

@app.get("/produit/{produit_id}")
def get_produit(produit_id: int):
    produits = charger_produits()
    for p in produits:
        if p["id"] == produit_id:
            return {"produit": p}
    raise HTTPException(status_code=404, detail="Produit introuvable")produits = [
    {
        "id": 1,
        "nom": "Valise cabine aluminium",
        "categorie": "Bagages",
        "prix": 429.00,
        "annonceur": "Rimowa",
        "image": "/images/produits/valise.jpg",
        "url": "https://www.cj.com/track/tonID/rimowa",
        "description": "Valise ultra résistante, cabine 35L.",
        "livraison": True,
        "stock": "En stock"
    },
    {
        "id": 2,
        "nom": "Sac Numéro Un",
        "categorie": "Sacs à main",
        "prix": 350.00,
        "annonceur": "Polène Paris",
        "image": "/images/produits/sac.jpg",
        "url": "https://www.cj.com/track/tonID/polene-paris",
        "description": "Sac iconique Polène, cuir italien.",
        "livraison": False,
        "stock": "Précommande"
    }
]