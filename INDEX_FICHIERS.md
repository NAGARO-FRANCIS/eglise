# 📑 Index des Fichiers du Projet

## Fichiers de Configuration Django

| Fichier | Rôle |
|---------|------|
| `manage.py` | Script de gestion principal Django |
| `db.sqlite3` | Base de données SQLite |
| `requirements.txt` | Liste des dépendances Python |
| `run.bat` | Script batch pour Windows (menu interactif) |

## Dossier `CCR/` - Projet Principal

| Fichier | Rôle |
|---------|------|
| `__init__.py` | Initialisation du projet |
| `settings.py` | Configuration Django (DB, INSTALLED_APPS, TEMPLATES, etc.) |
| `urls.py` | Routage des URLs principales (`/admin/` et inclusion de eglise.urls) |
| `asgi.py` | Configuration pour serveur ASGI |
| `wsgi.py` | Configuration pour serveur WSGI |

## Dossier `eglise/` - Application Django

### Configuration de l'Application
| Fichier | Rôle |
|---------|------|
| `__init__.py` | Initialisation (vide) |
| `apps.py` | Configuration de l'application (EgliseConfig) |

### Logique Métier
| Fichier | Rôle |
|---------|------|
| `models.py` | Modèles de données (Tribu, Departement, Membre, Culte, Presence, Statistique) |
| `views.py` | 4 vues principales (Dashboard, MembreList, Statistiques, Analyse) |
| `admin.py` | Configuration admin Django (6 admin classes enrichies) |
| `urls.py` | Routage des URLs de l'app (4 routes) |

### Base de Données
| Fichier | Rôle |
|---------|------|
| `migrations/__init__.py` | Initialisation des migrations |
| `migrations/0001_initial.py` | Migration initiale (création de toutes les tables) |

### Templates HTML
| Fichier | Rôle |
|---------|------|
| `templates/eglise/base.html` | Template parent avec navigation et styles CSS |
| `templates/eglise/dashboard.html` | Tableau de bord avec KPI principales |
| `templates/eglise/membre_list.html` | Liste des membres avec filtres avancés |
| `templates/eglise/statistiques.html` | Statistiques détaillées et tendances |
| `templates/eglise/analyse.html` | Analyse approfondie par tribu/département |

### Tests et Autres
| Fichier | Rôle |
|---------|------|
| `tests.py` | (Vide - prêt pour ajouter des tests) |
| `admin_customization.py` | Personnalisation du site admin |

## Fichiers de Documentation

| Fichier | Rôle |
|---------|------|
| `README.md` | 📘 Documentation complète du projet (>500 lignes) |
| `GUIDE_DEMARRAGE.md` | 🚀 Guide de démarrage rapide avec commandes |
| `RESUME_PROJET.md` | 📋 Résumé des fonctionnalités implémentées |
| `INDEX_FICHIERS.md` | 📑 Ce fichier - index de tous les fichiers |

## Scripts Utilitaires

| Fichier | Rôle |
|---------|------|
| `load_demo_data.py` | 📊 Script pour charger 30 membres + 15 cultes de test |
| `test_installation.py` | ✅ Script de validation d'installation |

---

## Répartition par Fonctionnalité

### 🏛️ Architecture Django
- `manage.py`
- `CCR/settings.py`
- `CCR/urls.py`
- `eglise/apps.py`
- `eglise/models.py`
- `eglise/urls.py`

### 🖥️ Interface Web
- `eglise/views.py` (4 vues)
- `eglise/templates/eglise/base.html`
- `eglise/templates/eglise/dashboard.html`
- `eglise/templates/eglise/membre_list.html`
- `eglise/templates/eglise/statistiques.html`
- `eglise/templates/eglise/analyse.html`

### 🔧 Administration
- `eglise/admin.py` (6 admin classes)
- `eglise/admin_customization.py`

### 📊 Base de Données
- `db.sqlite3` (données)
- `eglise/migrations/0001_initial.py` (schéma)

### 📝 Documentation
- `README.md`
- `GUIDE_DEMARRAGE.md`
- `RESUME_PROJET.md`

