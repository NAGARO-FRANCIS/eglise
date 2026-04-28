"""
Script de validation - Vérifie que tout est correctement installé et configuré
Utilisation: python manage.py shell < test_installation.py
"""

import sys
import django
from django.db import connection
from django.apps import apps

print("=" * 60)
print("🔍 TEST D'INSTALLATION - APPLICATION DE GESTION D'ÉGLISE")
print("=" * 60)

# Test 1: Django
print("\n✓ Django")
print(f"  Version: {django.VERSION}")

# Test 2: Applications installées
print("\n✓ Applications installées")
apps_to_check = ['eglise', 'django.contrib.admin', 'django.contrib.auth']
for app in apps_to_check:
    try:
        apps.get_app_config(app.split('.')[-1])
        print(f"  - {app}: OK")
    except Exception as e:
        print(f"  - {app}: ERREUR - {e}")

# Test 3: Modèles
print("\n✓ Modèles Django")
from eglise.models import Tribu, Departement, Membre, Culte, Presence, Statistique

models = [Tribu, Departement, Membre, Culte, Presence, Statistique]
for model in models:
    count = model.objects.count()
    print(f"  - {model.__name__}: {count} enregistrements")

# Test 4: Base de données
print("\n✓ Base de données")
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM eglise_tribu;")
        print(f"  - Connexion: OK")
        print(f"  - Tables créées: OK")
except Exception as e:
    print(f"  - Erreur: {e}")

# Test 5: Statistiques
print("\n✓ Statistiques")
total_membres = Membre.objects.count()
total_cultes = Culte.objects.count()
total_presences = Presence.objects.count()

print(f"  - Membres: {total_membres}")
print(f"  - Cultes: {total_cultes}")
print(f"  - Présences: {total_presences}")

if total_membres == 0:
    print("\n  ⚠️  Aucun membre - charger les données de demo: python manage.py shell < load_demo_data.py")

# Test 6: Configuration
print("\n✓ Configuration")
from django.conf import settings
print(f"  - DEBUG: {settings.DEBUG}")
print(f"  - BASE DE DONNÉES: SQLite" if "sqlite3" in settings.DATABASES['default']['ENGINE'] else f"  - BASE DE DONNÉES: {settings.DATABASES['default']['ENGINE']}")
print(f"  - LANGUE: {settings.LANGUAGE_CODE}")
print(f"  - FUSEAU HORAIRE: {settings.TIME_ZONE}")

# Test 7: Templates
print("\n✓ Templates")
templates_to_check = [
    'eglise/base.html',
    'eglise/dashboard.html',
    'eglise/membre_list.html',
    'eglise/statistiques.html',
    'eglise/analyse.html'
]

from django.template.loader import get_template
from django.template.exceptions import TemplateDoesNotExist

for template_name in templates_to_check:
    try:
        get_template(template_name)
        print(f"  - {template_name}: OK")
    except TemplateDoesNotExist:
        print(f"  - {template_name}: ABSENT")

# Test 8: URLs
print("\n✓ URLs")
from django.urls import reverse

url_names = ['eglise:dashboard', 'eglise:membre_list', 'eglise:statistiques', 'eglise:analyse']
for url_name in url_names:
    try:
        url = reverse(url_name)
        print(f"  - {url_name}: {url}")
    except Exception as e:
        print(f"  - {url_name}: ERREUR - {e}")

# Résumé
print("\n" + "=" * 60)
print("✅ TEST TERMINÉ")
print("=" * 60)
print("\n🚀 PROCHAIN ÉTAPE:")
if total_membres == 0:
    print("  1. Charger les données de démonstration")
    print("     > python manage.py shell < load_demo_data.py")
    print("  2. Démarrer le serveur")
    print("     > python manage.py runserver")
else:
    print("  1. Démarrer le serveur")
    print("     > python manage.py runserver")

print("\n📱 ACCÈS:")
print("  - Web: http://localhost:8000")
print("  - Admin: http://localhost:8000/admin")
print("\n" + "=" * 60)
