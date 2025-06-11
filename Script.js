// js/app.js
document.addEventListener('DOMContentLoaded', () => {
  // config CJ Affiliate → remplace par tes infos réelles
  const API_ENDPOINT = 'https://api.cj.com/v3/products';
  const WEBSITE_ID   = 'YOUR_WEBSITE_ID';
  const API_KEY      = 'YOUR_CJ_API_KEY';

  // DOM
  const promoGrid   = document.getElementById('promo-grid');
  const productGrid = document.getElementById('product-grid');
  const spinner     = document.getElementById('spinner');
  const searchForm  = document.getElementById('search-form');
  const searchInput = document.getElementById('search-input');
  const cats        = document.querySelectorAll('.cat-list button');

  // utils
  const showSpinner = () => spinner.style.visibility = 'visible