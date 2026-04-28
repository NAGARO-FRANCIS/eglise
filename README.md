# 🏛️ Application de Gestion d'Église - Suivi et Analyse

## 📋 Vue d'ensemble

Cette application Django permet de gérer et analyser les membres d'une église, suivi des présences aux cultes, statistiques et tendances de participation.

## ✨ Fonctionnalités principales

### 1. **Gestion des Membres**
- Enregistrement des informations personnelles (nom, prénom, email, téléphone, adresse)
- Gestion du statut (Nouveau, Actif, Inactif, Sorti)
- Attribution à une tribu et un département
- Suivi de la date d'adhésion et de départ
- Calcul automatique du taux de participation

### 2. **Organisation de l'Église**
- **Tribus** : Groupes de membres avec responsable
- **Départements** : Services/ministères avec responsable
- Gestion hiérarchique et organisationnelle

### 3. **Suivi des Cultes**
- Enregistrement des cultes (date, type, thème, prédicateur)
- Types de cultes : Dimanche, Mercredi, Spécial, Autre
- Suivi automatique du nombre de participants

### 4. **Gestion des Présences**
- Enregistrement des présences/absences à chaque culte
- Relation unique membre-culte pour éviter les doublons
- Historique complet des présences

### 5. **Statistiques et Analyses**
- **Dashboard** : Vue d'ensemble avec KPI principales
- **Statistiques** : Tendances de participation, évolution des membres
- **Analyse** : Détails par tribu, département et tendances hebdomadaires
- **Top Participants** : Classement des membres les plus assidus

## 🎯 Structure du Projet

```
c:\projet\CCR/
├── CCR/                          # Dossier du projet Django
│   ├── __init__.py
│   ├── settings.py              # Configuration Django
│   ├── urls.py                  # URLs principales
│   ├── wsgi.py
│   └── asgi.py
├── eglise/                        # Application Django
│   ├── migrations/              # Migrations de base de données
│   ├── templates/eglise/        # Templates HTML
│   │   ├── base.html           # Template de base
│   │   ├── dashboard.html      # Tableau de bord
│   │   ├── membre_list.html    # Liste des membres
│   │   ├── statistiques.html   # Statistiques
│   │   └── analyse.html        # Analyse
│   ├── models.py               # Modèles de données
│   ├── views.py                # Vues et logique métier
│   ├── admin.py                # Configuration admin
│   ├── urls.py                 # URLs de l'application
│   ├── tests.py                # Tests
│   └── apps.py                 # Configuration app
├── db.sqlite3                    # Base de données
├── manage.py                     # Script de gestion Django
└── README.md                     # Cette documentation
```

## 🔧 Installation et Configuration

### 1. **Prérequis**
- Python 3.7+
- Django 6.0+
- pip

### 2. **Installation des dépendances**
```bash
pip install django
```

### 3. **Appliquer les migrations**
```bash
cd c:\projet\CCR
python manage.py migrate
```

### 4. **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```
Lors de la création:
- **Username** : admin
- **Email** : admin@eglise.com
- **Password** : (à définir)

### 5. **Démarrer le serveur**
```bash
python manage.py runserver
```

Le serveur démarre sur `http://localhost:8000`

## 🌐 Accès à l'Application

### Routes Disponibles

| URL | Description |
|-----|-------------|
| `/` | **Accueil/Dashboard** - Vue d'ensemble avec statistiques |
| `/membres/` | **Liste des Membres** - Avec filtres avancés |
| `/statistiques/` | **Statistiques Détaillées** - Tendances et évolution |
| `/analyse/` | **Analyse** - Détails par tribu/département |
| `/admin/` | **Interface Admin Django** - Gestion complète |

## 📊 Modèles de Données

### Tribu
- `nom` : Nom unique de la tribu
- `description` : Description optionnelle
- `date_creation` : Date de création automatique

### Departement
- `nom` : Nom unique du département
- `responsable` : Nom du responsable
- `description` : Description optionnelle
- `date_creation` : Date de création automatique

### Membre
- **Infos Personnelles** : nom, prénom, email, téléphone, adresse, genre, date_naissance
- **Infos d'Église** : tribu, departement, statut, date_adhesion, date_depart
- **Métadonnées** : date_creation, date_modification
- **Statuts** : Nouveau, Actif, Inactif, Sorti
- Calcul automatique du taux de participation (3 derniers mois)

