document.addEventListener("DOMContentLoaded", () => {
  const API_BASE = "http://localhost:8000";

  const vedettesContainer = document.getElementById("vedettes-container");
  const nouvellesContainer = document.getElementById("nouvelles-container");

  // Fonction utilitaire pour créer une carte d’annonce
  function creerCarteAnnonce(produit) {
    const div = document.createElement("div");
    div.className = "catalogue-item";

    const image = document.createElement("img");
    image.src = produit.image || "https://via.placeholder.com/300x200?text=Sans+image";
    image.alt = produit.nom;
    image.className = "catalogue-image";
    div.appendChild(image);

    const infos = document.createElement("div");
    infos.className = "catalogue-infos";
    infos.innerHTML = `
      <h3>${produit.nom}</h3>
      <p><strong>Prix:</strong> ${produit.prix.toFixed(2)} €</p>
      <p><strong>Catégorie:</strong> ${produit.categorie}</p>
      <p><strong>Annonceur:</strong> ${produit.annonceur}</p>
      <p><a href="${produit.url || "#"}" target="_blank">🔗 Voir le produit</a></p>
    `;
    div.appendChild(infos);

    return div;
  }// Charger les annonces vedettes (par exemple : triées par prix croissant et limitées à 4)
  fetch(`${API_BASE}/catalogue/tri/prix`)
    .then(res => res.json())
    .then(data => {
      const vedettes = data.produits.slice(0, 4); // on affiche les 4 moins chers
      vedettes.forEach(p => {
        vedettesContainer.appendChild(creerCarteAnnonce(p));
      });
    })
    .catch(err => {
      vedettesContainer.innerHTML = "<p>Impossible de charger les annonces vedettes.</p>";
      console.error(err);
    });// Charger les annonces récentes (en les triant par date décroissante si l’API le permet)
  fetch(`${API_BASE}/catalogue/tri/recents`)
    .then(res => res.json())
    .then(data => {
      const recents = data.produits.slice(0, 6); // par exemple, les 6 plus récentes
      recents.forEach(p => {
        nouvellesContainer.appendChild(creerCarteAnnonce(p));
      });
    })
    .catch(err => {
      nouvellesContainer.innerHTML = "<p>Impossible de charger les nouvelles annonces.</p>";
      console.error(err);
    });// Fin du DOMContentLoaded
});