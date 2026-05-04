# 🚀 GUIDE DE DÉMARRAGE RAPIDE - Système de Rapports

## En 5 Minutes

### Étape 1: Vérifier la Configuration (30 sec)
```bash
cd c:\projet\CCR
python manage.py check
# Résultat attendu: "System check identified no issues (0 silenced)"
```

### Étape 2: Générer un Rapport (1 min)
```bash
python generer_rapports.py
# Résultat attendu: 
# ✓ Rapport généré avec succès:
#   - Période: Mai 2026
#   - Membres: 18
#   - Taux de participation: 100.0%
#   - Cultes: 6
```

### Étape 3: Démarrer le Serveur (30 sec)
```bash
python manage.py runserver
# Résultat attendu: "Starting development server at http://127.0.0.1:8000/"
```

### Étape 4: Accéder aux Rapports (30 sec)

**Dans le navigateur:**
1. Accueil: `http://localhost:8000/`
2. Se connecter (admin/admin ou autre utilisateur)
3. Cliquer sur "Rapports" dans le menu
4. Voir la liste des rapports

### Étape 5: Voir les Détails (1 min)

**Dans le navigateur:**
1. Cliquer sur "Voir Détails" d'un rapport
2. Observer les 8 sections
3. Voir les 3 graphiques interactifs
4. Retour à la liste

---

## 🎯 Cas d'Utilisation

### Cas 1: Consulter les Rapports (Utilisateur)
```
1. Se connecter
2. Cliquer "Rapports" dans le menu
3. Voir liste avec filtrage
4. Cliquer "Voir Détails"
5. Consulter graphiques
```

### Cas 2: Générer un Nouveau Rapport (Admin)
```
1. Terminal: python generer_rapports.py
2. Aller à /admin/eglise/rapportmensuel/
3. Voir le nouveau rapport en haut de liste
4. Cliquer pour éditer
5. Ajouter observations
6. Changer statut à "Validé"
7. Enregistrer
```

### Cas 3: Générer pour un Mois Passé (Admin)
```
1. Terminal: python manage.py shell
2. Copier-coller:

from generer_rapports import generer_rapport_mensuel
from django.contrib.auth.models import User
auteur = User.objects.get(username='admin')

# Générer les 12 derniers mois
for month in range(1, 13):
    try:
        generer_rapport_mensuel(month, 2025, auteur)
        print(f"✓ Mois {month} généré")
    except Exception as e:
        print(f"✗ Mois {month} erreur: {e}")

exit()

3. Aller à /rapports/ - voir tous les mois
```

---

## 📱 Navigation dans l'App

```
Home (/)
├── Rapports (/rapports/) ← NEW!
│   ├── Liste des rapports
│   │   ├── Filtre par statut
│   │   ├── Pagination
│   │   └── Cartes avec stats
│   └── Détail (/rapports/1/) ← NEW!
│       ├── 8 sections
│       ├── 3 graphiques
│       └── Bouton retour
├── Membres
├── Statistiques
├── Analyse
└── Admin
    └── Rapports Mensuels ← Nouveau!
```

---

## 🔑 Comptes de Test

### Admins
- **Utilisateur**: admin
- **Mot de passe**: admin
- **Accès**: Tous les rapports + Admin

### Patriarches/Responsables
- Créer un compte lors de l'inscription
- Accès: Rapports (lecture)

---

## 📊 Données de Test

Le système génère automatiquement:
```
✓ 18 membres total
✓ 15 actifs, 2 nouveaux, 1 inactif, 0 sortis
✓ 2 tribus avec répartition
✓ 3 départements avec répartition
✓ 6 cultes (4 dimanche, 2 mercredi)
✓ 45 présences, 0 absences
✓ 100% taux de participation
```

---

## 🐛 Dépannage Rapide

### Problem: 404 Not Found
```
❌ /rapports/ → 404
Solution: 
1. Redémarrer le serveur
2. Vérifier: python manage.py check
```

### Problem: Pas de rapport généré
```
❌ Liste vide
Solution:
1. python generer_rapports.py
2. Rafraîchir la page
3. Aller à /admin/eglise/rapportmensuel/ pour vérifier
```

