// script.js — Gère l’affichage des produits et la recherche dynamique

const API_URL = "http://localhost:8000";

// ⚙️ Fonction appelée au chargement de la page
window.onload = () => {
  chargerProduits();
};

// 🔄 Charge les produits depuis l’API et les insère dans la page
function chargerProduits() {
  fetch(`${API_URL}/produits`)
    .then((res) => res.json())
    .then((data) => {
      const section = document.getElementById("liste-produits");
      section.innerHTML = "";
      data.resultats.forEach((item) => {
        const card = document.createElement("div");
        card.className = "produit";
        card.innerHTML = `
          <img src="${item.produit.image}" alt="${item.produit.nom}" />
          <h3>${item.produit.nom}</h3>
          <p>${item.produit.description}</p>
          <p><strong>${item.produit.prix} €</strong></p>
          <a href="produit.html?id=${item.produit_id}">Voir produit</a>
        `;
        section.appendChild(card);
      });
    })
    .catch((err) => {
      document.getElementById("liste-produits").innerHTML = "❌ Erreur lors du chargement.";
      console.error(err);
    });
}

// 🔍 Gère la recherche par mot-clé
function rechercher() {
  const mot = document.getElementById("champ-recherche").value.trim();
  if (!mot) return;
  fetch(`${API_URL}/recherche?mot=${encodeURIComponent(mot)}`)
    .then((res) => res.json())
    .then((data) => {
      const section = document.getElementById("liste-produits");
      section.innerHTML = `<h2>Résultats pour "${data.terme}"</h2>`;
      data.resultats.forEach((item) => {
        const card = document.createElement("div");
        card.className = "produit";
        card.innerHTML = `
          <img src="${item.produit.image}" alt="${item.produit.nom}" />
          <h3>${item.produit.nom}</h3>
          <p>${item.produit.description}</p>
          <p><strong>${item.produit.prix} €</strong></p>
          <a href="produit.html?id=${item.produit_id}">Voir produit</a>
        `;
        section.appendChild(card);
      });
    })
    .catch((err) => {
      document.getElementById("liste-produits").innerHTML = "❌ Erreur de recherche.";
      console.error(err);
    });
}