# Fichier : utils_helpers.py
# Description : Fonctions utilitaires pour tout le projet comparateur (tri, formatage, scoring, manipulation de chaînes et dates)

import re
import os
import math
import json
import random
import string
import logging
import base64
import unicodedata
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Union, Any
from functools import wraps

logger = logging.getLogger(__name__)

# Nettoyage d’une chaîne en supprimant les caractères spéciaux
def clean_string(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^\w\s-]", "", text).strip().lower()

# Génère un identifiant alphanumérique court
def generate_slug(length: int = 12) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))

# Formatage d’un prix en euro
def format_price(value: Union[float, int]) -> str:
    return f"{value:,.2f} €".replace(",", " ").replace(".", ",")

# Arrondi intelligent selon le seuil
def round_up(value: float, threshold: float = 0.05) -> float:
    return math.ceil(value / threshold) * threshold

# Transformation d’une date ISO en format lisible
def human_date(date_str: str) -> str:
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%d/%m/%Y à %Hh%M")
    except:
        return date_str

# Calcul de durée lisible
def duration_since(date_str: str) -> str:
    try:
        past = datetime.fromisoformat(date_str)
        now = datetime.utcnow()
        delta = now - past
        if delta.days > 0:
            return f"il y a {delta.days} jour{'s' if delta.days > 1 else ''}"
        hours = delta.seconds // 3600
        return f"il y a {hours} heure{'s' if hours > 1 else ''}"
    except:
        return "date inconnue"

# Décorateur de mesure de temps
def timing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.utcnow()
        result = func(*args, **kwargs)
        elapsed = datetime.utcnow() - start
        logger.debug(f"Temps d’exécution de {func.__name__} : {elapsed.total_seconds():.3f} s")
        return result
    return wrapper

# Extraction du domaine depuis une URL
def get_domain(url: str) -> str:
    try:
        return re.search(r"https?://(?:www\.)?([^/]+)", url).group(1)
    except:
        return "domaine inconnu"

# Calcul du score de mise en avant d’un produit
def compute_product_score(commission: float, epc: float, ctr: float, base_weight: float = 1.0) -> float:
    # Pondération personnalisée pour ton comparateur
    return round((commission * 0.4 + epc * 0.3 + ctr * 0.3) * base_weight, 3)

# Normalisation d’un pourcentage
def normalize_percent(val: float) -> float:
    return max(0, min(100, round(val * 100, 2)))# Tri d’une liste de produits par score décroissant
def sort_by_score(products: List[Dict], score_field: str = "score") -> List[Dict]:
    return sorted(products, key=lambda x: x.get(score_field, 0), reverse=True)

# Filtrage par catégorie
def filter_by_category(products: List[Dict], category: str) -> List[Dict]:
    return [p for p in products if p.get("categorie", "").lower() == category.lower()]

# Générateur de mots-clés SEO à partir d’une description
def extract_keywords(text: str, min_length: int = 4) -> List[str]:
    words = re.findall(r"\b\w+\b", text.lower())
    stop_words = {"avec", "pour", "une", "des", "dans", "chez", "mais", "tres", "bien", "plus"}
    return list({w for w in words if len(w) >= min_length and w not in stop_words})

# Création d’une URL optimisée pour le SEO
def build_seo_url(product_name: str, category: str) -> str:
    slug = clean_string(product_name)
    category_slug = clean_string(category)
    return f"/{category_slug}/{slug}.html"

# Calcul du taux de clic moyen
def average_ctr(clicks: int, views: int) -> float:
    if views == 0:
        return 0.0
    return round(clicks / views * 100, 2)

# Générateur de titre marketing
def generate_ad_title(brand: str, product: str, discount: float) -> str:
    return f"{brand} - {product} à {discount:.0f}% de réduction"

# Normalisation des scores sur une base 100
def normalize_scores(products: List[Dict], field: str) -> List[Dict]:
    values = [p.get(field, 0) for p in products]
    max_val = max(values) if values else 1
    for product in products:
        product[f"{field}_normalized"] = round(product.get(field, 0) / max_val * 100, 2)
    return products

# Groupement des produits par annonceur
def group_by_annonceur(products: List[Dict]) -> Dict[str, List[Dict]]:
    result = {}
    for p in products:
        key = p.get("annonceur", "inconnu")
        result.setdefault(key, []).append(p)
    return result

