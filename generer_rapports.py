#!/usr/bin/env python
"""
Utilitaire pour générer les rapports mensuels automatiquement.
"""
import os
import django
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Count, Q

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CCR.settings')
django.setup()

from django.contrib.auth.models import User
from eglise.models import RapportMensuel, Membre, Tribu, Departement, Culte, Presence


def generer_rapport_mensuel(mois, annee, auteur=None):
    """
    Génère un rapport mensuel pour le mois et l'année spécifiés.
    
    Args:
        mois (int): Le mois (1-12)
        annee (int): L'année
        auteur (User, optional): L'utilisateur auteur du rapport
    """
    
    # Vérifier si le rapport existe déjà
    rapport_existing = RapportMensuel.objects.filter(mois=mois, annee=annee).first()
    if rapport_existing:
        print(f"Un rapport pour {mois}/{annee} existe déjà. Mise à jour...")
        rapport = rapport_existing
    else:
        print(f"Création d'un nouveau rapport pour {mois}/{annee}...")
        rapport = RapportMensuel(mois=mois, annee=annee)
    
    # Définir la période
    date_debut = datetime(annee, mois, 1).date()
    if mois == 12:
        date_fin = datetime(annee + 1, 1, 1).date() - timedelta(days=1)
    else:
        date_fin = datetime(annee, mois + 1, 1).date() - timedelta(days=1)
    
    # 1. Données générales sur les membres
    rapport.nombre_total_membres = Membre.objects.count()
    rapport.nombre_membres_actifs = Membre.objects.filter(statut='actif').count()
    rapport.nombre_membres_nouveau = Membre.objects.filter(
        statut='nouveau',
        date_adhesion__month=mois,
        date_adhesion__year=annee
    ).count()
    rapport.nombre_membres_inactif = Membre.objects.filter(statut='inactif').count()
    rapport.nombre_membres_sorti = Membre.objects.filter(statut='sorti').count()
    
    # 2. Données par tribu
    rapport.nombre_tribus = Tribu.objects.count()
    membres_par_tribu = {}
    for tribu in Tribu.objects.all():
        count = tribu.membre_set.filter(statut='actif').count()
        if count > 0:
            membres_par_tribu[tribu.nom] = count
    rapport.membres_par_tribu = membres_par_tribu
    
    # 3. Données par département
    rapport.nombre_departements = Departement.objects.count()
    membres_par_departement = {}
    for departement in Departement.objects.all():
        count = departement.membre_set.filter(statut='actif').count()
        if count > 0:
            membres_par_departement[departement.nom] = count
    rapport.membres_par_departement = membres_par_departement
    
    # 4. Statistiques d'assistance
    cultes_du_mois = Culte.objects.filter(
        date__gte=date_debut,
        date__lte=date_fin
    )
    rapport.nombre_cultes = cultes_du_mois.count()
    
    presences_du_mois = Presence.objects.filter(
        culte__date__gte=date_debut,
        culte__date__lte=date_fin
    )
    rapport.nombre_total_presences = presences_du_mois.filter(present=True).count()
    rapport.nombre_total_absences = presences_du_mois.filter(present=False).count()
    
    # Calculer le taux de participation moyen
    if presences_du_mois.count() > 0:
        rapport.taux_participation_moyen = round(
            (rapport.nombre_total_presences / presences_du_mois.count()) * 100,
            2
        )
    else:
        rapport.taux_participation_moyen = 0.0
    
    # 5. Données par type de culte
    cultes_par_type = {}
    for culte in cultes_du_mois:
        type_culte = culte.get_type_culte_display()
        if type_culte not in cultes_par_type:
            cultes_par_type[type_culte] = {'nombre': 0, 'participants': 0}
        cultes_par_type[type_culte]['nombre'] += 1
        cultes_par_type[type_culte]['participants'] += culte.nombre_participants
    rapport.cultes_par_type = cultes_par_type
    
    # 6. Définir l'auteur
    if auteur:
        rapport.auteur = auteur
    
    # 7. Sauvegarder
    rapport.save()
    
    print(f"✓ Rapport généré avec succès:")
    print(f"  - Période: {rapport.periode_str}")
    print(f"  - Membres: {rapport.nombre_total_membres}")
    print(f"  - Taux de participation: {rapport.taux_participation_moyen}%")
    print(f"  - Cultes: {rapport.nombre_cultes}")
    
    return rapport


def generer_rapport_mensuel_courant():
    """Génère le rapport pour le mois courant."""
    maintenant = datetime.now()
    return generer_rapport_mensuel(maintenant.month, maintenant.year)


def generer_rapport_mois_precedent():
    """Génère le rapport pour le mois précédent."""
    maintenant = datetime.now()
    mois_precedent = maintenant - relativedelta(months=1)
    return generer_rapport_mensuel(mois_precedent.month, mois_precedent.year)


if __name__ == '__main__':
    print("=" * 80)
    print("Générateur de Rapports Mensuels")
    print("=" * 80)
    
    # Générer le rapport du mois courant
    print("\n1. Génération du rapport du mois courant...")
    generer_rapport_mensuel_courant()
    
    print("\n" + "=" * 80)
    print("Génération terminée!")
    print("=" * 80)
