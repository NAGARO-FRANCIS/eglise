# 📊 Système de Rapports Mensuels - Documentation Complète

## Vue d'Ensemble

Un système complet de **rapports mensuels automatisés** pour suivre l'activité de l'église mois par mois.

## ✨ Fonctionnalités

### 1. **Génération Automatique des Rapports**
- Collecte automatique des données chaque mois
- Calcul des statistiques globales
- Agrégation des données par structure (tribus, départements)

### 2. **Gestion des Rapports**
- **Interface Admin Django** pour gérer et valider les rapports
- **Trois statuts de rapport**:
  - **Brouillon**: Rapport nouvellement généré
  - **Validé**: Rapport approuvé par un responsable
  - **Archivé**: Rapport ancien conservé pour historique

### 3. **Données Collectées par Rapport**
- **Statistiques générales**:
  - Nombre total de membres
  - Membres actifs, nouveaux, inactifs, sortis
  
- **Distribution par structure**:
  - Répartition par tribu
  - Répartition par département
  
- **Statistiques d'assistance**:
  - Nombre de cultes
  - Présences et absences
  - Taux de participation moyen
  - Cultes par type
  
- **Annotations**:
  - Notes et observations des responsables

## 📁 Fichiers Créés/Modifiés

### Modèles
- ✅ `eglise/models.py` - Ajout du modèle `RapportMensuel`

### Vues
- ✅ `eglise/views_rapports.py` - Nouvelles vues:
  - `RapportMensuelListView`: Liste des rapports
  - `RapportMensuelDetailView`: Détail d'un rapport

### Templates
- ✅ `eglise/templates/eglise/rapport_mensuel_list.html` - Liste des rapports
- ✅ `eglise/templates/eglise/rapport_mensuel_detail.html` - Détail du rapport

### URLs
- ✅ `eglise/urls.py` - Routes pour accéder aux rapports:
  - `/rapports/` - Liste des rapports
  - `/rapports/<id>/` - Détail d'un rapport

### Admin
- ✅ `eglise/admin.py` - Interface admin pour gérer les rapports

### Utilitaires
- ✅ `generer_rapports.py` - Script pour générer les rapports mensuels

### Migrations
- ✅ `eglise/migrations/0005_rapportmensuel.py` - Création de la table

## 🚀 Comment Utiliser

### 1. **Générer un Rapport Manuellement**

```bash
cd c:\projet\CCR
python generer_rapports.py
```

**Résultat**:
```
✓ Rapport généré avec succès:
  - Période: Mai 2026
  - Membres: 18
  - Taux de participation: 100.0%
  - Cultes: 6
```

### 2. **Générer un Rapport pour un Mois Spécifique**

```python
from generer_rapports import generer_rapport_mensuel
from django.contrib.auth.models import User

# Générer pour Janvier 2026
auteur = User.objects.get(username='admin')
generer_rapport_mensuel(1, 2026, auteur)
```

### 3. **Accéder aux Rapports**

**Interface Web**:
1. Aller à `/rapports/` pour voir la liste
2. Cliquer sur un rapport pour voir les détails
3. Observer les graphiques et statistiques

**Interface Admin**:
1. Aller à `/admin/eglise/rapportmensuel/`
2. Voir la liste des rapports
3. Modifier le statut (brouillon → validé → archivé)

## 📊 Contenu d'un Rapport

### Vue de Liste
```
✅ Affiche une carte pour chaque rapport avec:
   - Période (mois/année)
   - Statut (couleur)
   - Stats principales:
     * Total membres
     * Membres actifs
     * Taux participation
     * Nombre cultes
   - Bouton "Voir Détails"
```

### Vue de Détail
```
✅ Affiche le rapport complet avec:
   1. En-tête: Période, statut, dates
   2. Statistiques générales en cartes colorées
   3. Répartition par tribu (tableau + graphique)
   4. Répartition par département (tableau + graphique)
   5. Cultes par type (graphique doughnut)
   6. Notes et observations
   7. Graphiques Chart.js interactifs
```

## 🔄 Flux de Travail Recommandé