### Problem: Les graphiques ne s'affichent pas
```
❌ Cartes OK, mais graphiques vides
Solution:
1. F12 → Console
2. Vérifier les erreurs JavaScript
3. Vérifier que Chart.js se charge (onglet Réseau)
```

### Problem: Permission Denied
```
❌ Accès refusé
Solution:
1. Se connecter: /login/
2. Vérifier que l'utilisateur existe
3. Essayer avec: admin/admin
```

---

## 📚 Fichiers Importants

```
c:\projet\CCR\
├── generer_rapports.py          ← Script de génération
├── eglise/
│   ├── models.py                ← Modèle RapportMensuel
│   ├── views_rapports.py        ← Vues web (NEW)
│   ├── admin.py                 ← Admin interface
│   ├── urls.py                  ← Routes (NEW)
│   └── templates/eglise/
│       ├── rapport_mensuel_list.html      ← Détail (NEW)
│       └── rapport_mensuel_detail.html    ← Détail (NEW)
├── GUIDE_RAPPORTS_MENSUELS.md   ← Documentation détaillée
├── TEST_RAPPORTS_MENSUELS.md    ← Guide de test
└── validate_rapport_system.py   ← Validation

```

---

## ⏱️ Chronométrage

```
Configuration        : 30 secondes
Génération rapport   : 1 minute
Démarrage serveur    : 30 secondes
Accès à /rapports/   : 2-3 secondes
Affichage détails    : 2-3 secondes
---
Total               : ~5 minutes
```

---

## ✅ Checklist de Démarrage

- [ ] Terminal ouvert
- [ ] CD dans `c:\projet\CCR`
- [ ] Run: `python manage.py check` ✅
- [ ] Run: `python generer_rapports.py` ✅
- [ ] Run: `python manage.py runserver`
- [ ] Navigateur: `http://localhost:8000/`
- [ ] Se connecter (admin/admin)
- [ ] Cliquer "Rapports" dans menu
- [ ] Voir la liste
- [ ] Cliquer "Voir Détails"
- [ ] Voir les graphiques
- [ ] 🎉 Terminé!

---

## 🎯 Commandes Essentielles

```bash
# Configuration
python manage.py check

# Générer rapports
python generer_rapports.py

# Démarrer serveur
python manage.py runserver

# Admin shell
python manage.py shell
>>> from eglise.models import RapportMensuel
>>> RapportMensuel.objects.all().count()
>>> exit()

# Migrations
python manage.py showmigrations
python manage.py migrate

# Validation finale
python validate_rapport_system.py
```

---

## 🌐 URLs Principales

```
Accueil              : http://localhost:8000/
Login                : http://localhost:8000/login/
Rapports (liste)     : http://localhost:8000/rapports/ ← NEW
Rapport (détail)     : http://localhost:8000/rapports/1/ ← NEW
Admin rapports       : http://localhost:8000/admin/eglise/rapportmensuel/ ← NEW
Admin général        : http://localhost:8000/admin/
```

---

## 📞 Help & Support

### Si ça ne fonctionne pas:

1. **Lire**: GUIDE_RAPPORTS_MENSUELS.md
2. **Tester**: TEST_RAPPORTS_MENSUELS.md (phase par phase)
3. **Valider**: python validate_rapport_system.py
4. **Debugger**: Voir le dépannage ci-dessus

### Erreurs Communes:

```
"No such table: eglise_rapportmensuel"
→ python manage.py migrate

"Page not found (404)"
→ Redémarrer le serveur

"Permission Denied"
→ Se connecter avec admin/admin

"Les graphiques ne s'affichent pas"
→ Vérifier console navigateur (F12)
```

---

## 🚀 Vous êtes Prêt!

Commencez par cette commande:
```bash
cd c:\projet\CCR && python generer_rapports.py && python manage.py runserver
```

Puis ouvrez dans le navigateur:
```
http://localhost:8000/rapports/
```

**Bon développement! 🎉**

---

**Dernière mise à jour**: 4 Mai 2026  
**Version**: 2.0 Production  
**Statut**: ✅ Prêt à l'emploi
