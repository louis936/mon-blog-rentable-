# Fichier : config_initialisation.py
# Description : Initialisation de l’environnement système, chargement dynamique, sécurité, intégration de la clé API, surveillance

import os
import sys
import json
import time
import base64
import hashlib
import logging
import socket
import signal
import uuid
import threading
import platform
import psutil
import pathlib
import warnings
import re
import locale
import configparser
import subprocess
import inspect
import shutil
import urllib.parse
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Optional, Dict, List

# Dossier racine du projet
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Chargement du fichier de configuration
CONFIG_PATH = os.path.join(ROOT_DIR, "settings.ini")
if not os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "w") as f:
        f.write("[general]\napi_key = 9UJdqflU6NsT0JW_z6bAqogATA\nlog_level = INFO\n")
CONFIG = configparser.ConfigParser()
CONFIG.read(CONFIG_PATH)

# Définir la clé API principale
API_KEY = CONFIG.get("general", "api_key", fallback="")

# Définition des constantes système
LOG_DIR = os.path.join(ROOT_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "system.log")
TEMP_DIR = os.path.join(ROOT_DIR, "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

# Configuration du logger principal
logging.basicConfig(
    filename=LOG_FILE,
    level=getattr(logging, CONFIG.get("general", "log_level", fallback="INFO")),
    format="%(asctime)s — %(levelname)s — %(message)s",
)
logger = logging.getLogger(__name__)

# Détection de l’environnement d’exécution
ENV_OS = platform.system()
ARCHITECTURE = platform.architecture()[0]
PYTHON_VERSION = platform.python_version()
ENCODING = locale.getpreferredencoding()
logger.info(f"Environnement détecté : OS={ENV_OS}, Arch={ARCHITECTURE}, Python={PYTHON_VERSION}")

# Contrôle de disponibilité réseau
def is_connected():
    try:
        socket.create_connection(("1.1.1.1", 53), 2)
        return True
    except OSError:
        return False

NETWORK_AVAILABLE = is_connected()
logger.info(f"Connexion internet active : {NETWORK_AVAILABLE}")

# Décorateur de sécurité pour fonction critique
def secured(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.debug(f"Exécution sécurisée de : {func.__name__}")
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Erreur dans {func.__name__} : {str(e)}", exc_info=True)
            return None
    return wrapper

# Générateur d'identifiants uniques
@secured
def generate_unique_id(prefix: str = "CMP") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12].upper()}"

# Chargement dynamique des modules nécessaires
@secured
def dynamic_import(module_name: str) -> Any:
    try:
        return __import__(module_name)
    except ImportError:
        logger.warning(f"Module manquant : {module_name}")
        return None

# Surveillance des ressources système
@secured
def system_monitor(interval: int = 15):
    def monitor():
        while True:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            logger.debug(f"Surveillance — CPU: {cpu}%, RAM: {ram}%")
            time.sleep(interval)
    thread = threading.Thread(target=monitor, daemon=True)
    thread.start()

system_monitor()# Validation du système et détection d’anomalies critiques
@secured
def check_system_health():
    issues = []
    if not NETWORK_AVAILABLE:
        issues.append("Connexion internet absente")
    if psutil.cpu_count() < 2:
        issues.append("Nombre de cœurs CPU insuffisant")
    if psutil.virtual_memory().total < 1 * 1024**3:
        issues.append("RAM disponible inférieure à 1 Go")
    if not os.access(ROOT_DIR, os.W_OK):
        issues.append("Accès en écriture au dossier racine refusé")
    return issues

SYSTEM_ISSUES = check_system_health()
if SYSTEM_ISSUES:
    for issue in SYSTEM_ISSUES:
        logger.warning(f"Problème système détecté : {issue}")
else:
    logger.info("Système validé — aucun problème critique détecté")

# Cache de pré-démarrage
CACHE_DIR = os.path.join(ROOT_DIR, "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

def load_cache_entry(key: str) -> Optional[str]:
    path = os.path.join(CACHE_DIR, f"{key}.cache")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return None

def save_cache_entry(key: str, data: str):
    path = os.path.join(CACHE_DIR, f"{key}.cache")
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)

# Vérification de fichiers nécessaires
REQUIRED_FOLDERS = ["templates", "public", "database", "modules"]
for folder in REQUIRED_FOLDERS:
    full_path = os.path.join(ROOT_DIR, folder)
    os.makedirs(full_path, exist_ok=True)
    logger.debug(f"Dossier vérifié ou créé : {full_path}")

# Sécurisation de la clé API
def hash_api_key(api_key: str) -> str:
    hashed = hashlib.sha256(api_key.encode()).hexdigest()
    logger.debug("Clé API hachée pour sécurisation")
    return hashed

API_KEY_HASHED = hash_api_key(API_KEY)

