document.addEventListener("DOMContentLoaded", () => {
  const API_BASE = "http://localhost:8000";

  const formFiltre = document.getElementById("filtre-form");
  const produitsList = document.getElementById("produits-list");
  const template = document.getElementById("produit-catalogue-template");
  const catalogueMessage = document.getElementById("catalogue-message");

  const categorieSelect = document.getElementById("categorie-select");
  const annonceurSelect = document.getElementById("annonceur-select");

  // Charger catégories
  fetch(`${API_BASE}/categories`)
    .then((res) => res.json())
    .then((data) => {
      data.categories.forEach((cat) => {
        const option = document.createElement("option");
        option.value = cat;
        option.textContent = cat;
        categorieSelect.appendChild(option);
      });
    });

  // Charger annonceurs
  fetch(`${API_BASE}/annonceurs`)
    .then((res) => res.json())
    .then((data) => {
      data.annonceurs.forEach((a) => {
        const option = document.createElement("option");
        option.value = a;
        option.textContent = a;
        annonceurSelect.appendChild(option);
      });
    });// Fonction pour afficher un produit dans le DOM
  function afficherProduit(produit) {
    const clone = template.content.cloneNode(true);
    clone.querySelector(".catalogue-nom").textContent = produit.nom;
    clone.querySelector(".catalogue-prix").textContent = produit.prix.toFixed(2);
    clone.querySelector(".catalogue-categorie").textContent = produit.categorie;
    clone.querySelector(".catalogue-annonceur").textContent = produit.annonceur;

    const url = clone.querySelector(".catalogue-url");
    if (produit.url) {
      url.href = produit.url;
      url.textContent = "🔗 Voir le produit";
    } else {
      url.href = "#";
      url.textContent = "—";
    }

    const img = clone.querySelector(".catalogue-image");
    img.src = produit.image || "https://via.placeholder.com/300x200?text=Sans+image";
    img.alt = produit.nom;

    produitsList.appendChild(clone);
  }

  // Affichage initial de tous les produits triés par nom
  fetch(`${API_BASE}/catalogue/tri/nom`)
    .then((res) => res.json())
    .then((data) => {
      produitsList.innerHTML = "";
      data.produits.forEach(afficherProduit);
    });// Gestion du formulaire de recherche avec filtres
  formFiltre.addEventListener("submit", (e) => {
    e.preventDefault();

    const motCle = document.getElementById("recherche-nom").value.trim();
    const categorie = categorieSelect.value;
    const annonceur = annonceurSelect.value;
    const minPrix = parseFloat(document.getElementById("min-prix").value) || 0;
    const maxPrix = parseFloat(document.getElementById("max-prix").value) || Number.MAX_VALUE;

    let url = `${API_BASE}/catalogue/recherche/avancee?mot_cle=${encodeURIComponent(motCle)}`;
    if (annonceur) {
      url += `&annonceur=${encodeURIComponent(annonceur)}`;
    }

    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        const filtres = data.resultats.filter((p) =>
          p.prix >= minPrix &&
          p.prix <= maxPrix &&
          (categorie ? p.categorie === categorie : true)
        );

        produitsList.innerHTML = "";
        if (filtres.length > 0) {
          filtres.forEach(afficherProduit);
          catalogueMessage.textContent = `${filtres.length} produit(s) trouvé(s)`;
        } else {
          catalogueMessage.textContent = "Aucun produit ne correspond à ces critères.";
        }
      })
      .catch((err) => {
        catalogueMessage.textContent = "Erreur lors du filtrage.";
        console.error(err);
      });
  });// (Optionnel) Rechargement automatique si les filtres sont modifiés sans soumettre
  ["recherche-nom", "categorie-select", "annonceur-select", "min-prix", "max-prix"].forEach((id) => {
    document.getElementById(id).addEventListener("change", () => {
      formFiltre.requestSubmit(); // Déclenche la soumission pour relancer la recherche
    });
  });
});// Fin du script — tous les événements sont maintenant actifs
// Tu peux ajouter ici d'autres options comme un tri personnalisé ou un système de pagination