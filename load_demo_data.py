"""
Script pour charger des données de démonstration dans l'application d'église.
Utilisation: python manage.py shell < load_demo_data.py
"""

from eglise.models import Tribu, Departement, Membre, Culte, Presence
from django.utils import timezone
from datetime import timedelta
import random

# Vider les données existantes (optionnel)
# Tribu.objects.all().delete()
# Departement.objects.all().delete()
# Membre.objects.all().delete()
# Culte.objects.all().delete()
# Presence.objects.all().delete()

# Créer les Tribus
print("📍 Création des Tribus...")
tribus_data = [
    ("Juda", "Tribu de Juda"),
    ("Benjamin", "Tribu de Benjamin"),
    ("Lévi", "Tribu de Lévi"),
]

tribus = {}
for nom, desc in tribus_data:
    tribu, created = Tribu.objects.get_or_create(
        nom=nom,
        defaults={'description': desc}
    )
    tribus[nom] = tribu
    print(f"  ✓ {nom}")

# Créer les Départements
print("\n🏢 Création des Départements...")
depts_data = [
    ("Adoration & Louange", "Ministère musical"),
    ("Enfants", "Accueil et enseignement des enfants"),
    ("Accueil", "Réception et accueil des visiteurs"),
    ("Aide Sociale", "Support aux personnes dans le besoin"),
    ("Intercession", "Groupe de prière"),
    ("Audio-Visuel", "Son et technologie"),
]

departements = {}
for nom, desc in depts_data:
    dept, created = Departement.objects.get_or_create(
        nom=nom,
        defaults={
            'description': desc,
            'responsable': f"Responsable {nom}"
        }
    )
    departements[nom] = dept
    print(f"  ✓ {nom}")

# Créer les Membres
print("\n👥 Création des Membres...")
prenoms = ["Marie", "Jean", "Pierre", "Paul", "Sophie", "Anne", "Marc", "Luc", "Thomas", "Philippe",
           "André", "Jacques", "Matthieu", "Simone", "Jeanne", "Madeleine", "Rachel", "Ruth", "David", "Samuel"]
noms = ["Dupont", "Martin", "Bernard", "Thomas", "Robert", "Richard", "Petit", "Durand", "Lefevre", "Moreau",
        "Simon", "Laurent", "Lefebvre", "Michel", "Garcia", "Martinez", "Lopez", "Sanchez", "Ramos", "Costa"]

membres_list = []
for i in range(30):
    prenom = random.choice(prenoms)
    nom = random.choice(noms)
    tribu = random.choice(list(tribus.values()))
    dept = random.choice(list(departements.values()))
    statut = random.choice(['nouveau', 'actif', 'actif', 'actif', 'inactif', 'sorti'])
    
    date_adhesion = timezone.now().date() - timedelta(days=random.randint(10, 500))
    
    membre, created = Membre.objects.get_or_create(
        nom=nom,
        prenom=prenom,
        defaults={
            'email': f"{prenom.lower()}.{nom.lower()}@email.com",
            'telephone': f"+33 {random.randint(600000000, 799999999)}",
            'adresse': f"{random.randint(1, 100)} Rue de l'Église, {random.randint(10000, 99999)}",
            'tribu': tribu,
            'departement': dept,
            'statut': statut,
            'date_adhesion': date_adhesion,
            'genre': random.choice(['M', 'F']),
            'date_naissance': None,
        }
    )
    if created:
        membres_list.append(membre)
        print(f"  ✓ {membre.nom_complet()} ({tribu.nom})")

print(f"\n  Total: {len(membres_list)} membres créés")

# Créer les Cultes
print("\n📅 Création des Cultes...")
cultes = []
today = timezone.now().date()

for i in range(15):
    date_culte = today - timedelta(days=random.randint(1, 90))
    type_culte = random.choice(['dimanche', 'mercredi', 'dimanche', 'dimanche'])
    
    culte, created = Culte.objects.get_or_create(
        date=date_culte,
        type_culte=type_culte,
        defaults={
            'theme': f"Message #{i+1}",
            'predicateur': random.choice(["Pasteur Martin", "Pasteur Sophie", "Pasteur Pierre"]),
        }
    )
    if created:
        cultes.append(culte)
        print(f"  ✓ Culte du {date_culte} ({type_culte})")

print(f"\n  Total: {len(cultes)} cultes créés")

# Créer les Présences
print("\n📋 Enregistrement des Présences...")
presence_count = 0

for culte in cultes:
    # 60-80% des membres actifs présents
    membres_presents = random.sample(
        [m for m in Membre.objects.filter(statut='actif')],
        k=int(Membre.objects.filter(statut='actif').count() * random.uniform(0.6, 0.8))
    )
    
    for membre in membres_presents:
        presence, created = Presence.objects.get_or_create(
            membre=membre,
            culte=culte,
            defaults={'present': True}
        )
        if created:
            presence_count += 1

# Mettre à jour les nombres de participants
for culte in cultes:
    culte.mettre_a_jour_nombre_participants()

print(f"  ✓ {presence_count} présences enregistrées")

print("\n✅ Données de démonstration chargées avec succès!")
print(f"\n📊 Statistiques:")
print(f"  - Tribus: {Tribu.objects.count()}")
print(f"  - Départements: {Departement.objects.count()}")
print(f"  - Membres: {Membre.objects.count()}")
print(f"  - Membres actifs: {Membre.objects.filter(statut='actif').count()}")
print(f"  - Cultes: {Culte.objects.count()}")
print(f"  - Présences: {Presence.objects.count()}")

print("\n🚀 L'application est prête à être utilisée!")
