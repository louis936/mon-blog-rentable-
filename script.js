document.addEventListener("DOMContentLoaded", () => {
  const API_BASE = "http://localhost:8000";

  const formAjout = document.getElementById("ajout-produit-form");
  const messageAjout = document.getElementById("message-ajout");
  const produitsContainer = document.getElementById("produits-container");
  const template = document.getElementById("produit-template");
  const messageActions = document.getElementById("message-actions");

  // Charger tous les produits existants
  fetch(`${API_BASE}/admin/produits`)
    .then((res) => res.json())
    .then((data) => {
      if (data.produits) {
        data.produits.forEach(afficherProduit);
      }
    });// Fonction pour afficher un produit
  function afficherProduit(produit) {
    const clone = template.content.cloneNode(true);
    clone.querySelector(".produit-nom").textContent = produit.nom;
    clone.querySelector(".produit-prix").textContent = produit.prix.toFixed(2);
    clone.querySelector(".produit-categorie").textContent = produit.categorie;
    clone.querySelector(".produit-annonceur").textContent = produit.annonceur;
    const url = clone.querySelector(".produit-url");
    if (produit.url) {
      url.href = produit.url;
      url.textContent = "🔗 Voir le produit";
    } else {
      url.href = "#";
      url.textContent = "—";
    }
    const image = clone.querySelector(".produit-image");
    image.src = produit.image || "https://via.placeholder.com/300x200?text=Sans+image";
    image.alt = produit.nom;

    const elementProduit = clone.querySelector(".produit-item");// Action : supprimer un produit
    clone.querySelector(".supprimer-btn").addEventListener("click", () => {
      fetch(`${API_BASE}/admin/produit/${produit.id}`, {
        method: "DELETE",
      })
        .then((res) => res.json())
        .then((data) => {
          messageActions.textContent = data.message;
          elementProduit.remove();
        })
        .catch((err) => {
          messageActions.textContent = "Erreur lors de la suppression.";
          console.error(err);
        });
    });

    // Action : modifier un produit
    clone.querySelector(".modifier-btn").addEventListener("click", () => {
      document.getElementById("modale-modification").classList.remove("hidden");
      document.getElementById("modif-id").value = produit.id;
      document.getElementById("modif-nom").value = produit.nom;
      document.getElementById("modif-prix").value = produit.prix;
      document.getElementById("modif-categorie").value = produit.categorie;
      document.getElementById("modif-annonceur").value = produit.annonceur;
      document.getElementById("modif-image").value = produit.image || "";
      document.getElementById("modif-url").value = produit.url || "";
    });

    produitsContainer.appendChild(clone);
  }// Soumission du formulaire d’ajout de produit
  formAjout.addEventListener("submit", (e) => {
    e.preventDefault();
    const nouveauProduit = {
      nom: document.getElementById("nom").value,
      prix: parseFloat(document.getElementById("prix").value),
      categorie: document.getElementById("categorie").value,
      annonceur: document.getElementById("annonceur").value,
      image: document.getElementById("image").value || null,
      url: document.getElementById("url").value || null
    };

    fetch(`${API_BASE}/admin/produit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(nouveauProduit)
    })
      .then((res) => res.json())
      .then((data) => {
        messageAjout.textContent = data.message;
        afficherProduit(data.produit);
        formAjout.reset();
      })
      .catch((err) => {
        messageAjout.textContent = "Erreur lors de l'ajout du produit.";
        console.error(err);
      });
  });// Soumission du formulaire de modification
  const modifForm = document.getElementById("modification-form");
  const messageModif = document.getElementById("message-modif");

  modifForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const id = document.getElementById("modif-id").value;
    const produitModifie = {
      id: id,
      nom: document.getElementById("modif-nom").value,
      prix: parseFloat(document.getElementById("modif-prix").value),
      categorie: document.getElementById("modif-categorie").value,
      annonceur: document.getElementById("modif-annonceur").value,
      image: document.getElementById("modif-image").value || null,
      url: document.getElementById("modif-url").value || null
    };

    fetch(`${API_BASE}/admin/produit/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(produitModifie)
    })
      .then((res) => res.json())
      .then((data) => {
        messageModif.textContent = data.message;
        modifForm.reset();
        location.reload(); // Recharger pour refléter les modifs
      })
      .catch((err) => {
        messageModif.textContent = "Erreur lors de la modification.";
        console.error(err);
      });
  });

  // Annuler la modification
  document.getElementById("annuler-modif").addEventListener("click", () => {
    document.getElementById("modale-modification").classList.add("hidden");
    modifForm.reset();
  });
});