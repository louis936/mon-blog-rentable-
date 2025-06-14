document.addEventListener("DOMContentLoaded", () => {
  // → Remplace ces URLs par tes vrais liens CJ
  const AFFIL_LINKS = {
    tech: [
      { merchant: "TechShop", price: 49.99, url: "https://cj.com/affil/tech1" },
      { merchant: "GadgetPro", price: 45.50, url: "https://cj.com/affil/tech2" }
    ],
    mode: [
      { merchant: "StyleCorner", price: 79.90, url: "https://cj.com/affil/mode1" },
      { merchant: "FashionWeb", price: 85.00, url: "https://cj.com/affil/mode2" }
    ],
    maison: [
      { merchant: "HomeEssentials", price: 120.00, url: "https://cj.com/affil/maison1" },
      { merchant: "DailyComfort", price: 110.25, url: "https://cj.com/affil/maison2" }
    ]
  };

  // PRODUITS
  const products = [
    {
      id: 1, name: "Gadget Tech",
      category: "tech", image: "tech.jpg",
      description: "Le meilleur gadget tech du marché.",
      offers: AFFIL_LINKS.tech
    },
    {
      id: 2, name: "Veste Stylée",
      category: "mode", image: "mode.jpg",
      description: "Veste tendance à petit prix.",
      offers: AFFIL_LINKS.mode
    },
    {
      id: 3, name: "Robot Ménager",
      category: "maison", image: "maison.jpg",
      description: "Facilite ton quotidien.",
      offers: AFFIL_LINKS.maison
    }
  ];

  // AVIS CLIENTS
  const reviews = [
    { author: "Alice", text: "Produit top, livraison rapide ! ⭐⭐⭐⭐" },
    { author: "Bob",   text: "Très satisfait, je recommande. ⭐⭐⭐⭐⭐" },
    { author: "Claire",text: "Bon rapport qualité-prix. ⭐⭐⭐⭐" }
  ];

  // Éléments DOM
  const prodContainer  = document.getElementById("products");
  const revContainer   = document.getElementById("reviewList");
  const searchInput    = document.getElementById("search");
  const catButtons     = document.querySelectorAll(".sidebar button[data-cat]");
  const minPriceInput  = document.getElementById("minPrice");
  const maxPriceInput  = document.getElementById("maxPrice");
  const applyPriceBtn  = document.getElementById("applyPrice");

  // AFFICHAGE PRODUITS
  function displayProducts(list) {
    prodContainer.innerHTML = "";
    list.forEach(p => {
      // trier les offres par prix croissant
      p.offers.sort((a,b) => a.price - b.price);
      const card = document.createElement("div");
      card.className = "product";
      card.innerHTML = `
        <img src="${p.image}" alt="${p.name}">
        <div class="product-body">
          <h3>${p.name}</h3>
          <p>${p.description}</p>
        </div>
        <div class="offers">
          ${p.offers.map(o =>
            `<div class="offer">
               <span>${o.merchant}: ${o.price.toFixed(2)}€</span>
               <a href="${o.url}" target="_blank">Acheter</a>
             </div>`
          ).join("")}
        </div>
      `;
      prodContainer.appendChild(card);
    });
  }

  // AFFICHAGE AVIS
  function displayReviews() {
    revContainer.innerHTML = "";
    reviews.forEach(r => {
      const card = document.createElement("div");
      card.className = "review";
      card.innerHTML = `<div class="author">${r.author}</div><div>${r.text}</div>`;
      revContainer.appendChild(card);
    });
  }

  // FILTRAGE
  function filterAndDisplay() {
    let filtered = products.filter(p => {
      // catégorie
      const catFilter = document.querySelector(".sidebar button.active").dataset.cat;
      if (catFilter !== "all" && p.category !== catFilter) return false;

      // prix
      const minPrice = parseFloat(minPriceInput.value) || 0;
      const maxPrice = parseFloat(maxPriceInput.value) || Infinity;
      return p.offers.some(o => o.price >= minPrice && o.price <= maxPrice);
    });

    displayProducts(filtered);
  }

  // ÉCOUTEURS D'ÉVÉNEMENTS
  searchInput.addEventListener("input", () => {
    const query = searchInput.value.toLowerCase();
    displayProducts(products.filter(p => p.name.toLowerCase().includes(query)));
  });

  catButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      catButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      filterAndDisplay();
    });
  });

  applyPriceBtn.addEventListener("click", filterAndDisplay);

  // INIT
  displayProducts(products);
  displayReviews();
});