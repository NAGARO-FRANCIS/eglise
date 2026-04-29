"""
Script pour charger les données de test de base
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CCR.settings')
django.setup()

from django.utils import timezone
from eglise.models import Tribu, Departement, Culte, Membre
from datetime import datetime, timedelta

def create_test_data():
    """Crée des données de test de base"""
    
    # Créer les tribus
    tribus = []
    tribu_names = ['Judah', 'Benjamin', 'Levi', 'Simeon', 'Reuben', 'Gad']
    
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
    
    # Créer les départements
    departements = []
    dept_names = ['Louange et Adoration', 'Enseignement', 'Assistance Sociale', 'Jeunesse', 'Évangélisation']
    
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
    
    # Créer des cultes récents
    culte_types = ['dimanche', 'mercredi', 'special']
    themes = ['La Résurrection', 'La Foi', 'L\'Amour', 'La Grâce', 'Le Salut']
    preachers = ['Pasteur Jean', 'Pasteur Marie', 'Pasteur Pierre', 'Pasteur Paul']
    
    for i in range(10):
        date = timezone.now().date() - timedelta(days=7*i)
        culte_type = culte_types[i % len(culte_types)]
        theme = themes[i % len(themes)]
        preacher = preachers[i % len(preachers)]
        
        culte, created = Culte.objects.get_or_create(
            date=date,
            type_culte=culte_type,
            defaults={
                'theme': theme,
                'predicateur': preacher,
                'nombre_participants': 0
            }
        )
        if created:
            print(f"✓ Culte du {date} créé")
        else:
            print(f"ℹ Culte du {date} existe déjà")
    
    # Créer des membres de test
    prenom_list = ['Jean', 'Marie', 'Pierre', 'Sophie', 'Michel', 'Anne', 'Paul', 'Isabelle', 'Laurent', 'Nicole']
    nom_list = ['Dupont', 'Martin', 'Bernard', 'Thomas', 'Robert', 'Richard', 'Durand', 'Lefevre', 'Moreau', 'Simon']
    statuts = ['actif', 'actif', 'actif', 'nouveau', 'inactif']
    genres = ['M', 'F']
    
    count = 0
    for i, (prenom, nom) in enumerate(zip(prenom_list * 2, nom_list * 2)):
        tribu = tribus[i % len(tribus)]
        dept = departements[i % len(departements)]
        statut = statuts[i % len(statuts)]
        genre = genres[i % 2]
        
        membre, created = Membre.objects.get_or_create(
            nom=nom,
            prenom=prenom,
            defaults={
                'email': f'{prenom.lower()}.{nom.lower()}@example.com',
                'telephone': f'06{i:08d}',
                'tribu': tribu,
                'departement': dept,
                'statut': statut,
                'genre': genre,
                'date_naissance': timezone.now().date() - timedelta(days=365*30 + i*30),
                'adresse': f'{i+1} rue de l\'Église'
            }
        )
        
        if created:
            print(f"✓ Membre '{prenom} {nom}' créé")
            count += 1
    
    print(f"\n✓ Total: {count} nouveaux membres créés")
    print(f"\nRésumé des données créées:")
    print(f"  - {Tribu.objects.count()} tribus")
    print(f"  - {Departement.objects.count()} départements")
    print(f"  - {Culte.objects.count()} cultes")
    print(f"  - {Membre.objects.count()} membres")

if __name__ == '__main__':
    create_test_data()
