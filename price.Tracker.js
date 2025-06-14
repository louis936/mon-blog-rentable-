// priceTracker.js
// Gère l’historique des prix et les alertes

const PriceTracker = (() => {
  const STORAGE_KEY = 'price_history';
  const ALERTS_KEY  = 'price_alerts';

  function saveHistory(productId, price) {
    const all = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
    if (!all[productId]) all[productId] = [];
    all[productId].push({ date: Date.now(), price });
    localStorage.setItem(STORAGE_KEY, JSON.stringify(all));
  }

  function getHistory(productId) {
    const all = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
    return all[productId] || [];
  }

  function addAlert(productId, targetPrice) {
    const alerts = JSON.parse(localStorage.getItem(ALERTS_KEY) || '[]');
    alerts.push({ productId, targetPrice, created: Date.now() });
    localStorage.setItem(ALERTS_KEY, JSON.stringify(alerts));
  }

  function getAlerts() {
    return JSON.parse(localStorage.getItem(ALERTS_KEY) || '[]');
  }

  function checkAlerts(latestOffers) {
    const alerts = getAlerts();
    const fired = [];
    for (let a of alerts) {
      const offer = latestOffers[a.productId]?.find(o => o.price <= a.targetPrice);
      if (offer) fired.push({ ...a, offer });
    }
    return fired;
  }

  return { saveHistory, getHistory, addAlert, getAlerts, checkAlerts };
})();