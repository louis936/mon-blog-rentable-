// produit.js
document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const produitId = params.get("id");
  const API_BASE = "http://localhost:8000";

  const fiche = document.getElementById("fiche-produit");
  const comparaison = document.getElementById("comparaison-container");

  fetch(`${API_BASE}/produit/${produitId}`)
    .then(res => res.json())
    .then(data => {
      const p = data.produit;
      fiche.innerHTML = `
        <div class="catalogue-item">
          <img src="${p.image}" alt="${p.nom}" class="catalogue-image">
          <div class="catalogue-infos">
            <h2>${p.nom}</h2>
            <p><strong>Prix :</strong> ${p.prix.toFixed(2)} €</p>
            <p><strong>Catégorie :</strong> ${p.categorie}</p>
            <p><strong>Annonceur :</strong> ${p.annonceur}</p>
            <p><strong>Description :</strong> ${p.description || "—"}</p>
            <p><a href="${p.url}" target="_blank">🔗 Lien affilié</a></p>
          </div>
        </div>
      `;

      return fetch(`${API_BASE}/catalogue/filtrer?categorie=${p.categorie}`);
    })
    .then(res => res.json())
    .then(data => {
      const produits = data.produits
        .filter(p => p.id !== parseInt(produitId))
        .slice(0, 4);

      produits.forEach(pr => {
        const div = document.createElement("div");
        div.className = "catalogue-item";
        div.innerHTML = `
          <img src="${pr.image}" alt="${pr.nom}" class="catalogue-image">
          <div class="catalogue-infos">
            <h3>${pr.nom}</h3>
            <p><strong>Prix :</strong> ${pr.prix.toFixed(2)} €</p>
            <p><strong>Annonceur :</strong> ${pr.annonceur}</p>
            <p><a href="produit.html?id=${pr.id}">🔁 Voir fiche</a></p>
          </div>
        `;
        comparaison.appendChild(div);
      });

      // Comparatif par tableau
      if (produits.length) {
        const table = document.createElement("table");
        table.innerHTML = `
          <thead>
            <tr>
              <th>Produit</th>
              <th>Prix</th>
              <th>Livraison</th>
              <th>Annonceur</th>
              <th>Stock</th>
              <th>🔗</th>
            </tr>
          </thead>
          <tbody>
            ${produits.map(p => `
              <tr>
                <td>${p.nom}</td>
                <td>${p.prix.toFixed(2)} €</td>
                <td>${p.livraison ? "✅" : "❌"}</td>
                <td>${p.annonceur}</td>
                <td>${p.stock || "?"}</td>
                <td><a href="${p.url}" target="_blank">Voir</a></td>
              </tr>
            `).join("")}
          </tbody>
        `;
        comparaison.appendChild(table);
      }
    })
    .catch(err => {
      fiche.innerHTML = "<p>Erreur de chargement du produit</p>";
      console.error(err);
    });
});