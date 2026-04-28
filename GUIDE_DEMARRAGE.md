# 🚀 Guide de Démarrage Rapide

## Installation Rapide (Windows)

### 1. Installer Python et Django

```bash
# Installer les dépendances
pip install -r requirements.txt
```

### 2. Préparer la Base de Données

```bash
# Appliquer les migrations
python manage.py migrate

# Créer un administrateur
python manage.py createsuperuser
```

### 3. Démarrer le Serveur

```bash
# Lancer le serveur
python manage.py runserver

# Ou utiliser le fichier batch (Windows)
run.bat
```

### 4. Accéder à l'Application

- **Interface Web** : http://localhost:8000
- **Administration** : http://localhost:8000/admin

## Commandes Essentielles

### Gestion de la Base de Données

```bash
# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Revenir à une migration spécifique
python manage.py migrate eglise 0001
```

### Gestion des Utilisateurs

```bash
# Créer un superutilisateur
python manage.py createsuperuser

# Créer un superutilisateur sans interaction
python manage.py createsuperuser --username admin --email admin@eglise.com --noinput

# Shell Django pour manipulation avancée
python manage.py shell
```

### Données de Démonstration

```bash
# Charger les données de démonstration
python manage.py shell < load_demo_data.py
```

### Maintenance

```bash
# Vérifier les problèmes
python manage.py check

# Collecter les fichiers statiques (production)
python manage.py collectstatic

# Créer un backup de la base de données
copy db.sqlite3 db.sqlite3.backup
```

## Accès à l'Administration

### Connexion

1. Aller à http://localhost:8000/admin
2. Entrer les identifiants créés lors de `createsuperuser`
3. Cliquer sur "Se connecter"

### Gestion des Données

#### Ajouter un Nouveau Membre
1. Cliquer sur "Membres" → "+ Ajouter Membre"
2. Remplir les informations personnelles
3. Sélectionner la tribu et le département
4. Définir le statut
5. Cliquer sur "Enregistrer"

#### Enregistrer un Culte
1. Cliquer sur "Cultes" → "+ Ajouter Culte"
2. Entrer la date et le type
3. Ajouter le thème et le prédicateur
4. Cliquer sur "Enregistrer"

#### Enregistrer les Présences
1. Cliquer sur "Présences" → "+ Ajouter Présence"
2. Sélectionner le membre et le culte
3. Cocher "Présent" si le membre était présent
4. Cliquer sur "Enregistrer"

## Navigation dans l'Application

### 📊 Tableau de Bord (/)
Vue d'ensemble avec:
- Statistiques clés (total, actifs, nouveaux, sortis)
- Taux de participation moyen
- Répartition par tribu et département
- Cultes récents
- Distribution par statut

### 👥 Liste des Membres (/membres)
Gestion complète des membres avec:
- Filtres: statut, tribu, département
- Informations personnelles et d'église
- Calcul du taux de participation

### 📈 Statistiques (/statistiques)
Analyses détaillées:
- Top 10 participants
- Participation mensuelle
- Évolution des membres

### 🔍 Analyse (/analyse)
Analyse approfondie:
- Répartition par tribu et département
- Tendances hebdomadaires
- Identification des patterns

## Résolution des Problèmes Courants

### Le serveur ne démarre pas

```bash
# Vérifier l'installation
python -m django --version

# Vérifier la configuration
python manage.py check

# Appliquer les migrations manquantes
python manage.py migrate
```

### Base de données corrompue

```bash
# Sauvegarder la base actuelle
copy db.sqlite3 db.sqlite3.corrupt

# Recréer les migrations
python manage.py migrate eglise zero

# Réappliquer les migrations
python manage.py migrate
```

### Oublié le mot de passe admin

```bash
# Créer un nouvel admin
python manage.py createsuperuser

# Ou réinitialiser via le shell
python manage.py shell

# Dans le shell:
# from django.contrib.auth.models import User
# User.objects.filter(username='admin').delete()
# exit()
```

### Performance lente

```bash
# Vérifier les requêtes SQL
# Dans settings.py, ajouter:
# LOGGING = {...}  # Configuration de logging

# Optimiser les requêtes dans les vues
# Utiliser select_related() et prefetch_related()
```

## Configuration Avancée

### Changer le Port du Serveur

```bash
python manage.py runserver 0.0.0.0:8080
```

### Activer le Mode Production

1. Dans `settings.py`:
   - Changer `DEBUG = False`
   - Configurer `ALLOWED_HOSTS`
   - Générer une nouvelle `SECRET_KEY`

2. Déployer sur un serveur WSGI (Gunicorn, uWSGI)

### Intégrer une Base de Données Externe

Modifier `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'eglise_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Sauvegarde et Restauration

### Sauvegarder les Données

```bash
# Exporter les données
python manage.py dumpdata > donnees.json

# Ou sauvegarder simplement la base
copy db.sqlite3 db.backup.sqlite3
```

### Restaurer les Données

```bash
# Restaurer depuis un dump JSON
python manage.py loaddata donnees.json

# Ou restaurer la base
copy db.backup.sqlite3 db.sqlite3
python manage.py migrate
```

## Conseils et Bonnes Pratiques

1. **Sauvegarde régulière** : Créer des backups hebdomadaires
2. **Maintenance** : Exécuter `python manage.py check` régulièrement
3. **Données de test** : Utiliser `load_demo_data.py` pour les tests
4. **Documentation** : Maintenir à jour la documentation
5. **Contrôle d'accès** : Définir les permissions des utilisateurs
6. **Audit** : Suivre les modifications importantes

## Support et Ressources

- **Documentation Django** : https://docs.djangoproject.com
- **Guide Admin Django** : https://docs.djangoproject.com/en/stable/ref/contrib/admin/
- **Tutoriels** : https://www.djangoproject.com/

---

**Besoin d'aide ?** Consultez le README.md pour plus de détails.