# Fonction de configuration globale
@secured
def bootstrap_config():
    global CONFIG_READY, LAUNCH_TOKEN
    CONFIG_READY = False
    LAUNCH_TOKEN = generate_unique_id("BOOT")
    logger.info(f"Lancement du système avec token {LAUNCH_TOKEN}")
    CONFIG_READY = True
    return True

bootstrap_config()

# Génération automatique de fichiers par défaut (si absents)
DEFAULT_TEMPLATE = "<html><head><title>Comparateur</title></head><body>{{ content }}</body></html>"
TEMPLATE_FILE = os.path.join(ROOT_DIR, "templates", "default.html")
if not os.path.exists(TEMPLATE_FILE):
    with open(TEMPLATE_FILE, "w", encoding="utf-8") as f:
        f.write(DEFAULT_TEMPLATE)
    logger.info("Template HTML par défaut généré automatiquement")# Détection automatique d’un port disponible pour le backend
@secured
def find_available_port(default_port: int = 8000, max_offset: int = 25) -> int:
    for offset in range(max_offset):
        port = default_port + offset
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                logger.info(f"Port {port} détecté comme disponible")
                return port
            except OSError:
                continue
    logger.warning("Aucun port disponible dans la plage spécifiée, fallback sur le port par défaut")
    return default_port

# Port sur lequel démarrera le backend du comparateur
SERVER_PORT = find_available_port()
API_HOST = "0.0.0.0"
API_URL = f"http://{API_HOST}:{SERVER_PORT}"
logger.info(f"Adresse du serveur préparée : {API_URL}")

# Modes de déploiement : local, production, test
MODE = os.environ.get("APP_MODE", "local")
logger.info(f"Mode d’exécution : {MODE}")

# Signature de lancement initial
START_SIGNATURE = hashlib.md5(
    f"{API_KEY}_{datetime.utcnow().isoformat()}".encode()
).hexdigest()

# Préparation du module de routage HTML
@secured
def register_basic_routes():
    route_map = {
        "/": "index.html",
        "/legal": "legal_notice.html",
        "/contact": "contact_form.html",
    }
    for route, file in route_map.items():
        path = os.path.join(ROOT_DIR, "templates", file)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"<html><body><h1>{file.replace('.html','').capitalize()}</h1></body></html>")
            logger.debug(f"Route initiale générée : {route} → {file}")
    return route_map

ROUTES = register_basic_routes()

# Activation du mode surveillance système étendu
EXTENDED_MONITORING = os.environ.get("EXTENDED_MONITORING", "yes").lower() == "yes"
if EXTENDED_MONITORING:
    logger.info("Surveillance étendue activée")
    thread = threading.Thread(target=system_monitor, args=(10,), daemon=True)
    thread.start()

# Chargement du profil machine
MACHINE_PROFILE = {
    "uuid": str(uuid.uuid4()),
    "hostname": socket.gethostname(),
    "os": ENV_OS,
    "architecture": ARCHITECTURE,
    "python": PYTHON_VERSION,
    "encoding": ENCODING,
    "mode": MODE,
    "boot_token": LAUNCH_TOKEN,
}
logger.debug(f"Profil de la machine chargé : {MACHINE_PROFILE}")# Initialisation des modules dynamiques à charger plus tard
DYNAMIC_MODULES = [
    "modeles_donnees",
    "db_transactions",
    "api_endpoints",
    "interface_cli",
    "optimisation_finale",
]

@secured
def preload_dynamic_modules():
    results = {}
    for mod in DYNAMIC_MODULES:
        loaded = dynamic_import(mod)
        results[mod] = bool(loaded)
        logger.info(f"Préchargement du module {mod} : {'succès' if loaded else 'échec'}")
    return results

PRELOADED = preload_dynamic_modules()

# Chargement d’un environnement de test temporaire
TEST_ENV = os.environ.get("ENABLE_TEST_ENV", "false").lower() == "true"
if TEST_ENV:
    logger.info("Mode test activé : environnement temporaire prêt")
    TEMP_TEST_FILE = os.path.join(TEMP_DIR, "test_session.tmp")
    with open(TEMP_TEST_FILE, "w") as f:
        f.write("TestEnv=ACTIVE")

# Audit et traçabilité des appels critiques
AUDIT_LOG = os.path.join(LOG_DIR, "audit.log")

def log_audit(message: str):
    timestamp = datetime.utcnow().isoformat()
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} — AUDIT — {message}\n")

log_audit("Configuration initiale du comparateur terminée")

# Résumé global de démarrage
@secured
def display_boot_summary():
    logger.info("Résumé de lancement du projet comparateur premium :")
    logger.info(f"API_KEY_HASHED = {API_KEY_HASHED[:10]}****")
    logger.info(f"ENV_OS = {ENV_OS}")
    logger.info(f"BOOT_TOKEN = {LAUNCH_TOKEN}")
    logger.info(f"PORT = {SERVER_PORT}")
    logger.info(f"MODULES PRÉCHARGÉS = {list(PRELOADED.keys())}")
    logger.info("Initialisation complète ✅")

display_boot_summary()