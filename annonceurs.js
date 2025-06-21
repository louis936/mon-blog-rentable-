document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("liste-annonceurs");

  const annonceurs = [
    {
      nom: "Petit Bateau",
      slug: "petit-bateau",
      categorie: "Enfants",
      id: "7000830",
      commission: "6%",
      lien: "https://www.cj.com/track/7587661/petit-bateau-de",
      produits: [
        { nom: "Pyjama coton bio", prix: 29.99, image: "/images/produits/bateau1.jpg" },
        { nom: "Marinière enfant", prix: 34.99, image: "/images/produits/bateau2.jpg" }
      ]
    },
    {
      nom: "Pierre & Vacances",
      slug: "pierre-vacances",
      categorie: "Vacances",
      id: "2249115",
      commission: "6%",
      lien: "https://www.cj.com/track/7587661/pierre-vacances-uk",
      produits: [
        { nom: "Semaine à la montagne", prix: 499.00, image: "/images/produits/vacances1.jpg" },
        { nom: "Week-end Center Parcs", prix: 269.00, image: "/images/produits/vacances2.jpg" }
      ]
    },
    {
      nom: "Polène Paris",
      slug: "polene",
      categorie: "Sacs à main",
      id: "5305861",
      commission: "10%",
      lien: "https://www.cj.com/track/7587661/polene-paris",
      produits: [
        { nom: "Sac Numéro Un", prix: 350.00, image: "/images/produits/sac1.jpg" },
        { nom: "Modèle Tonca", prix: 420.00, image: "/images/produits/sac2.jpg" }
      ]
    },
    {
      nom: "Rimowa",
      slug: "rimowa",
      categorie: "Bagages",
      id: "5291065",
      commission: "8%",
      lien: "https://www.cj.com/track/7587661/rimowa",
      produits: [
        { nom: "Valise cabine", prix: 429.00, image: "/images/produits/valise1.jpg" },
        { nom: "Valise Check-In M", prix: 580.00, image: "/images/produits/valise2.jpg" }
      ]
    },
    {
      nom: "Singulart",
      slug: "singulart",
      categorie: "Art & déco",
      id: "6783970",
      commission: "variable",
      lien: "https://www.cj.com/track/7587661/singulart",
      produits: [
        { nom: "Peinture contemporaine", prix: 899.00, image: "/images/produits/peinture1.jpg" },
        { nom: "Photographie limitée", prix: 450.00, image: "/images/produits/peinture2.jpg" }
      ]
    }
  ];

  annonceurs.forEach((a) => {
    const card = document.createElement("div");
    card.className = "catalogue-item";

    card.innerHTML = `
      <img src="/images/annonceurs/${a.slug}.png" alt="Logo ${a.nom}" style="height:60px; margin-bottom:10px" />
      <h2>${a.nom}</h2>
      <p><strong>Catégorie :</strong> ${a.categorie}</p>
      <p><strong>ID affilié :</strong> ${a.id}</p>
      <p><strong>Commission :</strong> ${a.commission}</p>
      <p><a href="${a.lien}" target="_blank">🔗 Voir la boutique</a></p>
      <div class="produits-mini">
        ${a.produits.map(p => `
          <div class="mini-produit">
            <img src="${p.image}" alt="${p.nom}" />
            <p>${p.nom}<br><strong>${p.prix.toFixed(2)} €</strong></p>
          </div>
        `).join('')}
      </div>
    `;

    container.appendChild(card);
  });
});