# Fonction utilitaire : conversion string -> float sécurisée
def safe_float(value: Any) -> float:
    try:
        return float(str(value).replace(",", ".").strip())
    except:
        return 0.0

# Vérification des champs obligatoires d’un produit
def is_valid_product(product: Dict) -> bool:
    required = ["nom", "categorie", "prix", "commission", "annonceur"]
    return all(k in product and product[k] for k in required)# Conversion rapide d’un dictionnaire produit en résumé affichable
def product_summary(p: Dict) -> str:
    return f"{p.get('nom', 'Produit inconnu')} – {format_price(p.get('prix', 0))} ({p.get('categorie', 'non classé')})"

# Détection d’outliers dans une liste de prix
def detect_outliers(prices: List[float]) -> List[float]:
    if not prices:
        return []
    mean = sum(prices) / len(prices)
    std_dev = (sum((x - mean) ** 2 for x in prices) / len(prices)) ** 0.5
    return [x for x in prices if abs(x - mean) > 2 * std_dev]

# Décorateur pour logguer les entrées et sorties de fonction
def log_io(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"Entrée : {func.__name__} args={args} kwargs={kwargs}")
        result = func(*args, **kwargs)
        logger.debug(f"Sortie : {func.__name__} result={result}")
        return result
    return wrapper

# Générateur de score basé sur ancienneté + perf
@log_io
def compute_bonus_score(score: float, age_days: int, multiplier: float = 1.2) -> float:
    bonus = max(0.1, 1 + (30 - min(age_days, 30)) / 100)
    return round(score * bonus * multiplier, 3)

# Simulation aléatoire d’un produit “moyen”
def generate_mock_product(nom: str = "Produit", annonceur: str = "Générique") -> Dict:
    price = random.uniform(10, 1000)
    commission = round(random.uniform(0.05, 0.15), 2)
    epc = round(random.uniform(0.3, 2.5), 2)
    ctr = round(random.uniform(0.01, 0.15), 2)
    return {
        "nom": nom,
        "prix": round_up(price, 0.05),
        "commission": commission,
        "epc": epc,
        "ctr": ctr,
        "score": compute_product_score(commission, epc, ctr),
        "categorie": "Divers",
        "annonceur": annonceur,
    }

# Tri pondéré sur plusieurs critères
def multi_criteria_sort(products: List[Dict], weights: Dict[str, float]) -> List[Dict]:
    def get_weighted(p):
        total = 0
        for k, w in weights.items():
            total += p.get(k, 0) * w
        return total
    return sorted(products, key=get_weighted, reverse=True)

# Fonction de vérification de compatibilité produit
def is_comparable(p1: Dict, p2: Dict) -> bool:
    return p1.get("categorie") == p2.get("categorie") and abs(p1.get("prix", 0) - p2.get("prix", 0)) <= 50# Chargement sécurisé d’un fichier JSON
def load_json_file(path: str) -> Optional[dict]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"Erreur de lecture JSON : {path} — {e}")
        return None

# Sauvegarde d’un dictionnaire en fichier JSON
def save_json_file(data: dict, path: str):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Erreur de sauvegarde JSON : {path} — {e}")

# Encodage base64 d’un identifiant
def encode_id(identifier: str) -> str:
    return base64.urlsafe_b64encode(identifier.encode()).decode()

# Décodage base64 d’un identifiant
def decode_id(encoded: str) -> str:
    try:
        return base64.urlsafe_b64decode(encoded.encode()).decode()
    except:
        return ""

# Calcul rapide de la moyenne
def quick_average(values: List[float]) -> float:
    return round(sum(values) / len(values), 2) if values else 0.0

# Mini gestionnaire de session par token (non sécurisé)
SESSION_STORE = {}

def store_session(token: str, payload: dict, ttl: int = 180):
    expiry = datetime.utcnow() + timedelta(seconds=ttl)
    SESSION_STORE[token] = {"payload": payload, "expires": expiry}

def get_session(token: str) -> Optional[dict]:
    session = SESSION_STORE.get(token)
    if session and session["expires"] > datetime.utcnow():
        return session["payload"]
    return None

# Nettoyage des sessions expirées
def cleanup_sessions():
    now = datetime.utcnow()
    keys_to_remove = [k for k, v in SESSION_STORE.items() if v["expires"] <= now]
    for k in keys_to_remove:
        del SESSION_STORE[k]
    logger.debug(f"Sessions nettoyées : {len(keys_to_remove)} supprimées")