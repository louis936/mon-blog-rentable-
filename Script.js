/* ========================================
   CONFIGURATION & ÉTAT GLOBAL
======================================== */
const API_KEY     = "9UJdqflU6NsT0JW_z6bAqogATA";
const SITE_ID     = "7587661";
const BASE_SEARCH = "https://api.cj.com/v3/product-search";
const BASE_CAT    = "https://api.cj.com/v3/categories";

const cache       = {};
let favorites     = JSON.parse(localStorage.getItem("favorites") || "[]");
let comparison    = [];

/* ========================================
   UTILITAIRES UI
======================================== */
const show = el => el.style.display = "";
const hide = el => el.style.display = "none";
const toggle = el => el.classList.toggle("hidden");
const qs = s => document.querySelector(s);

/* ========================================
   INITIALISATION DOM
======================================== */
document.addEventListener("DOMContentLoaded", () => {
  const loader    = qs("#loader");
  const message   = qs("#message");
  const results   = qs("#results");
  const pageInfo  = qs("#page-info");
  const btnPrev   = qs("#prev-page");
  const btnNext   = qs("#next-page");

  const cmpPanel      = qs("#compare-container");
  const favPanel      = qs("#favorites-container");
  const favList       = qs("#favorites-list");
  const cmpTbody      = qs("#compare-table tbody");
  const toggleFavBtn  = qs("#toggle-favorites");
  const toggleCmpBtn  = qs("#toggle-compare");
  const closeCmpBtn   = qs("#close-compare");
  const closeFavBtn   = qs("#close-favorites");
  const acceptCookie  = qs("#accept-cookies");
  const cookieBanner  = qs("#cookie-banner");
  const themeToggle   = qs("#theme-toggle");

  let currentPage = 1, lastQuery = "";

  // Mode sombre init
  const savedTheme = localStorage.getItem("theme") || "light";
  document.documentElement.dataset.theme = savedTheme;
  themeToggle.textContent = savedTheme==="dark" ? "☀️":"🌙";

  // bannière cookies
  if (!localStorage.getItem("cookiesAccepted")) {
    cookieBanner.classList.remove("hidden");
  }
  acceptCookie.onclick = () => {
    localStorage.setItem("cookiesAccepted","yes");
    cookieBanner.classList.add("hidden");
  };

  // panels toggle
  toggleFavBtn.onclick = () => toggle(favPanel);
  toggleCmpBtn.onclick = () => toggle(cmpPanel);
  closeCmpBtn.onclick  = () => cmpPanel.classList.add("hidden");
  closeFavBtn.onclick  = () => favPanel.classList.add("hidden");

  // theme toggle
  themeToggle.onclick = () => {
    const newTheme = document.documentElement.dataset.theme==="dark"?"light":"dark";
    document.documentElement.dataset.theme = newTheme;
    localStorage.setItem("theme", newTheme);
    themeToggle.textContent = newTheme==="dark" ? "☀️":"🌙";
  };

  // pagination
  btnPrev.onclick = () => fetchProducts(lastQuery, currentPage-1);
  btnNext.onclick = () => fetchProducts(lastQuery, currentPage+1);

  // filtres
  qs("#apply-filters").onclick = () => {
    const q = qs("#search-input").value.trim();
    if (!q) return showMessage("Entrez un mot-clé");
    lastQuery = q; currentPage = 1;
    fetchProducts(q, 1);
  };
  qs("#clear-filters").onclick = () => {
    qs("#search-input").value="";
    qs("#min-price").value="";
    qs("#max-price").value="";
    qs("#cat-select").value="";
    qs("#sort-by").value="relevance";
    lastQuery = ""; results.innerHTML="";
    hide(qs("#pagination"));
  };

  // load categories & favorites
  loadCategories();
  renderFavorites();

  // optional default search
  // lastQuery="tech"; fetchProducts("tech",1);

  /*** FUNCTIONS ***/

  function showMessage(txt) {
    message.textContent = txt;
    show(message); hide(loader);
  }

  async function fetchProducts(query, page=1) {
    lastQuery = query; currentPage = page;
    const key = `${query}|${page}`;
    show(loader); hide(message); hide(qs("#results")); hide(qs("#pagination"));

    if (cache[key]) {
      renderProducts(cache[key].products);
      updatePagination(page, cache[key].totalPages);
      return;
    }

    const params = new URLSearchParams({
      query, "website-id": SITE_ID,
      "page-number": page, "records-per-page": 12
    });
    const min = qs("#min-price").value, max = qs("#max-price").value, cat = qs("#cat-select").value, sort = qs("#sort-by").value;
    if (min) params.append("min-price", min);
    if (max) params.append("max-price", max);
    if (cat) params.append("category", cat);

    try {
      const res = await fetch(`${BASE_SEARCH}?${params}`, {
        headers: { "Authorization": `Bearer ${API_KEY}`, "Accept":"application/json" }
      });
      if (!res.ok) throw new Error(`Statut ${res.status}`);
      const json    = await res.json();
      const prods   = json.products || [];
      sortProducts(prods, sort);
      cache[key]    = { products: prods, totalPages: Math.ceil((json["total-matched"]||0)/12) };
      renderProducts(prods);
      updatePagination(page, cache[key].totalPages);
    } catch(err) {
      showMessage("Erreur API : "+err.message);
    }
  }

  function renderProducts(products) {
    const container = qs("#results");
    container.innerHTML = "";
    if (!products.length) { showMessage("Aucun résultat"); return; }
    show(container);
    products.forEach(p => {
      const card = document.createElement("div"); card.className="card";
      const liked = favorites.some(f=>f.id===p.id);
      card.innerHTML = `
        <img src="${p["image-url"]||''}" alt="${p.name}">
        <div class="card-content">
          <h3 class="card-title">${p.name}</h3>
          <p class="card-price">${p.price} ${p.currency}</p>
          <div class="card-actions">
            <button class="favorite-btn ${liked?'liked':''}">★</button>
            <button class="compare-btn">⚖️</button>
          </div>
        </div>`;
      card.querySelector(".favorite-btn").onclick = ()=> toggleFavorite(p);
      card.querySelector(".compare-btn").onclick  = ()=> toggleCompare(p);
      container.appendChild(card);
    });
    show(qs("#pagination")); hide(qs("#loader"));
  }

  function updatePagination(page, total) {
    currentPage = page;
    qs("#page-info").textContent = `Page ${page} / ${total}`;
    qs("#prev-page").disabled = page<=1;
    qs("#next-page").disabled = page>=total;
  }

  function sortProducts(arr, mode) {
    if (mode==="price-asc")  arr.sort((a,b)=>a.price-b.price);
    if (mode==="price-desc") arr.sort((a,b)=>b.price-a.price);
    if (mode==="name-asc")   arr.sort((a,b)=>a.name.localeCompare(b.name));
    if (mode==="name-desc")  arr.sort((a,b)=>b.name.localeCompare(a.name));
  }

  async function loadCategories() {
    try {
      const res = await fetch(`${BASE_CAT}?website-id=${SITE_ID}`, {
        headers: { "Authorization":`Bearer ${API_KEY}`,"Accept":"application/json" }
      });
      if (!res.ok) throw new Error(res.status);
      const { categories } = await res.json();
      const sel = qs("#cat-select");
      categories.forEach(c => {
        const opt = document.createElement("option");
        opt.value = c.id; opt.textContent = c.name;
        sel.appendChild(opt);
      });
    } catch(e){ console.warn("Catégories indisponibles", e); }
  }

  function toggleCompare(prod) {
    const i = comparison.findIndex(x=>x.id===prod.id);
    if (i>-1) comparison.splice(i,1); else comparison.push(prod);
    renderCompare();
  }
  function renderCompare() {
    const tbody = qs("#compare-table tbody");
    tbody.innerHTML = "";
    if (!comparison.length) return qs("#compare-container").classList.add("hidden");
    comparison.forEach(p=>{
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${p.name}</td>
        <td>${p.price} ${p.currency}</td>
        <td>${p.category||'–'}</td>
        <td><a href="${p.buyUrl}" target="_blank">Voir</a></td>
        <td><button class="secondary">✕</button></td>`;
      tr.querySelector("button").onclick = ()=> toggleCompare(p);
      tbody.appendChild(tr);
    });
    qs("#compare-container").classList.remove("hidden");
  }

  function toggleFavorite(prod) {
    const i = favorites.findIndex(x=>x.id===prod.id);
    if (i>-1) favorites.splice(i,1); else favorites.push(prod);
    localStorage.setItem("favorites", JSON.stringify(favorites));
    renderFavorites();
  }
  function renderFavorites() {
    const ul = qs("#favorites-list");
    ul.innerHTML = "";
    if (!favorites.length) return;
    favorites.forEach(p=>{
      const li = document.createElement("li");
      li.innerHTML = `<span>${p.name} – ${p.price} ${p.currency}</span><button class="secondary">✕</button>`;
      li.querySelector("button").onclick = ()=> toggleFavorite(p);
      ul.appendChild(li);
    });
  }
});