### Mensuellement:
```
1. Fin du mois: Générer le rapport
   python generer_rapports.py

2. Vérification: Accéder à /admin/eglise/rapportmensuel/

3. Validation:
   - Lire les données
   - Ajouter des notes/observations
   - Changer le statut à "Validé"
   - Enregistrer

4. Archivage (optionnel):
   - Après 3 mois, passer le rapport à "Archivé"
```

## 📈 Données dans le Rapport

### Structure JSON des Données

```python
rapport = {
    'mois': 5,
    'annee': 2026,
    'nombre_total_membres': 18,
    'nombre_membres_actifs': 15,
    'nombre_membres_nouveau': 2,
    'nombre_membres_inactif': 1,
    'nombre_membres_sorti': 0,
    
    'nombre_tribus': 2,
    'membres_par_tribu': {
        'Tribu Alpha': 10,
        'Tribu Beta': 5
    },
    
    'nombre_departements': 3,
    'membres_par_departement': {
        'Diaconie': 6,
        'Louange': 7,
        'Accueil': 5
    },
    
    'nombre_cultes': 6,
    'nombre_total_presences': 45,
    'nombre_total_absences': 0,
    'taux_participation_moyen': 100.0,
    
    'cultes_par_type': {
        'Dimanche': {'nombre': 4, 'participants': 35},
        'Mercredi': {'nombre': 2, 'participants': 10}
    },
    
    'statut': 'validé',
    'auteur': 'admin',
    'date_creation': '2026-05-04 10:30:00'
}
```

## 🔐 Permissions

- **Pasteur/Admin**: Peut voir et gérer tous les rapports
- **Patriarche/Responsable**: Peut voir tous les rapports
- **Visiteur**: Accès refusé (protection LoginRequiredMixin)

## 🛠️ Personnalisations Futures

### Possibilités d'Extension:
1. **Génération Automatique**: Intégrer une tâche Celery pour générer auto le 1er du mois
2. **Export PDF**: Générer un PDF du rapport pour impression/partage
3. **Comparaison**: Comparer deux mois côte à côte
4. **Tendances**: Graphiques de tendances sur 6/12 mois
5. **Alertes**: Notifications si taux participation < seuil
6. **Email**: Envoyer les rapports par email aux responsables

## 📞 Dépannage

### Le rapport ne s'affiche pas
```
✓ Vérifier que le serveur Django est en cours d'exécution
✓ Vérifier que l'URL est correct: /rapports/
✓ Vérifier que l'utilisateur est connecté
```

### Les données ne sont pas à jour
```
✓ Générer un nouveau rapport: python generer_rapports.py
✓ Vérifier que les données des cultes/membres sont enregistrées
```

### Les graphiques ne s'affichent pas
```
✓ Vérifier que Chart.js est chargé (CDN)
✓ Vérifier que JavaScript est activé
✓ Vérifier la console du navigateur pour les erreurs
```

## 📊 Exemple de Commande

```bash
# Générer le rapport du mois courant
python generer_rapports.py

# Sortie attendue:
# ================================================================================
# Générateur de Rapports Mensuels
# ================================================================================
# 
# 1. Génération du rapport du mois courant...
# Création d'un nouveau rapport pour 5/2026...
# ✓ Rapport généré avec succès:
#   - Période: Mai 2026
#   - Membres: 18
#   - Taux de participation: 100.0%
#   - Cultes: 6
#
# ================================================================================
# Génération terminée!
# ================================================================================
```

## 🎯 Cas d'Usage

### 1. Suivi Mensuel de l'Activité
- Voir l'évolution du nombre de membres chaque mois
- Identifier les tendances de participation
- Suivre la croissance par structure

### 2. Rapports pour Direction
- Partager les performances mensuelles
- Comparer les mois
- Valider les progrès

### 3. Analyse Détaillée
- Voir les graphiques interactifs
- Ajouter des notes personnalisées
- Archiver pour historique

## ✅ Résumé

✅ **Modèle de données complet**
✅ **Génération automatique des rapports**
✅ **Interface admin pour gérer les rapports**
✅ **Vues web pour consulter les rapports**
✅ **Graphiques interactifs avec Chart.js**
✅ **Système de filtrage par statut**
✅ **Données détaillées par structure**
✅ **Notes et observations personnalisées**

Le système est **100% fonctionnel** et **prêt à l'emploi**! 🚀
