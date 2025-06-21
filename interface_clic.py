# Fichier : interface_cli.py
# Description : Interface ligne de commande pour interagir avec le projet

import argparse
from db_transactions import (
    get_produits_visibles,
    get_annonceurs_actifs,
    rechercher_produits,
    get_clics_produit,
    get_vues_produit,
    calculer_epc,
    api_export_produit,
)

def lister_produits(limit: int = 10):
    produits = get_produits_visibles(limit=limit)
    print(f"🛒 {len(produits)} produit(s) visibles :")
    for p in produits:
        d = api_export_produit(p.id)
        print(f"- {d['produit']['nom']} ({d['produit']['prix']}€) | Score : {d['produit']['score']}")

def lister_annonceurs():
    annonceurs = get_annonceurs_actifs()
    print(f"📢 {len(annonceurs)} annonceur(s) actif(s) :")
    for a in annonceurs:
        print(f"- {a.nom} ({a.categorie}) — {a.commission*100:.1f}%")

def recherche_produit(mot: str):
    produits = rechercher_produits(mot)
    print(f"🔎 Résultats pour '{mot}' : {len(produits)} produit(s)")
    for p in produits:
        print(f"- {p.nom} ({p.prix} €) — Catégorie : {p.categorie}")

def stats_produit(produit_id: int):
    clics = get_clics_produit(produit_id)
    vues = get_vues_produit(produit_id)
    epc = calculer_epc(produit_id)
    print(f"📊 Stats produit ID {produit_id} :")
    print(f"- Vues : {vues}")
    print(f"- Clics : {clics}")
    print(f"- EPC estimé : {epc:.4f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interface CLI — Comparateur Premium")
    subparsers = parser.add_subparsers(dest="commande")

    # Commande : lister produits
    parser_produits = subparsers.add_parser("liste-produits")
    parser_produits.add_argument("--limit", type=int, default=10)

    # Commande : lister annonceurs
    subparsers.add_parser("liste-annonceurs")

    # Commande : recherche
    parser_recherche = subparsers.add_parser("recherche")
    parser_recherche.add_argument("mot")

    # Commande : stats produit
    parser_stats = subparsers.add_parser("stats")
    parser_stats.add_argument("produit_id", type=int)

    args = parser.parse_args()

    if args.commande == "liste-produits":
        lister_produits(limit=args.limit)
    elif args.commande == "liste-annonceurs":
        lister_annonceurs()
    elif args.commande == "recherche":
        recherche_produit(args.mot)
    elif args.commande == "stats":
        stats_produit(args.produit_id)
    else:
        parser.print_help()from db_transactions import (
    enregistrer_clic,
    enregistrer_vue,
    ajouter_produit,
    ajouter_favori,
    retirer_favori,
)

def enregistrer_clic_cli(produit_id: int, utilisateur_id: int = None):
    ip = "127.0.0.1"
    enregistrer_clic(produit_id, utilisateur_id, ip)
    print(f"🖱️ Clic enregistré pour produit {produit_id}")

def enregistrer_vue_cli(produit_id: int):
    enregistrer_vue(produit_id, "CLI-Agent", "cli://interface")
    print(f"👁️ Vue enregistrée pour produit {produit_id}")

def ajouter_produit_cli():
    nom = input("Nom du produit : ")
    prix = float(input("Prix (€) : "))
    description = input("Description : ")
    categorie = input("Catégorie : ")
    annonceur_id = int(input("ID annonceur : "))
    url = input("URL : ")
    image = input("Image URL : ")
    data = {
        "nom": nom,
        "prix": prix,
        "description": description,
        "categorie": categorie,
        "annonceur_id": annonceur_id,
        "url": url,
        "image": image,
        "score": 0.0,
    }
    p = ajouter_produit(data)
    if p:
        print(f"✅ Produit ajouté avec ID {p.id}")
    else:
        print("❌ Erreur lors de l’ajout")

def test_favori(utilisateur_id: int, produit_id: int):
    ajouter_favori(utilisateur_id, produit_id)
    print(f"⭐ Favori ajouté pour utilisateur {utilisateur_id} - produit {produit_id}")
    retirer_favori(utilisateur_id, produit_id)
    print(f"🗑 Favori retiré pour utilisateur {utilisateur_id} - produit {produit_id}")# 📥 Commande : clic
parser_clic = subparsers.add_parser("clic")
parser_clic.add_argument("--produit", type=int, required=True)
parser_clic.add_argument("--utilisateur", type=int, default=None)

# 👁 Commande : vue
parser_vue = subparsers.add_parser("vue")
parser_vue.add_argument("--produit", type=int, required=True)

# ➕ Commande : ajout-produit
subparsers.add_parser("ajout-produit")

# ⭐ Commande : test-favori
parser_fav = subparsers.add_parser("test-favori")
parser_fav.add_argument("--utilisateur", type=int, required=True)
parser_fav.add_argument("--produit", type=int, required=True)

# 🔀 Dispatcher des nouvelles commandes
elif args.commande == "clic":
    enregistrer_clic_cli(args.produit, args.utilisateur)
elif args.commande == "vue":
    enregistrer_vue_cli(args.produit)
elif args.commande == "ajout-produit":
    ajouter_produit_cli()
elif args.commande == "test-favori":
    test_favori(args.utilisateur, args.produit)