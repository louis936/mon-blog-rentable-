// Données issues de recherches pour 2025 avec enseignes populaires
const enseignes = [
  {
    enseigne: "Amazon",
    logo: "https://via.placeholder.com/400x180?text=Amazon+Logo",
    product: {
      name: "Amazon Echo Dot 4ème Génération",
      img: "https://via.placeholder.com/400x180?text=Echo+Dot",
      description: "L'assistant vocal le plus plébiscité pour une maison connectée.",
      affiliateLink: "https://amazon.fr/?tag=tonaffiliatetag"
    }
  },
  {
    enseigne: "Kwanko",
    logo: "https://via.placeholder.com/400x180?text=Kwanko+Logo",
    product: {
      name: "Formation Marketing Digital",
      img: "https://via.placeholder.com/400x180?text=Formation+Digital",
      description: "Améliorez vos compétences avec une formation complète en marketing digital.",
      affiliateLink: "https://kwanko.com/affiliation?ref=tonaffiliatetag"
    }
  },
  {
    enseigne: "Digitiz",
    logo: "https://via.placeholder.com/400x180?text=Digitiz+Logo",
    product: {
      name: "Comparatif d'Offres Digitales",
      img: "https://via.placeholder.com/400x180?text=Comparatif+Offres",
      description: "Découvrez et comparez les meilleures offres du marché digital.",
      affiliateLink: "https://digitiz.com/affiliation?ref=tonaffiliatetag"
    }
  },
  {
    enseigne: "Action",
    logo: "https://via.placeholder.com/400x180?text=Action+Logo",
    product: {
      name: "Objets du quotidien à petit prix",
      img: "https://via.placeholder.com/400x180?text=Action+Deals",
      description: "Des trouvailles incroyables pour un quotidien malin, plébiscité par les Français.",
      affiliateLink: "https://action.com/affiliation?ref=tonaffiliatetag"
    }
  },
  {
    enseigne: "Leroy Merlin",
    logo: "https://via.placeholder.com/400x180?text=Leroy+Merlin+Logo",
    product: {
      name: "Outils et solutions pour la maison",
      img: "https://via.placeholder.com/400x180?text=Leroy+Merlin+Offre",
      description: "Tout pour rénover et embellir votre intérieur avec des outils de qualité.",
      affiliateLink: "https://leroymerlin.fr/affiliation?ref=tonaffiliatetag"
    }
  },
  {
    enseigne: "Decathlon",
    logo: "https://via.placeholder.com/400x180?text=Decathlon+Logo",
    product: {
      name: "Equipements et vêtements de sport",
      img: "https://via.placeholder.com/400x180?text=Decathlon+Offre",
      description: "Des produits sportifs de qualité, parfaits pour vos entraînements.",
      affiliateLink: "https://decathlon.fr/affiliation?ref=tonaffiliatetag"
    }
  }
];

// Le produit premium retenu est celui mis en avant pour chaque enseigne.
const produitsPremium = enseignes.map(item => {
  return {
    enseigne: item.enseigne,
    name: item.product.name,
    img: item.product.img,
    description: item.product.description,
    affiliateLink: item.product.affiliateLink
  };
});

// Fonction pour créer une carte HTML (avec événement pour ouvrir la modal)
function createCard(data, isEnseigne = false) {
  const card = document.createElement('div');
  card.className = 'card';
  let cardInner = '';

  if (isEnseigne) {
    cardInner = `
      <img src="${data.logo}" alt="${data.enseigne} Logo">
      <div class="card-content">
        <h3>${data.enseigne}</h3>
        <p>${data.product.name}</p>
        <a href="${data.product.affiliateLink}" class="cta" target="_blank">Voir l'offre</a>
      </div>
    `;
  } else {
    cardInner = `
      <img src="${data.img}" alt="${data.name}">
      <div class="card-content">
        <h3>${data.name}</h3>
        <p>${data.description}</p>
        <a href="${data.affiliateLink}" class="cta" target="_blank">Profiter de l'offre</a>
      </div>
    `;
  }

  card.innerHTML = cardInner;

  // Ajout d'un événement de clic pour ouvrir la modal avec des détails du produit
  card.addEventListener('click', (e) => {
    // Évite d'interférer avec le lien d'affiliation (ouverture dans un nouvel onglet)
    if(e.target.tagName.toLowerCase() !== 'a'){
      openModal(data, isEnseigne);
    }
  });

  return card;
}

