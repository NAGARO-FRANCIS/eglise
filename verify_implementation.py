#!/usr/bin/env python
"""
Test script to verify the Culte management system is properly set up
"""

import os
import sys

# Add the project to the path
sys.path.insert(0, '/c/projet/CCR')

# Check if all necessary files exist
files_to_check = [
    'eglise/forms.py',  # Should have CulteForm
    'eglise/culte_views.py',  # NEW file with views
    'eglise/urls.py',  # Should have new URLs
    'eglise/templates/eglise/culte_list.html',
    'eglise/templates/eglise/culte_form.html',
    'eglise/templates/eglise/culte_statistics.html',
]

print("=" * 60)
print("✅ VÉRIFICATION DES FICHIERS D'IMPLÉMENTATION")
print("=" * 60)

all_good = True
for file_path in files_to_check:
    full_path = os.path.join('/c/projet/CCR', file_path)
    if os.path.exists(full_path):
        print(f"✅ {file_path}")
    else:
        print(f"❌ {file_path} - MANQUANT!")
        all_good = False

print("\n" + "=" * 60)
print("✅ VÉRIFICATION DES IMPORTS")
print("=" * 60)

try:
    from eglise.forms import CulteForm
    print("✅ CulteForm importable depuis eglise.forms")
except ImportError as e:
    print(f"❌ Erreur import CulteForm: {e}")
    all_good = False

try:
    from eglise import culte_views
    print("✅ Module culte_views disponible")
except ImportError as e:
    print(f"❌ Erreur import culte_views: {e}")
    all_good = False

print("\n" + "=" * 60)
if all_good:
    print("✅ TOUS LES FICHIERS SONT EN PLACE!")
    print("=" * 60)
    print("\n🚀 PROCHAINES ÉTAPES:")
    print("1. Exécuter: python manage.py check")
    print("2. Exécuter: python manage.py runserver")
    print("3. Accéder à: http://localhost:8000/cultes/")
    print("\nAssurez-vous d'être connecté comme responsable STATISTIQUE")
else:
    print("❌ CERTAINS FICHIERS MANQUENT!")
    print("=" * 60)

sys.exit(0 if all_good else 1)
