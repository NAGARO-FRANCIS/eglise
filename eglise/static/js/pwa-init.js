// Enregistrement et gestion du Service Worker pour la PWA

if ('serviceWorker' in navigator) {
  // Enregistrer le service worker au chargement de la page
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/static/js/service-worker.js', {
      scope: '/'
    }).then(registration => {
      console.log('[PWA] Service Worker enregistré:', registration);
      
      // Vérifier les mises à jour
      registration.addEventListener('updatefound', () => {
        const newWorker = registration.installing;
        newWorker.addEventListener('statechange', () => {
          if (newWorker.state === 'activated') {
            // Une nouvelle version du service worker est disponible
            showUpdateNotification();
          }
        });
      });
      
      // Vérifier les mises à jour toutes les heures
      setInterval(() => {
        registration.update();
      }, 3600000);
      
    }).catch(error => {
      console.error('[PWA] Erreur enregistrement Service Worker:', error);
    });
  });
  
  // Écouter les messages du service worker
  navigator.serviceWorker.addEventListener('message', event => {
    if (event.data.type === 'UPDATE_AVAILABLE') {
      showUpdateNotification();
    }
  });
}

// Afficher une notification de mise à jour
function showUpdateNotification() {
  const updateBanner = document.createElement('div');
  updateBanner.id = 'update-banner';
  updateBanner.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 16px;
    text-align: center;
    z-index: 9999;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  `;
  
  updateBanner.innerHTML = `
    <div style="max-width: 600px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between;">
      <span>📦 Une nouvelle version est disponible</span>
      <div>
        <button id="update-btn" style="background: white; color: #667eea; border: none; padding: 8px 20px; border-radius: 4px; cursor: pointer; font-weight: bold; margin-right: 10px;">
          Mettre à jour
        </button>
        <button id="dismiss-btn" style="background: transparent; color: white; border: 1px solid white; padding: 8px 20px; border-radius: 4px; cursor: pointer;">
          Plus tard
        </button>
      </div>
    </div>
  `;
  
  document.body.insertBefore(updateBanner, document.body.firstChild);
  
  document.getElementById('update-btn').addEventListener('click', () => {
    if (navigator.serviceWorker.controller) {
      navigator.serviceWorker.controller.postMessage({ type: 'SKIP_WAITING' });
    }
    window.location.reload();
  });
  
  document.getElementById('dismiss-btn').addEventListener('click', () => {
    updateBanner.remove();
  });
}

// Afficher une notification de statut online/offline
function updateOnlineStatus() {
  const isOnline = navigator.onLine;
  const statusIndicator = document.getElementById('online-status');
  
  if (statusIndicator) {
    if (isOnline) {
      statusIndicator.textContent = '🟢 En ligne';
      statusIndicator.style.color = '#2dce89';
    } else {
      statusIndicator.textContent = '🔴 Hors ligne';
      statusIndicator.style.color = '#f5365c';
    }
  }
}

// Écouter les changements de statut online/offline
window.addEventListener('online', updateOnlineStatus);
window.addEventListener('offline', updateOnlineStatus);

// Vérifier le statut au chargement
document.addEventListener('DOMContentLoaded', updateOnlineStatus);

// Installation PWA - Capturer l'événement d'installation
let deferredPrompt;

window.addEventListener('beforeinstallprompt', event => {
  // Empêcher l'installation automatique
  event.preventDefault();
  // Stocker l'événement pour l'affichage ultérieur
  deferredPrompt = event;
  
  // Afficher un bouton d'installation personnalisé si nécessaire
  const installButton = document.getElementById('install-pwa-btn');
  if (installButton) {
    installButton.style.display = 'block';
    installButton.addEventListener('click', () => {
      if (deferredPrompt) {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then((choiceResult) => {
          if (choiceResult.outcome === 'accepted') {
            console.log('[PWA] Application installée');
          }
          deferredPrompt = null;
        });
      }
    });
  }
});

// Événement d'installation réussie
window.addEventListener('appinstalled', () => {
  console.log('[PWA] Application installée avec succès');
  deferredPrompt = null;
  
  // Masquer le bouton d'installation
  const installButton = document.getElementById('install-pwa-btn');
  if (installButton) {
    installButton.style.display = 'none';
  }
});
