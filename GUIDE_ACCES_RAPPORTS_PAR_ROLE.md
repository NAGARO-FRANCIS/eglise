# 📊 ACCÈS AUX RAPPORTS - GUIDE COMPLÈTE

## 🎯 Vue d'ensemble

Chaque tribu et département a maintenant **accès à son propre rapport mensuel** généré automatiquement.

### ✅ Génération automatique
- ✅ **Quand**: Le 1er du mois à 00:15 UTC
- ✅ **Quoi**: 1 rapport global + 1 par tribu + 1 par département
- ✅ **Comment**: Automatique (APScheduler)

---

## 🔑 Accès selon votre rôle

### 👑 Patriarche de Tribu

**Accès:**
```
http://localhost:8000/mon-rapport-tribu/
```

**Que vous verrez:**
- ✅ Rapport de VOTRE tribu (dernier mois)
- ✅ Statistiques des membres de votre tribu
- ✅ Répartition par département (dans votre tribu)
- ✅ Cultes et participation
- ✅ Historique des 12 derniers rapports

**Exemple:**
```
Patriarche de la Tribu "Benjamin"
→ Voit le rapport de la Tribu "Benjamin"
→ Voit les départements dans sa tribu
→ Voit l'historique de ses rapports
```

---

### 👔 Responsable de Département

**Accès:**
```
http://localhost:8000/mon-rapport-departement/
```

**Que vous verrez:**
- ✅ Rapport de VOTRE département (dernier mois)
- ✅ Statistiques des membres de votre département
- ✅ Répartition par tribu (dans votre département)
- ✅ Cultes et participation
- ✅ Historique des 12 derniers rapports

**Exemple:**
```
Responsable du Département "Adultes"
→ Voit le rapport du Département "Adultes"
→ Voit les tribus dans son département
→ Voit l'historique de ses rapports
```

---

### 📋 Pasteur / Administrateur

**Accès:**
```
http://localhost:8000/rapports/
```

**Que vous verrez:**
- ✅ TOUS les rapports (global, tribus, départements)
- ✅ Liste complète avec pagination
- ✅ Filtres par statut/structure/année
- ✅ Lien vers chaque rapport détaillé

---

## 📅 Calendrier de génération

Les rapports sont générés **le 1er du mois** à 00:15 UTC:

| Date | Rapport généré | Pour |
|------|---|---|
| 1er juin 2026 | Mai 2026 | Global + Tribus + Départements |
| 1er juillet 2026 | Juin 2026 | Global + Tribus + Départements |
| 1er août 2026 | Juillet 2026 | Global + Tribus + Départements |

---

## 📊 Données dans chaque rapport

### Pour Patriarches (Rapport Tribu)

```
📊 Rapport Tribu "Benjamin" - Juin 2026

👥 Statistiques des Membres:
  - Total: 25
  - Actifs: 23 ✅
  - Nouveaux: 2 🆕
  - Inactifs: 0
  - Partis: 0

📍 Répartition par Département:
  - Enfants: 8
  - Jeunes: 10
  - Adultes: 7

⛪ Assistance:
  - Cultes: 4
  - Présences: 92
  - Absences: 8
  - Taux de participation: 92%

📋 Types de cultes:
  - Dimanche matin: 80 participants
  - Prière du soir: 12 participants
```

### Pour Responsables (Rapport Département)

```
📊 Rapport Département "Adultes" - Juin 2026

👥 Statistiques des Membres:
  - Total: 45
  - Actifs: 42 ✅
  - Nouveaux: 3 🆕
  - Inactifs: 2
  - Partis: 1

📍 Répartition par Tribu:
  - Benjamin: 15
  - Judah: 18
  - David: 12

⛪ Assistance:
  - Cultes: 4
  - Présences: 156
  - Absences: 24
  - Taux de participation: 87%

📋 Types de cultes:
  - Dimanche matin: 140 participants
  - Prière du soir: 16 participants
```

---

## 🔐 Sécurité

✅ **Chaque rôle voit UNIQUEMENT ce qu'il doit voir:**
- Patriarche → Sa tribu uniquement
- Responsable → Son département uniquement
- Admin/Pasteur → Tous les rapports

✅ **Contrôle d'accès strict:**
- Si un patriarche essaie d'accéder à un autre rapport → Erreur 404
- Si un responsable essaie d'accéder à un autre rapport → Erreur 404

---

## 🎓 Cas d'usage

### Patriarche Benjamin

```
1. Se connecte: http://localhost:8000/
2. Accède à son rapport: /mon-rapport-tribu/
3. Voit le rapport de sa tribu (dernier mois)
4. Analyse les données:
   - Comment vont les membres?
   - Quel est le taux d'assistance?
   - Comment évolue la tribu?
5. Partage les insights avec son équipe
```

### Responsable du Département Adultes

```
1. Se connecte: http://localhost:8000/
2. Accède à son rapport: /mon-rapport-departement/
3. Voit le rapport de son département (dernier mois)
4. Vérifie:
   - Nombre de participants aux cultes
   - Répartition par tribu
   - Nouveaux membres
5. Rapporte à la direction
```

### Administrateur

```
1. Se connecte: http://localhost:8000/
2. Accède à tous les rapports: /rapports/
3. Valide/valide les rapports générés automatiquement
4. Consulte les statistiques globales
5. Génère des rapports mensuels personnalisés
```

---

## 🚀 Démarrage

### Étape 1: Lancer le serveur
```bash
python manage.py runserver
```

### Étape 2: Se connecter
```
http://localhost:8000/login/
```

### Étape 3: Accéder à votre rapport
- **Patriarche**: http://localhost:8000/mon-rapport-tribu/
- **Responsable**: http://localhost:8000/mon-rapport-departement/
- **Admin**: http://localhost:8000/rapports/

---

## ⚠️ Notes importantes

### Génération des rapports
- Les rapports sont générés **automatiquement** le 1er du mois
- Vous n'avez rien à faire!
- Ils sont générés pour **TOUS les mois** dès maintenant

### Statut des rapports
- Après génération: **Brouillon** (pas encore validé)
- L'admin peut les passer à: **Validé** ou **Archivé**

### Données historiques
- Les rapports des 12 derniers mois sont affichés
- Vous pouvez consulter l'évolution mois par mois

---

## 📱 Questions fréquentes

### Q: Comment je vois mon rapport?
**R:** Allez à `/mon-rapport-tribu/` (patriarche) ou `/mon-rapport-departement/` (responsable)

### Q: Quand les rapports sont générés?
**R:** Le 1er du mois à 00:15 UTC (c'est automatique)

### Q: Pourquoi je ne vois pas le rapport de cette tribu?
**R:** Seul le patriarche de cette tribu peut le voir (sécurité)

### Q: Puis-je modifier le rapport?
**R:** Non, les rapports sont générés automatiquement et sont en lecture seule

### Q: Quand voir le rapport de juin?
**R:** À partir du 1er juillet à 00:15 UTC

---

## 📞 Dépannage

### Le lien `/mon-rapport-tribu/` ne fonctionne pas
→ Vérifiez que vous êtes un patriarche avec une tribu assignée

### Le lien `/mon-rapport-departement/` ne fonctionne pas
→ Vérifiez que vous êtes un responsable avec un département assigné

### "Aucun rapport n'existe encore"
→ Les rapports seront générés le 1er du mois. Revenez demain!

### Les données ne sont pas à jour
→ Les rapports capturent les données du mois précédent
→ Revenez le 1er du mois pour les dernières données

---

**✅ Le système est prêt! Chaque structure voit son propre rapport mensuel.**