### Culte
- `date` : Date du culte
- `type_culte` : Type (Dimanche, Mercredi, Spécial, Autre)
- `theme` : Thème du culte
- `predicateur` : Nom du prédicateur
- `nombre_participants` : Compté automatiquement
- `notes` : Notes optionnelles

### Presence
- `membre` : Référence au membre (ForeignKey)
- `culte` : Référence au culte (ForeignKey)
- `present` : Booléen (Présent/Absent)
- `date_enregistrement` : Date d'enregistrement automatique
- **Contrainte unique** : Un membre ne peut avoir qu'une présence par culte

### Statistique
- `date` : Date de la statistique
- `nombre_total_membres` : Total des membres
- `nombre_membres_actifs` : Membres actifs
- `nombre_membres_nouveau` : Nouveaux membres
- `nombre_membres_sorti` : Membres sortis
- `taux_participation_moyen` : Taux moyen de participation

## 🎨 Interface Admin Django

L'interface admin offre:

### ✅ Fonctionnalités Avancées
- Recherche par nom, email, téléphone
- Filtres par statut, genre, tribu, département
- Affichage du taux de participation
- Badges de couleur pour les statuts
- Inline editing pour les présences
- Metadonnées en sections repliables

### 🔐 Contrôles d'Accès
- Responsable de département
- Patriarche de tribu
- Administrateur système

## 📈 Tableaux de Bord et Rapports

### Dashboard Principal
- **KPI** : Total, Actifs, Nouveaux, Sortis, Taux participation
- **Répartition** : Membres par tribu et département
- **Cultes Récents** : Historique des 10 derniers cultes
- **Répartition par Statut** : Graphique de distribution

### Statistiques
- **Top 10 Participants** : Classement des plus assidus
- **Participation par Mois** : Tendances sur 3 mois
- **Évolution des Membres** : Historique complet

### Analyse
- **Par Tribu** : Distribution et taux d'activité
- **Par Département** : Distribution et taux d'activité
- **Tendances Hebdomadaires** : Variation de participation
- **Résumé d'Utilité** : Guide des objectifs de l'analyse

## 💡 Cas d'Usage

### Pour le Pasteur/Responsable
- Voir l'état global de l'église
- Identifier les members inactifs
- Analyser les tendances de participation
- Prendre des décisions basées sur les données

### Pour l'Administrateur
- Gérer tous les membres et leurs infos
- Enregistrer les cultes et présences
- Générer des rapports
- Maintenir la base de données

### Pour les Responsables de Tribu/Département
- Voir les membres de leur groupe
- Suivre les présences
- Identifier les personnes à contacter

## 🔄 Workflow Type

1. **Enregistrement d'un nouveau membre**
   - Admin ajoute le membre dans l'interface admin
   - Assigne tribu et département
   - Définit statut "Nouveau"

2. **Enregistrement d'un culte**
   - Admin crée le culte avec date, type, thème
   - Ajoute les présences (en masse ou individuellement)

3. **Suivi des statistiques**
   - Dashboard se met à jour automatiquement
   - Rapports disponibles via menu

4. **Analyse et décisions**
   - Revue des tendances
   - Identification des besoin de suivi

## 🛠️ Maintenance

### Sauvegarde de la Base de Données
```bash
# La base SQLite est automatiquement créée en db.sqlite3
# À sauvegarder régulièrement
```

### Création de Nouvelles Migrations
```bash
# Après modification des modèles
python manage.py makemigrations
python manage.py migrate
```

## 📝 Notes de Configuration

- **Langage** : Français pour l'interface et les données
- **Base de Données** : SQLite (db.sqlite3) - développement
- **Format de Date** : JJ/MM/AAAA
- **Timezone** : À configurer dans settings.py si nécessaire

## 🎓 Améliorations Futures Possibles

- [ ] Export des données (CSV, PDF)
- [ ] Graphiques interactifs (Chart.js)
- [ ] SMS/Email automatiques
- [ ] API REST
- [ ] Application mobile
- [ ] Intégration calendrier
- [ ] Gestion des événements spéciaux
- [ ] Système de permis/droits granulaire
- [ ] Audit trail complet
- [ ] Dashboard temps réel

## 📞 Support

Pour toute question ou problème, veuillez contacter l'administrateur du système.

---

**Version** : 1.0  
**Date** : 27 Avril 2026  
**Auteur** : [À compléter]
