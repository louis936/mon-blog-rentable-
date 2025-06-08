document.addEventListener("DOMContentLoaded", function() {
  // Message de bienvenue
  console.log("Bienvenue sur Mon Site Pro !");
  
  // Exemple d'interaction : changement de couleur pour les cards au clic
  const cards = document.querySelectorAll('.card');
  cards.forEach(card => {
    card.addEventListener('click', function() {
      card.style.backgroundColor = '#e0f7fa';
    });
  });
});