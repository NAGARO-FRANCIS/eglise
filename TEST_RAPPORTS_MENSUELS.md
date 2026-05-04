# 🧪 Guide de Test - Système de Rapports Mensuels

## Checklist de Validation Complète

### ✅ Phase 1: Configuration & Déploiement

- [ ] **Configuration Django**
  ```bash
  python manage.py check
  # Résultat attendu: "System check identified no issues (0 silenced)"
  ```

- [ ] **Migrations appliquées**
  ```bash
  python manage.py showmigrations
  # Vérifier que eglise 0005_rapportmensuel est "X" (appliquée)
  ```

### ✅ Phase 2: Génération des Données

- [ ] **Générer un rapport de test**
  ```bash
  python generer_rapports.py
  # Résultat attendu: Rapport généré pour le mois courant
  ```

- [ ] **Vérifier les données en Django Shell**
  ```bash
  python manage.py shell
  >>> from eglise.models import RapportMensuel
  >>> rapport = RapportMensuel.objects.last()
  >>> print(f"Rapport: {rapport.periode_str}")
  >>> print(f"Membres: {rapport.nombre_total_membres}")
  >>> print(f"Taux: {rapport.taux_participation_moyen}%")
  >>> exit()
  ```

### ✅ Phase 3: Interface Admin

- [ ] **Accéder à l'admin des rapports**
  1. Lancer le serveur: `python manage.py runserver`
  2. Aller à: `http://localhost:8000/admin/eglise/rapportmensuel/`
  3. Voir la liste des rapports générés
  4. Vérifier les colonnes: Période, Membres, Taux participation, Statut
  5. Cliquer sur un rapport pour voir les détails
  6. Modifier le statut (brouillon → validé)
  7. Ajouter une note
  8. Enregistrer

**Observations à Vérifier**:
- ✓ La liste affiche les rapports
- ✓ Les badges de statut sont colorés
- ✓ Les champs sont accessibles en édition
- ✓ L'enregistrement fonctionne

### ✅ Phase 4: Interface Web - Liste des Rapports

- [ ] **Accéder à la liste des rapports**
  1. URL: `http://localhost:8000/rapports/`
  2. Voir les cartes des rapports

**Validations**:
- ✓ Page affiche les rapports sous forme de cartes
- ✓ Chaque carte montre:
  - Période (ex: "📅 Mai 2026")
  - Statut (badge coloré)
  - 4 statistiques: Membres, Actifs, Participation%, Cultes
  - Bouton "Voir Détails"
- ✓ Filtrage par statut fonctionne (Tous, Validés, Brouillons, Archivés)
- ✓ Pagination affiche 12 rapports par page
- ✓ Lien "Voir Détails" fonctionne

### ✅ Phase 5: Interface Web - Détail du Rapport

- [ ] **Accéder au détail d'un rapport**
  1. Depuis la liste, cliquer sur "Voir Détails"
  2. URL devrait être: `http://localhost:8000/rapports/1/`

**Validations**:
- ✓ En-tête affiche la période, statut, date création, auteur
- ✓ **Section Statistiques Générales**: 5 cartes colorées
  - Membres Total
  - Membres Actifs (vert)
  - Nouveaux (bleu)
  - Inactifs (orange)
  - Sortis (rouge)
- ✓ **Section Structures**: 2 cartes
  - Nombre de tribus
  - Nombre de départements
- ✓ **Section Répartition par Tribu**: 
  - Tableau avec noms et nombres
  - Graphique bar chart
- ✓ **Section Répartition par Département**:
  - Tableau avec noms et nombres
  - Graphique bar chart
- ✓ **Section Statistiques d'Assistance**: 4 cartes
  - Cultes tenus
  - Présences
  - Absences
  - Taux participation (%)
- ✓ **Section Cultes par Type**:
  - Tableau avec type, nombre, participants
  - Graphique doughnut coloré