// Fonction pour afficher les cartes dans les conteneurs
function renderCards() {
  const enseigneContainer = document.getElementById('enseigne-cards');
  const premiumContainer = document.getElementById('premium-cards');
  
  enseigneContainer.innerHTML = '';
  premiumContainer.innerHTML = '';
  
  enseignes.forEach(item => {
    enseigneContainer.appendChild(createCard(item, true));
  });
  
  produitsPremium.forEach(item => {
    premiumContainer.appendChild(createCard(item, false));
  });

  // Lancer l'animation par Intersection Observer sur les cartes
  animateCards();
}

// Fonction de recherche qui filtre les cartes
function filterCards(query) {
  const lowerQuery = query.toLowerCase();
  const enseigneContainer = document.getElementById('enseigne-cards');
  const premiumContainer = document.getElementById('premium-cards');
  
  enseigneContainer.innerHTML = '';
  premiumContainer.innerHTML = '';

  enseignes
    .filter(item => 
      item.enseigne.toLowerCase().includes(lowerQuery) ||
      item.product.name.toLowerCase().includes(lowerQuery)
    )
    .forEach(item => {
      enseigneContainer.appendChild(createCard(item, true));
    });
  
  produitsPremium
    .filter(item =>
      item.name.toLowerCase().includes(lowerQuery)
    )
    .forEach(item => {
      premiumContainer.appendChild(createCard(item, false));
    });
  
  animateCards();
}

// Dark/Light Mode Toggle et sauvegarde
const themeToggle = document.getElementById('themeToggle');
themeToggle.addEventListener('click', () => {
  const currentMode = document.body.classList.toggle('dark-mode');
  themeToggle.textContent = currentMode ? '☀️' : '🌙';
  localStorage.setItem('theme', currentMode ? 'dark' : 'light');
});

// Récupération du thème enregistré lors du chargement
document.addEventListener('DOMContentLoaded', () => {
  const savedTheme = localStorage.getItem('theme');
  if(savedTheme === 'dark'){
    document.body.classList.add('dark-mode');
    themeToggle.textContent = '☀️';
  }
  renderCards();
});

// Animation des cartes avec Intersection Observer
function animateCards() {
  const cards = document.querySelectorAll('.card');
  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if(entry.isIntersecting) {
        entry.target.classList.add('show');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });

  cards.forEach(card => {
    observer.observe(card);
  });
}

// Fonctions pour gérer la modal avec détails du produit
const modal = document.getElementById('modal');
const modalBody = document.getElementById('modalBody');
const modalClose = document.getElementById('modalClose');

function openModal(data, isEnseigne) {
  let modalContent = '';
  
  if(isEnseigne) {
    modalContent = `
      <img src="${data.logo}" alt="${data.enseigne} Logo" style="width:100%; max-height:200px; object-fit:contain;">
      <h2>${data.enseigne}</h2>
      <p><strong>Produit mis en avant :</strong> ${data.product.name}</p>
      <p>${data.product.description}</p>
      <a href="${data.product.affiliateLink}" class="cta" target="_blank">Voir l'offre</a>
    `;
  } else {
    modalContent = `
      <img src="${data.img}" alt="${data.name}" style="width:100%; max-height:200px; object-fit:cover;">
      <h2>${data.name}</h2>
      <p>${data.description}</p>
      <a href="${data.affiliateLink}" class="cta" target="_blank">Profiter de l'offre</a>
    `;
  }
  
  modalBody.innerHTML = modalContent;
  modal.style.display = 'block';
}

// Fermeture de la modal
modalClose.addEventListener('click', () => {
  modal.style.display = 'none';
});
window.addEventListener('click', (e) => {
  if(e.target === modal) {
    modal.style.display = 'none';
  }
});

// Barre de recherche
document.getElementById('searchInput').addEventListener('input', (e) => {
  const query = e.target.value;
  if (query.trim() === '') {
    renderCards();
  } else {
    filterCards(query);
  }
});