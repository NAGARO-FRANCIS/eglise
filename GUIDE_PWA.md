# 📱 Configuration PWA - Gestion d'Église CCR

## 🎯 Vue d'ensemble

Votre application Django a été convertie en une **Progressive Web App (PWA)**, ce qui signifie qu'elle peut maintenant :

✅ **Être installée** sur les appareils (téléphone, tablette, ordinateur)  
✅ **Fonctionner hors ligne** avec les données mises en cache  
✅ **Se mettre à jour automatiquement** avec les nouvelles versions  
✅ **Recevoir des notifications** push (optionnel)  
✅ **Avoir une expérience native** avec icône sur l'écran d'accueil  

---

## 📋 Architecture PWA Implémentée

### 1. **Manifest.json** (`eglise/static/manifest.json`)
Le fichier de configuration PWA qui définit :
- Nom et description de l'application
- Icônes (192x192, 512x512 avec versions maskable)
- Couleurs (thème: #5e72e4, background: blanc)
- Mode d'affichage: `standalone` (sans barre du navigateur)
- Raccourcis (Tableau de bord, Rapports, Membres)
- Screenshots pour la bannière d'installation

### 2. **Service Worker** (`eglise/static/js/service-worker.js`)
Gère :
- **Cache des fichiers** à l'installation
- **Stratégie Network First** pour les données dynamiques (rapports, membres)
- **Stratégie Cache First** pour les assets statiques (CSS, JS, images)
- **Récupération offline** - retourne une page offline quand pas de connexion
- **Synchronisation en arrière-plan** - infrastructure prête pour les futures mises à jour

### 3. **Initialization Script** (`eglise/static/js/pwa-init.js`)
Gère :
- Enregistrement du Service Worker
- Vérification des mises à jour
- Notifications de mise à jour disponible
- Statut online/offline
- Invite d'installation PWA

### 4. **Page Offline** (`eglise/templates/eglise/offline.html`)
Affichée quand l'utilisateur est hors ligne avec :
- Message informatif
- État du cache local
- Bouton de reconnexion automatique
- Vérification périodique de la connexion

### 5. **Vues PWA** (dans `eglise/views.py`)
```python
OfflineView  # Vue pour la page offline
PingView     # Point de contrôle pour vérifier la connexion
```

---

## 🚀 Installation et Configuration

### Fichiers Modifiés :

1. **eglise/templates/eglise/base.html**
   - Ajout du manifest.json
   - Meta tags PWA (theme-color, mobile-web-app-capable, etc.)
   - Apple touch icon
   - Chargement du script pwa-init.js

2. **eglise/urls.py**
   - Route `/offline/` → OfflineView
   - Route `/ping/` → PingView (pour vérifier la connexion)

3. **CCR/settings.py**
   - Configuration STATIC_ROOT et STATICFILES_DIRS
   - Paramètres PWA (noms, couleurs, orientation)
   - Configuration du cache Django
   - Stockage des fichiers statiques manifestés

---

## 📥 Comment Installer la PWA

### Sur **Android (Chrome, Firefox)**:
1. Ouvrez l'application dans le navigateur
2. Attendez 3-5 secondes
3. Cliquez sur le bouton **"Installer"** (apparaît généralement en bas)
4. L'application s'ajoute à l'écran d'accueil

### Sur **iOS (Safari)**:
1. Ouvrez l'application dans Safari
2. Cliquez sur **Partager** (↑)
3. Choisissez **"Sur l'écran d'accueil"**
4. Nommez l'application (ex: "CCR")
5. L'application s'ajoute à l'écran d'accueil

### Sur **Windows/Mac (Edge, Chrome)**:
1. Ouvrez l'application
2. Cliquez sur l'**icône d'installation** dans la barre d'adresse
3. Choisissez **"Installer Gestion d'Église CCR"**
4. L'application s'ouvre comme une fenêtre indépendante

---

## 🔄 Stratégies de Mise en Cache

### **Network First** (données dynamiques):
```
/rapports/      → Cherche sur le réseau en premier
/membres/       → Si indisponible, retourne le cache
/api/           → Synchronise en background
```

### **Cache First** (assets statiques):
```
CSS, JS, images → Charge depuis le cache en premier
                → Met à jour en background
```

---

## 📱 Fonctionnalités Offline

Quand l'utilisateur est **hors ligne** :

✅ Peut consulter les rapports précédemment chargés  
✅ Peut voir la liste des membres en cache  
✅ Voit une page d'information offline  
✅ La connexion est vérifiée toutes les 5 secondes  
✅ Reconnecte automatiquement au rétablissement de la connexion  

---

## 🔐 Sécurité PWA

1. **HTTPS requis** (en production)
   - Les PWA nécessitent HTTPS pour fonctionner correctement
   - En développement, `localhost` est autorisé

2. **Service Worker scope**
   - Limité à `/` pour l'isolation
   - Pas d'accès aux autres domaines

3. **Cache management**
   - Vieilles versions supprimées automatiquement
   - Nouvelles versions téléchargées en background

---

## 📊 Icônes Générées

Toutes les icônes sont dans `eglise/static/icons/` :

### Icônes Standard:
- `icon-96x96.png` (petite)
- `icon-192x192.png` (écran d'accueil)
- `icon-512x512.png` (splash screen)

### Icônes Maskable (OS adaptatif):
- `icon-96x96-maskable.png`
- `icon-192x192-maskable.png`
- `icon-512x512-maskable.png`

### Screenshots:
- `screenshot-1.png` (540x720)
- `screenshot-2.png` (540x720)

### Format SVG:
- Toutes les icônes sont aussi disponibles en SVG pour une meilleure scalabilité

---

## 🧪 Test et Débogage

### Vérifier les Service Workers :
```
Chrome DevTools → Application → Service Workers
→ Vous devriez voir le service worker "Activated and running"
```

### Vérifier le Cache :
```
Chrome DevTools → Application → Storage → Cache Storage
→ Vous devriez voir "ccr-v1" avec les fichiers en cache
```

### Vérifier le Manifest :
```
Chrome DevTools → Application → Manifest
→ Vous devriez voir tous les détails PWA
```

### Mode Offline :
```
Chrome DevTools → Network → Throttling → Offline
→ Actualisez la page, la page offline s'affiche
```

---

## 🔧 Mise à Jour de la PWA

Quand vous mettez à jour l'application :

1. **Développement** : Changez le numéro de version dans `manifest.json` et `service-worker.js`
2. **Déploiement** : Le Service Worker détecte automatiquement la nouvelle version
3. **Notification** : Une bannière s'affiche : "Une nouvelle version est disponible"
4. **Mise à jour** : L'utilisateur clique sur "Mettre à jour" et recharge

```javascript
// Dans service-worker.js
const CACHE_NAME = 'ccr-v2';  // Changer v1 en v2
```

---

## 📚 Ressources Supplémentaires

- [MDN - Progressive Web Apps](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps)
- [Google - PWA Documentation](https://developers.google.com/web/progressive-web-apps)
- [Can I use - PWA Feature Support](https://caniuse.com/mdn-css_media_prefers_color_scheme)

---

## ⚡ Optimisations Futures

Pour améliorer davantage la PWA :

1. **Notifications Push** - Alerter les utilisateurs des nouveaux rapports
2. **Synchronisation Background** - Charger les données quand la connexion revient
3. **Compression des images** - Réduire la taille du cache
4. **Partage de fichiers** - Permettre l'export des rapports
5. **API de géolocalisation** - Localiser les cultes par géolocalisation

---

## 🐛 Dépannage

### "Le Service Worker ne s'enregistre pas"
```
✓ Vérifier que l'application utilise HTTPS
✓ Vérifier que manifest.json existe et est valide
✓ Vérifier la console du navigateur pour les erreurs
```

### "La mise en cache ne fonctionne pas"
```
✓ Vérifier que les fichiers statiques sont collectés:
  python manage.py collectstatic
✓ Vérifier le Storage dans les DevTools
✓ Vérifier que le Service Worker est "Activated"
```

### "L'application n'est pas installable"
```
✓ HTTPS requis (ou localhost)
✓ Manifest.json doit être valide
✓ Au moins 192x192 icône requise
✓ Service Worker enregistré avec succès
```

---

**✨ Votre application est maintenant une PWA complète et fonctionnelle!**