- ✓ **Graphiques Chart.js**:
  - Les 3 graphiques s'affichent correctement
  - Les couleurs correspondent aux données
  - Les graphiques sont interactifs
- ✓ Bouton "Retour aux rapports" fonctionne

### ✅ Phase 6: Navigation Menu

- [ ] **Vérifier le menu de navigation**
  1. Se connecter au site
  2. Voir la navigation en haut
  3. Observer les liens: Accueil, Membres, Statistiques, Analyse, **Rapports**, Administration
  4. Cliquer sur "Rapports"
  5. Être redirigé vers `/rapports/`

### ✅ Phase 7: Génération pour Mois Spécifique

- [ ] **Générer un rapport pour un mois passé (Python Shell)**
  ```bash
  python manage.py shell
  >>> from generer_rapports import generer_rapport_mensuel
  >>> from django.contrib.auth.models import User
  >>> from datetime import datetime
  >>> 
  >>> auteur = User.objects.get(username='admin')
  >>> generer_rapport_mensuel(4, 2026, auteur)  # Avril 2026
  >>> generer_rapport_mensuel(3, 2026, auteur)  # Mars 2026
  >>> 
  >>> from eglise.models import RapportMensuel
  >>> rapports = RapportMensuel.objects.all().order_by('-annee', '-mois')
  >>> for r in rapports:
  ...     print(f"{r.periode_str}: {r.nombre_total_membres} membres")
  >>> exit()
  ```

### ✅ Phase 8: Permissions et Sécurité

- [ ] **Tester l'accès non-authentifié**
  1. Se déconnecter (Logout)
  2. Aller à `/rapports/`
  3. Être redirigé vers la page de login
  4. ✓ Accès protégé

- [ ] **Tester avec utilisateur ordinaire**
  1. Se connecter avec un utilisateur non-admin
  2. Aller à `/rapports/`
  3. Voir les rapports
  4. ✓ Pas d'erreur 403

### ✅ Phase 9: Données Cohérence

- [ ] **Vérifier les données calculées**
  1. Accéder au détail d'un rapport
  2. Verifier que:
     - `nombre_membres_actifs + nombre_membres_nouveau + nombre_membres_inactif + nombre_membres_sorti = nombre_total_membres` (approximativement)
     - `taux_participation_moyen` est entre 0 et 100%
     - `nombre_total_presences + nombre_total_absences > 0` (si cultes)
     - Les dictionnaires JSON affichent correctement

### ✅ Phase 10: Performance & Stabilité

- [ ] **Tester avec plusieurs rapports**
  ```bash
  python manage.py shell
  >>> from generer_rapports import generer_rapport_mensuel
  >>> from django.contrib.auth.models import User
  >>> auteur = User.objects.first()
  >>> 
  >>> # Générer 12 mois de rapports
  >>> for month in range(1, 13):
  ...     generer_rapport_mensuel(month, 2025, auteur)
  ...
  >>> # Vérifier la pagination
  >>> exit()
  ```
  1. Aller à `/rapports/`
  2. Vérifier que la pagination fonctionne (12 par page)
  3. Cliquer "Suivante" pour voir plus de rapports

- [ ] **Vérifier les performances**
  - La page de liste charge rapidement (< 1s)
  - La page de détail charge rapidement (< 2s)
  - Pas d'erreurs en console

### ✅ Phase 11: Graphiques Avancés

- [ ] **Test des graphiques**
  1. Aller au détail d'un rapport
  2. Vérifier chaque graphique:
     - Bar chart (tribus): Barres bien espacées
     - Bar chart (départements): Valeurs corrects
     - Doughnut chart (cultes): Couleurs variées
  3. Passer la souris sur les graphiques
  4. Voir les tooltips avec les valeurs

### ✅ Phase 12: Édition Admin

- [ ] **Tester la modification en admin**
  1. Aller à `/admin/eglise/rapportmensuel/`
  2. Cliquer sur un rapport
  3. Changer le statut de "brouillon" à "validé"
  4. Ajouter une note: "Test de validation"
  5. Cliquer "Enregistrer"
  6. Voir le message de succès
  7. Retourner à la liste
  8. Vérifier que le statut s'est changé

