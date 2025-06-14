// recommendations.js
// Recommandations basiques basées sur notes et prix

const Recommendations = (() => {
  // Score = (rating out of 5) * 20 + (minPriceFactor)
  function scoreOffer(rating, price, minPrice) {
    return rating * 20 + ((minPrice / price) * 30);
  }

  function getTopOffers(offers) {
    if (!offers.length) return [];
    const minPrice = Math.min(...offers.map(o => o.price));
    return offers
      .map(o => ({ ...o, score: scoreOffer(o.rating || 3, o.price, minPrice) }))
      .sort((a, b) => b.score - a.score)
      .slice(0, 3);
  }

  return { getTopOffers };
})();