// main.js
import './priceTracker.js';
import './recommendations.js';
import './dashboard.js';

document.addEventListener('DOMContentLoaded', () => {
  // 1) Configuration API CJ
  const API_KEY      = 'TON_IDENTIFIANT_API_CJ';
  const API_ENDPOINT = 'https://api.cj.com/v3/product-search';

  // 2) Produits et annonceurs
  const PRODUCTS = [
    { id:1, name:'Petit Bateau – Body Bébé',        category:'mode',     advertisers:['Petit Bateau DE','Petit Bateau IT'], image:'images/petit-bateau-de.jpg' },
    { id:2, name:'Pierre & Vacances Séjour 7j',      category:'vacances', advertisers:['Pierre & Vacances UK'],    image:'images/pierre-vacances-uk.jpg' },
    { id:3, name:'Valise Rimowa Classic Cabin',      category:'bagages',  advertisers:['Rimowa EU'],               image:'images/rimowa-eu.jpg' },
    { id:4, name:'Tableau Moderne – Singulart',      category:'art',      advertisers:['Singulart'],                image:'images/singulart.jpg' }
  ];

  // 3) Helpers API
  async function fetchOffers(product) {
    const q       = encodeURIComponent(product.name);
    const advStr  = product.advertisers.map(a=>`"${a}"`).join(',');
    const url     = `${API_ENDPOINT}?apiKey=${API_KEY}&keywords=${q}&advertiser-ids=${advStr}`;
    try {
      const res  = await fetch(url);
      const jobj = await res.json();
      // normaliser
      return jobj.results
        .filter(o=> product.advertisers.includes(o.advertiserName))
        .map(o=>({ merchant:o.advertiserName, price:parseFloat(o.price), url:o.buyUrl, rating:parseFloat(o.avgRating||3) }))
        .sort((a,b)=>a.price - b.price);
    } catch(e) {
      console.error('API CJ error', e);
      return [];
    }
  }

  // 4) Rendu produit
  async function renderProduct(p) {
    const container = document.createElement('div');
    container.className = 'product';
    const offers    = await fetchOffers(p);
    PriceTracker.saveHistory(p.id, offers[0]?.price||0);
    const top3      = Recommendations.getTopOffers(offers);

    // alerts UI
    const alertsUI = PriceTracker.getAlerts().filter(a=>a.productId===p.id)
      .map(a=>`<div class="alert-item">🔔 Alerte à ${a.targetPrice}€ <button data-id="${p.id}" class="remove-alert">✖</button></div>`).join('');

    container.innerHTML = `
      <img src="${p.image}" alt="${p.name}">
      <div class="product-body">
        <h3>${p.name}</h3>
        <div class="description">Catégorie: ${p.category}</div>
      </div>
      <div class="offers">
        ${offers.map(o=>`
          <div class="offer">
            <span>${o.merchant} : ${o.price.toFixed(2)}€ ${o.rating?`★${o.rating}`:''}</span>
            <a href="${o.url}" target="_blank">Acheter</a>
          </div>`).join('')}
        ${!offers.length?'<div class="offer">Aucune offre</div>':''}
      </div>
      <div class="alerts">
        ${alertsUI || '<button class="add-alert">Créer alerte</button>'}
      </div>
      <div class="recommendations">
        <strong>Top Reco:</strong>
        ${top3.map(o=>`<div>${o.merchant} à ${o.price.toFixed(2)}€</div>`).join('')}
      </div>`;
    return container;
  }

  // 5) Affichage et interactions
  async function displayProducts(list) {
    const grid = document.getElementById('products');
    grid.innerHTML = '';
    const allOffers = {};
    for (let p of list) {
      const card = await renderProduct(p);
      allOffers[p.id] = JSON.parse(card.querySelector('.offers').innerText.match(/\d+(\.\d+)?/g) || '[]');
      grid.appendChild(card);
    }
    updateAlertsUI(allOffers);
    Dashboard.renderPriceChart(list[0]?.id);
  }

  function updateAlertsUI(allOffers) {
    const fired = PriceTracker.checkAlerts(allOffers);
    const alertsDiv = document.getElementById('alerts-list');
    alertsDiv.innerHTML = fired.map(f=>`
      <div class="alert-item">
        🔥 ${PRODUCTS.find(p=>p.id===f.product—