### ⚙️ Scripts
- `load_demo_data.py`
- `test_installation.py`
- `run.bat`

### 📦 Configuration
- `requirements.txt`
- `.gitignore` (recommandé - non inclus)

---

## Structure Visuelle

```
c:\projet\CCR/
│
├── 📄 manage.py                      (Commande principale Django)
├── 💾 db.sqlite3                     (Base de données SQLite)
├── 📋 requirements.txt               (Dépendances)
├── ⚡ run.bat                        (Menu Windows)
├── 🔧 load_demo_data.py             (Données test)
├── ✅ test_installation.py          (Validation)
│
├── 📖 README.md                      (Doc complète)
├── 🚀 GUIDE_DEMARRAGE.md            (Guide rapide)
├── 📊 RESUME_PROJET.md              (Résumé)
├── 📑 INDEX_FICHIERS.md             (Index)
│
├── 📁 CCR/                          (Projet Django)
│   ├── __init__.py
│   ├── settings.py                  (Config + INSTALLED_APPS)
│   ├── urls.py                      (Routes principales)
│   ├── asgi.py
│   └── wsgi.py
│
└── 📁 eglise/                       (Application Django)
    ├── __init__.py
    ├── apps.py                      (Configuration)
    ├── models.py                    (6 modèles)
    ├── views.py                     (4 vues)
    ├── admin.py                     (Admin enrichie)
    ├── urls.py                      (4 routes)
    ├── tests.py
    ├── admin_customization.py
    ├── 📁 migrations/
    │   ├── __init__.py
    │   └── 0001_initial.py
    └── 📁 templates/eglise/
        ├── base.html                (Template parent)
        ├── dashboard.html           (Accueil)
        ├── membre_list.html         (Liste)
        ├── statistiques.html        (Stats)
        └── analyse.html             (Analyse)
```

---

## Taille Approximative par Catégorie

| Catégorie | Fichiers | Lignes de Code |
|-----------|----------|----------------|
| Configuration | 5 | 200+ |
| Modèles Django | 1 | 250+ |
| Vues | 1 | 150+ |
| Templates | 5 | 600+ |
| Admin Django | 1 | 180+ |
| Documentation | 4 | 1500+ |
| Scripts | 2 | 250+ |
| **TOTAL** | **19** | **3130+** |

---

## Fichiers à Ne Pas Supprimer

⚠️ **Critiques**:
- `manage.py` - Gestion Django
- `db.sqlite3` - Données
- `eglise/models.py` - Structure données
- `CCR/settings.py` - Configuration
- `CCR/urls.py` - Routage

⚠️ **Importants**:
- `eglise/views.py` - Logique métier
- `eglise/admin.py` - Interface admin
- `eglise/templates/` - Interface web

---

## Fichiers Optionnels

📦 **Peuvent être supprimés sans casser le projet**:
- `test_installation.py` - Script de test
- `load_demo_data.py` - Données de démo
- Documentation (pour production)

---

## Points de Modification Courants

### Pour Ajouter une Nouvelle Fonctionnalité:
1. Modifier `eglise/models.py`
2. Créer migration: `python manage.py makemigrations`
3. Ajouter vue dans `eglise/views.py`
4. Ajouter URL dans `eglise/urls.py`
5. Créer template dans `eglise/templates/eglise/`
6. Ajouter admin dans `eglise/admin.py` (si nécessaire)

### Pour Personnaliser le Design:
- Modifier CSS dans `eglise/templates/eglise/base.html`
- Ou créer un fichier `eglise/static/css/style.css`

### Pour Configurer la Base de Données:
- Modifier `CCR/settings.py` section `DATABASES`

---

## Recommandations Git

Fichiers à ajouter à `.gitignore`:
```
*.pyc
__pycache__/
*.egg-info/
.env
.venv/
venv/
env/
*.sqlite3
*.db
.DS_Store
.vscode/
.idea/
```

---

**Dernière mise à jour**: 27 Avril 2026  
**Version du Projet**: 1.0  
**Statut**: ✅ Complet et Fonctionnel
