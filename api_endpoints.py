# Fichier : api_endpoints.py
# Description : API REST FastAPI pour ton comparateur (produits, annonceurs, clics, favoris...)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db_transactions import (
    get_produits_visibles,
    get_annonceurs_actifs,
    get_produit_by_id,
    api_export_produit,
)
from typing import List
import uvicorn

app = FastAPI(title="Comparateur API", version="1.0.0")

# ⚙️ Autoriser les requêtes cross-domain (pratique pour tests navigateur/mobile)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre plus tard si besoin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Route GET /produits (produits visibles, triés par score)
@app.get("/produits")
def route_produits():
    produits = get_produits_visibles(limit=100)
    return {"status": "ok", "resultats": [api_export_produit(p.id) for p in produits]}

# ✅ Route GET /produit/{id}
@app.get("/produit/{produit_id}")
def route_produit_detail(produit_id: int):
    produit = api_export_produit(produit_id)
    if not produit:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return {"status": "ok", "produit": produit}

# ✅ Route GET /annonceurs
@app.get("/annonceurs")
def route_annonceurs():
    annonceurs = get_annonceurs_actifs()
    return {"status": "ok", "annonceurs": [{"nom": a.nom, "commission": a.commission, "site": a.site} for a in annonceurs]}

# 📦 Lancer l’API avec Uvicorn (exécutable depuis Acode ou terminal)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)from fastapi import Request
from pydantic import BaseModel
from db_transactions import (
    enregistrer_clic,
    enregistrer_vue,
    ajouter_favori,
    retirer_favori,
    est_dans_favoris,
)

# Modèles de requête pour POST
class ClicRequest(BaseModel):
    produit_id: int
    utilisateur_id: Optional[int] = None

class VueRequest(BaseModel):
    produit_id: int
    user_agent: str
    referer: Optional[str] = ""

class FavoriRequest(BaseModel):
    utilisateur_id: int
    produit_id: int

# 🖱️ POST /clic — enregistre un clic
@app.post("/clic")
async def route_enregistrer_clic(data: ClicRequest, request: Request):
    ip = request.client.host
    enregistrer_clic(data.produit_id, data.utilisateur_id, ip)
    return {"status": "ok", "message": "Clic enregistré"}

# 👁️ POST /vue — enregistre une vue
@app.post("/vue")
async def route_enregistrer_vue(data: VueRequest):
    enregistrer_vue(data.produit_id, data.user_agent, data.referer)
    return {"status": "ok", "message": "Vue enregistrée"}

# ⭐ POST /favori — ajoute aux favoris
@app.post("/favori")
def route_ajouter_favori(data: FavoriRequest):
    ajouter_favori(data.utilisateur_id, data.produit_id)
    return {"status": "ok", "message": "Ajouté aux favoris"}

# ❌ DELETE /favori — retire des favoris
@app.delete("/favori")
def route_retirer_favori(data: FavoriRequest):
    retirer_favori(data.utilisateur_id, data.produit_id)
    return {"status": "ok", "message": "Retiré des favoris"}

# ✔️ GET /favori/{uid}/{pid} — vérifier si favori
@app.get("/favori/{utilisateur_id}/{produit_id}")
def route_verif_favori(utilisateur_id: int, produit_id: int):
    fav = est_dans_favoris(utilisateur_id, produit_id)
    return {"status": "ok", "favori": fav}from db_transactions import (
    rechercher_produits,
    get_clics_produit,
    get_vues_produit,
    calculer_epc,
    get_categories,
    get_favoris_utilisateur,
)

# 🔍 GET /recherche?q=mot
@app.get("/recherche")
def route_recherche(mot: str):
    produits = rechercher_produits(mot)
    return {
        "status": "ok",
        "terme": mot,
        "resultats": [api_export_produit(p.id) for p in produits],
    }

# 📊 GET /stats/{produit_id} — vues, clics, EPC
@app.get("/stats/{produit_id}")
def route_stats(produit_id: int):
    stats = {
        "vues": get_vues_produit(produit_id),
        "clics": get_clics_produit(produit_id),
        "epc": calculer_epc(produit_id),
    }
    return {"status": "ok", "stats": stats}

# 🧩 GET /categories
@app.get("/categories")
def route_categories():
    cats = get_categories()
    return {"status": "ok", "categories": cats}

# ⭐ GET /favoris/{utilisateur_id}
@app.get("/favoris/{utilisateur_id}")
def route_favoris(utilisateur_id: int):
    favoris = get_favoris_utilisateur(utilisateur_id)
    return {"status": "ok", "produits": favoris}from db_transactions import (
    verifier_connexion,
    creer_utilisateur,
    ajouter_log,
    ajouter_produit,
)
from fastapi import Body

# 📥 POST /auth/login — Vérifie connexion utilisateur
class LoginRequest(BaseModel):
    email: str
    mot_de_passe: str

@app.post("/auth/login")
def route_login(data: LoginRequest):
    uid = verifier_connexion(data.email, data.mot_de_passe)
    if uid:
        return {"status": "ok", "utilisateur_id": uid}
    return {"status": "error", "message": "Identifiants invalides"}

# 🧾 POST /auth/register — Création utilisateur
class RegisterRequest(BaseModel):
    nom: str
    email: str
    mot_de_passe: str

@app.post("/auth/register")
def route_register(data: RegisterRequest):
    u = creer_utilisateur(data.nom, data.email, data.mot_de_passe)
    if u:
        return {"status": "ok", "utilisateur_id": u.id}
    return {"status": "error", "message": "Création impossible"}

# ➕ POST /produit — Ajouter produit (simplifié)
@app.post("/produit")
def route_ajout_produit(prod: dict = Body(...)):
    new = ajouter_produit(prod)
    if new:
        return {"status": "ok", "produit_id": new.id}
    return {"status": "error", "message": "Erreur à l’ajout"}

# 🪵 POST /log — Ajout d’un log système API
class LogRequest(BaseModel):
    niveau: str
    message: str
    origine: str

@app.post("/log")
def route_log(data: LogRequest):
    ajouter_log(data.niveau, data.message, data.origine)
    return {"status": "ok", "message": "Log enregistré"}