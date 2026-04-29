"""
Script pour créer un utilisateur administrateur de test
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CCR.settings')
django.setup()

from django.contrib.auth.models import User
from eglise.models import UserProfile

def create_admin_user():
    """Crée un utilisateur administrateur de test"""
    
    # Créer l'utilisateur admin
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'first_name': 'Admin',
            'last_name': 'Test',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"✓ Utilisateur admin créé (password: admin123)")
    else:
        print(f"ℹ Utilisateur admin existe déjà")
    
    # Créer un pasteur de test
    pasteur_user, created = User.objects.get_or_create(
        username='pasteur',
        defaults={
            'email': 'pasteur@example.com',
            'first_name': 'Pasteur',
            'last_name': 'Test',
        }
    )
    
    if created:
        pasteur_user.set_password('pasteur123')
        pasteur_user.save()
        profile, _ = UserProfile.objects.get_or_create(
            user=pasteur_user,
            defaults={'role': 'pasteur'}
        )
        print(f"✓ Utilisateur pasteur créé (password: pasteur123)")
    else:
        print(f"ℹ Utilisateur pasteur existe déjà")
    
    print(f"\nUtilisateurs créés ou existants:")
    print(f"  - Administrateur: admin / admin123")
    print(f"  - Pasteur: pasteur / pasteur123")

if __name__ == '__main__':
    create_admin_user()
