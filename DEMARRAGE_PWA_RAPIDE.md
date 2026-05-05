# 🚀 DÉMARRAGE RAPIDE PWA

## En 3 Commandes

### 1️⃣ Collecter les fichiers statiques
```bash
python manage.py collectstatic --noinput
```

### 2️⃣ Démarrer le serveur
```bash
python manage.py runserver
```

### 3️⃣ Ouvrir dans le navigateur
```
http://localhost:8000
```

---

## ✅ Vérifier que tout fonctionne

### 📱 Installation PWA

**Sur Android:**
1. Attendez 2-3 secondes après chargement
2. Vous verrez un bouton "Installer" en bas de l'écran
3. Cliquez dessus
4. L'app s'ajoute à l'écran d'accueil

**Sur iOS (Safari):**
1. Cliquez le bouton Partage (↑)
2. Sélectionnez "Sur l'écran d'accueil"
3. Nommez-la "CCR"
4. Cliquez "Ajouter"

**Sur Windows/Mac (Edge, Chrome):**
1. Cliquez l'icône d'installation dans la barre d'adresse
2. Ou: Menu → "Installer Gestion d'Église CCR"
3. L'app s'ouvre comme une fenêtre indépendante

---

## 🧪 Tests Offline

### Tester le mode hors ligne:

1. **Ouvrir DevTools** (F12)
2. **Aller à**: Application → Service Workers
3. **Vérifier**: "Activated and running" ✅
4. **Cocher**: "Offline"
5. **Actualiser la page**
   - Vous verrez la page offline
   - Les boutons Reconnexion apparaîtront
6. **Décocher**: "Offline"
   - La page se recharge automatiquement
   - Vous êtes de retour en ligne

---

## 🔍 Vérifier le Service Worker

### Console DevTools:
```javascript
// Vérifier que le SW est enregistré:
navigator.serviceWorker.getRegistrations()

// Affichera:
// ServiceWorkerRegistration {
//   scope: "http://localhost:8000/"
//   active: ServiceWorker
// }
```

### Vérifier le Cache:
1. **DevTools** → **Application** → **Storage** → **Cache Storage**
2. Vous devriez voir `ccr-v1`
3. Cliquez dessus pour voir tous les fichiers en cache

---

## 🔄 Vérifier les Icônes

### Icônes générées:
- ✅ `icon-96x96.png`
- ✅ `icon-192x192.png`
- ✅ `icon-512x512.png`
- ✅ Versions maskable pour iOS/Android

### Localisation:
```
eglise/static/icons/
```

---

## 📊 Vérifier la Validation

```bash
python validate_pwa.py
```

Résultat attendu:
```
✅ Manifest
✅ Scripts
✅ Templates
✅ Icons
✅ Settings
✅ URLs
✅ Views

✅ Résultat: 7/7 composants validés
```

---

## 🛠️ Configuration Fichiers

### Manifest.json
Fichier: `eglise/static/manifest.json`
- Définit le nom, icônes, couleurs
- Contient les raccourcis d'app
- Ajoute les screenshots

### Service Worker
Fichier: `eglise/static/js/service-worker.js`
- Gère le cache
- Fonctionne offline
- Synchronisation en background

### PWA Init
Fichier: `eglise/static/js/pwa-init.js`
- Enregistre le Service Worker
- Détecte les mises à jour
- Gère le statut online/offline

---

## 🎨 Personnaliser les Icônes

Si vous voulez générer vos propres icônes:

```bash
python generate_icons.py
```

Cela créera:
- Icônes SVG + PNG
- Versions maskable
- Screenshots placeholder

---

## 📝 Fichiers Clés

| Fichier | Purpose |
|---------|---------|
| `eglise/static/manifest.json` | Configuration PWA |
| `eglise/static/js/service-worker.js` | Cache & Offline |
| `eglise/static/js/pwa-init.js` | Initialisation PWA |
| `eglise/templates/eglise/offline.html` | Page offline |
| `eglise/static/icons/` | Icônes et screenshots |
| `GUIDE_PWA.md` | Documentation complète |
| `validate_pwa.py` | Script de validation |

---

## 🐛 Problèmes Courants

### "L'app n'est pas installable"
- ✅ HTTPS requis (localhost OK)
- ✅ manifest.json doit être valide
- ✅ Service Worker enregistré
- ✅ Icône 192x192 minimum

### "Le mode offline ne fonctionne pas"
- ✅ Vérifier le Service Worker dans DevTools
- ✅ Vérifier que offline.html existe
- ✅ Vérifier le cache dans Storage
- ✅ Rafraîchir la page (Ctrl+F5)

### "Les changements n'apparaissent pas"
- ✅ Vider le cache: `caches.delete('ccr-v1')`
- ✅ Actualiser en dur: Ctrl+Shift+Delete
- ✅ Désinstaller et réinstaller l'app
- ✅ Vérifier la version du Service Worker

---

## 📱 Où Trouver la PWA Installée

### Android:
- Écran d'accueil → Cherchez "CCR"
- Menu d'app → CCR

### iOS:
- Écran d'accueil → Cherchez "Gestion d'Église"

### Windows:
- Menu Démarrer → Cherchez "Gestion d'Église"
- Ou: Bureau (si épinglée)

### Mac:
- Dock (si épinglée)
- Applications → Gestion d'Église CCR

---

## ✨ Fonctionnalités Avancées

### Raccourcis d'App (preuve):
L'app a 3 raccourcis configurés:

1. **Tableau de Bord** → `/`
2. **Mes Rapports** → `/rapports/`
3. **Liste des Membres** → `/membres/`

Accès: Appui long sur l'icône d'app → Appuyez sur le raccourci

---

## 📞 Besoin d'Aide?

1. Consultez: `GUIDE_PWA.md`
2. Exécutez: `python validate_pwa.py`
3. Vérifiez DevTools: Application → Service Workers
4. Regardez les logs: `logs/scheduler.log`

---

**🎉 Prêt? Commencez par: `python manage.py runserver`**
