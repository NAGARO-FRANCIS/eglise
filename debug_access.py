"""
Script de débogage pour vérifier l'accès à la page culte_statistics
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CCR.settings')
django.setup()

from django.contrib.auth.models import User
from eglise.models import UserProfile

print("=" * 60)
print("VÉRIFICATION DES ACCÈS À LA PAGE CULTE_STATISTICS")
print("=" * 60)

# Lister tous les utilisateurs
users = User.objects.all()
print(f"\n📊 Nombre total d'utilisateurs: {len(users)}\n")

for user in users:
    print(f"Utilisateur: {user.username}")
    print(f"  Email: {user.email}")
    print(f"  Superuser: {user.is_superuser}")
    
    try:
        profile = user.profile
        print(f"  Rôle: {profile.get_role_display()}")
        
        if profile.role == 'responsable':
            dept = profile.departement
            if dept:
                print(f"  Département: {dept.nom}")
                can_access = dept.nom == 'STATISTIQUE'
                print(f"  ✅ Accès culte_statistics: OUI" if can_access else f"  ❌ Accès culte_statistics: NON ({dept.nom} ≠ STATISTIQUE)")
            else:
                print(f"  ❌ Pas de département assigné")
        elif profile.role == 'pasteur':
            print(f"  ✅ Accès culte_statistics: OUI (Pasteur)")
        else:
            print(f"  ❌ Accès culte_statistics: NON (Patriarche)")
    except UserProfile.DoesNotExist:
        print(f"  ❌ Pas de profil créé")
        if user.is_superuser:
            print(f"  ✅ Accès culte_statistics: OUI (Superuser)")
    
    print()

print("=" * 60)
print("\n💡 POUR CRÉER UN UTILISATEUR AVEC ACCÈS:\n")

# Vérifier si le département STATISTIQUE existe
from eglise.models import Departement

try:
    dept_stat = Departement.objects.get(nom='STATISTIQUE')
    print(f"✅ Département STATISTIQUE existe")
except Departement.DoesNotExist:
    print(f"❌ Département STATISTIQUE n'existe pas - création en cours...")
    dept_stat = Departement.objects.create(
        nom='STATISTIQUE',
        description='Département chargé de la gestion des statistiques'
    )
    print(f"✅ Créé!")

print("\nCommandes pour Django Shell:")
print("------")
print("python manage.py shell")
print("from eglise.models import Departement, UserProfile")
print("from django.contrib.auth.models import User")
print()
print("# Créer un utilisateur test")
print("user = User.objects.create_user('statistique_test', 'stat@test.com', 'password123')")
print()
print("# Ajouter le profil de responsable")
print("dept = Departement.objects.get(nom='STATISTIQUE')")
print("UserProfile.objects.create(user=user, role='responsable', departement=dept)")
print()
print("# Vérifier")
print("user.profile.departement  # Doit afficher: STATISTIQUE")
print("------")
