"""
Script simple pour créer les données de test minimales
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CCR.settings')
django.setup()

from eglise.models import Tribu, Departement, Culte
from datetime import datetime, timedelta
from django.utils import timezone

print("🔄 Création des données de base...\n")

# Créer les tribus
tribus = []
tribu_names = ['Judah', 'Benjamin', 'Levi', 'Simeon']

for name in tribu_names:
    tribu, created = Tribu.objects.get_or_create(
        nom=name,
        defaults={'description': f'Tribu de {name}'}
    )
    if created:
        print(f"✓ Tribu '{name}' créée")
    else:
        print(f"ℹ Tribu '{name}' existe déjà")
    tribus.append(tribu)

print()

# Créer les départements
departements = []
dept_names = ['Louange', 'Enseignement', 'Assistance', 'Jeunesse']

for name in dept_names:
    dept, created = Departement.objects.get_or_create(
        nom=name,
        defaults={'description': f'Département de {name}'}
    )
    if created:
        print(f"✓ Département '{name}' créé")
    else:
        print(f"ℹ Département '{name}' existe déjà")
    departements.append(dept)

print()

# Créer 5 cultes
for i in range(5):
    date = timezone.now().date() - timedelta(days=7*i)
    culte_type = ['dimanche', 'mercredi', 'special'][i % 3]
    culte, created = Culte.objects.get_or_create(
        date=date,
        type_culte=culte_type,
        defaults={
            'theme': f'Culte {i+1}',
            'predicateur': 'Pasteur Test',
            'nombre_participants': 0
        }
    )
    if created:
        print(f"✓ Culte du {date} ({culte_type}) créé")
    else:
        print(f"ℹ Culte du {date} existe déjà")

print("\n✓ Base de données prête !\n")
print(f"Résumé:")
print(f"  - {Tribu.objects.count()} tribus")
print(f"  - {Departement.objects.count()} départements")
print(f"  - {Culte.objects.count()} cultes")
print(f"\nAccédez aux pages:")
print(f"  - Tribu 1: http://localhost:8000/tribu/1/membres/")
print(f"  - Département 1: http://localhost:8000/departement/1/membres/")
print(f"  - Culte 1: http://localhost:8000/culte/1/presence/")
