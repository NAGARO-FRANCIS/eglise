#!/usr/bin/env python
"""
Script de test pour vérifier que la validation de l'unicité des responsables fonctionne correctement.
Une tribu et un département ne peuvent avoir qu'un seul utilisateur.
"""
import os
import django

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CCR.settings')
django.setup()

from django.contrib.auth.models import User
from eglise.models import UserProfile, Tribu, Departement
from django.core.exceptions import ValidationError

print("=" * 80)
print("TEST: Validation de l'unicité des responsables")
print("=" * 80)

# Nettoyer les données de test
print("\n1. Nettoyage des données de test...")
User.objects.filter(username__startswith='test_').delete()
Tribu.objects.filter(nom__startswith='TEST').delete()
Departement.objects.filter(nom__startswith='TEST').delete()

# Créer des données de test
print("2. Création des données de test...")
tribu_test = Tribu.objects.create(nom='TEST Tribu Alpha', description='Tribu de test')
departement_test = Departement.objects.create(nom='TEST Département Beta', description='Département de test')

user1 = User.objects.create_user(username='test_patriarche1', password='testpass123', first_name='Jean', last_name='Dupont')
user2 = User.objects.create_user(username='test_patriarche2', password='testpass123', first_name='Marie', last_name='Martin')

print(f"  - Tribu créée: {tribu_test.nom}")
print(f"  - Département créé: {departement_test.nom}")
print(f"  - User 1 créé: {user1.username}")
print(f"  - User 2 créé: {user2.username}")

# Test 1: Créer un premier patriarche pour la tribu
print("\n3. Test 1: Créer le premier patriarche pour la tribu...")
try:
    profile1 = UserProfile.objects.create(
        user=user1,
        role='patriarche',
        tribu=tribu_test
    )
    print(f"  ✓ Patriarche créé avec succès: {user1.username}")
except ValidationError as e:
    print(f"  ✗ Erreur (attendue): {e}")

# Test 2: Essayer de créer un deuxième patriarche pour la même tribu (doit échouer)
print("\n4. Test 2: Essayer de créer un deuxième patriarche pour la même tribu...")
try:
    profile2 = UserProfile.objects.create(
        user=user2,
        role='patriarche',
        tribu=tribu_test
    )
    print(f"  ✗ ERREUR: Le deuxième patriarche a été créé (ne devrait pas arriver ici)!")
except ValidationError as e:
    print(f"  ✓ Validation correctement bloquée: {e}")

# Test 3: Vérifier qu'un responsable peut être créé pour le département
print("\n5. Test 3: Créer un responsable pour le département...")
try:
    user3 = User.objects.create_user(username='test_responsable1', password='testpass123', first_name='Paul', last_name='Leblanc')
    profile3 = UserProfile.objects.create(
        user=user3,
        role='responsable',
        departement=departement_test
    )
    print(f"  ✓ Responsable créé avec succès: {user3.username}")
except ValidationError as e:
    print(f"  ✗ Erreur: {e}")

# Test 4: Essayer de créer un deuxième responsable pour le même département (doit échouer)
print("\n6. Test 4: Essayer de créer un deuxième responsable pour le même département...")
try:
    user4 = User.objects.create_user(username='test_responsable2', password='testpass123', first_name='Anne', last_name='Durand')
    profile4 = UserProfile.objects.create(
        user=user4,
        role='responsable',
        departement=departement_test
    )
    print(f"  ✗ ERREUR: Le deuxième responsable a été créé (ne devrait pas arriver ici)!")
except ValidationError as e:
    print(f"  ✓ Validation correctement bloquée: {e}")

# Test 5: Vérifier qu'on peut modifier un profil existant sans erreur
print("\n7. Test 5: Modifier un profil existant sans changement...")
try:
    profile1.save()
    print(f"  ✓ Profil modifié avec succès: {user1.username}")
except ValidationError as e:
    print(f"  ✗ Erreur: {e}")

# Nettoyage final
print("\n8. Nettoyage final...")
User.objects.filter(username__startswith='test_').delete()
Tribu.objects.filter(nom__startswith='TEST').delete()
Departement.objects.filter(nom__startswith='TEST').delete()
print("  ✓ Données de test supprimées")

print("\n" + "=" * 80)
print("Tests terminés!")
print("=" * 80)
