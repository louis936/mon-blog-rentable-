// dashboard.js
// Affiche un graphique Chart.js de l’historique des prix

const Dashboard = (() => {
  function renderPriceChart(productId) {
    const data = PriceTracker.getHistory(productId);
    if (!data.length) return;
    const ctx = document.getElementById('chart-price-history').getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: data.map(pt => new Date(pt.date).toLocaleDateString()),
        datasets: [{ label: 'Prix', data: data.map(pt => pt.price), borderColor: '#007bff', fill: false }]
      },
      options: { responsive: true, scales: { y: { beginAtZero: false } } }
    });
  }
  return { renderPriceChart };
})();