### ✅ Phase 13: Cas d'Erreur

- [ ] **Test d'erreur 404**
  1. Aller à `/rapports/99999/` (ID inexistant)
  2. Voir une page 404 propre

- [ ] **Test de pagination hors limites**
  1. Aller à `/rapports/?page=99999`
  2. Voir une page 404 ou redirection

## 📝 Feuille de Résultats

```
Date: ___________
Testeur: ___________

[Phase 1] Configuration & Déploiement
  ☐ Configuration OK
  ☐ Migrations OK
  Résultat: ___________

[Phase 2] Génération des Données
  ☐ Rapport généré
  ☐ Shell verification OK
  Résultat: ___________

[Phase 3] Admin Interface
  ☐ Admin accessible
  ☐ Rapports visibles
  ☐ Édition fonctionne
  Résultat: ___________

[Phase 4] Web List
  ☐ Liste affiche OK
  ☐ Cartes correctes
  ☐ Filtrage OK
  ☐ Pagination OK
  Résultat: ___________

[Phase 5] Web Detail
  ☐ Detail page OK
  ☐ Sections affichées
  ☐ Graphiques OK
  Résultat: ___________

[Phase 6] Navigation
  ☐ Menu updated
  ☐ Lien "Rapports" OK
  Résultat: ___________

[Phase 7] Multiple Months
  ☐ Générations OK
  ☐ Historique visible
  Résultat: ___________

[Phase 8] Permissions
  ☐ Non-auth blocked
  ☐ User access OK
  Résultat: ___________

[Phase 9] Data Integrity
  ☐ Calculs OK
  ☐ JSON correct
  Résultat: ___________

[Phase 10] Performance
  ☐ Load time OK
  ☐ Pagination OK
  Résultat: ___________

[Phase 11] Charts
  ☐ All charts OK
  ☐ Interactions OK
  Résultat: ___________

[Phase 12] Admin Edit
  ☐ Status change OK
  ☐ Note saving OK
  Résultat: ___________

[Phase 13] Error Handling
  ☐ 404 page OK
  ☐ Invalid page OK
  Résultat: ___________

RÉSULTAT FINAL: ___________
```

## 🐛 Dépannage

### Problem: "Page not found (404)" pour /rapports/

**Solutions:**
```
1. Vérifier que l'URL est dans eglise/urls.py:
   - path('rapports/', views_rapports.RapportMensuelListView.as_view(), name='rapports_list')
   
2. Vérifier que views_rapports est importé:
   - from . import views_rapports
   
3. Vérifier que le serveur est redémarré après modifications
```

### Problem: "No such table: eglise_rapportmensuel"

**Solutions:**
```
1. Appliquer les migrations:
   python manage.py migrate
   
2. Vérifier la migration existe:
   python manage.py showmigrations | grep rapport
```

### Problem: Les graphiques ne s'affichent pas

**Solutions:**
```
1. Vérifier la console du navigateur (F12 → Console)
2. Vérifier que Chart.js se charge (réseau)
3. Vérifier que les données JSON sont valides
```

### Problem: "Permission Denied" en accédant aux rapports

**Solutions:**
```
1. Vérifier que vous êtes connecté
2. Vérifier que le LoginRequiredMixin est présenent
3. Vérifier les permissions Django
```

## 🎉 Résultat Attendu

Après tous les tests, vous devriez avoir:
- ✅ 1 page de liste des rapports avec filtrage
- ✅ 1 page de détail avec 8 sections
- ✅ 3 graphiques Chart.js interactifs
- ✅ Admin interface complète
- ✅ Génération automatique fonctionnelle
- ✅ Menu de navigation mis à jour
- ✅ Sécurité et permissions correctes

**État**: 🟢 PRÊT POUR LA PRODUCTION
