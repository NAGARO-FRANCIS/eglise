#!/usr/bin/env python
"""
Utilitaire pour générer les rapports mensuels automatiquement.
Génère un rapport global + rapports par tribu + rapports par département.
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


def generer_rapport_mensuel_global(mois, annee, auteur=None):
    """Génère le rapport mensuel global pour l'église"""
    
    rapport_existing = RapportMensuel.objects.filter(
        mois=mois, annee=annee, tribu__isnull=True, departement__isnull=True
    ).first()
    
    if rapport_existing:
        rapport = rapport_existing
    else:
        rapport = RapportMensuel(mois=mois, annee=annee, tribu=None, departement=None)
    
    # Définir la période
    date_debut = datetime(annee, mois, 1).date()
    if mois == 12:
        date_fin = datetime(annee + 1, 1, 1).date() - timedelta(days=1)
    else:
        date_fin = datetime(annee, mois + 1, 1).date() - timedelta(days=1)
    
    # Données générales
    rapport.nombre_total_membres = Membre.objects.count()
    rapport.nombre_membres_actifs = Membre.objects.filter(statut='actif').count()
    rapport.nombre_membres_nouveau = Membre.objects.filter(
        statut='nouveau',
        date_adhesion__month=mois,
        date_adhesion__year=annee
    ).count()
    rapport.nombre_membres_inactif = Membre.objects.filter(statut='inactif').count()
    rapport.nombre_membres_sorti = Membre.objects.filter(statut='sorti').count()
    
    # Données par tribu
    rapport.nombre_tribus = Tribu.objects.count()
    membres_par_tribu = {}
    for tribu in Tribu.objects.all():
        count = tribu.membre_set.filter(statut='actif').count()
        if count > 0:
            membres_par_tribu[tribu.nom] = count
    rapport.membres_par_tribu = membres_par_tribu
    
    # Données par département
    rapport.nombre_departements = Departement.objects.count()
    membres_par_departement = {}
    for departement in Departement.objects.all():
        count = departement.membre_set.filter(statut='actif').count()
        if count > 0:
            membres_par_departement[departement.nom] = count
    rapport.membres_par_departement = membres_par_departement
    
    # Statistiques d'assistance
    cultes_du_mois = Culte.objects.filter(date__gte=date_debut, date__lte=date_fin)
    rapport.nombre_cultes = cultes_du_mois.count()
    
    presences_du_mois = Presence.objects.filter(culte__date__gte=date_debut, culte__date__lte=date_fin)
    rapport.nombre_total_presences = presences_du_mois.filter(present=True).count()
    rapport.nombre_total_absences = presences_du_mois.filter(present=False).count()
    
    if presences_du_mois.count() > 0:
        rapport.taux_participation_moyen = round(
            (rapport.nombre_total_presences / presences_du_mois.count()) * 100, 2
        )
    else:
        rapport.taux_participation_moyen = 0.0
    
    # Cultes par type
    cultes_par_type = {}
    for culte in cultes_du_mois.values('type').distinct():
        type_culte = culte['type']
        cultes_type = cultes_du_mois.filter(type=type_culte)
        presences_type = presences_du_mois.filter(culte__type=type_culte, present=True).count()
        cultes_par_type[type_culte] = {
            'nombre': cultes_type.count(),
            'participants': presences_type
        }
    rapport.cultes_par_type = cultes_par_type
    
    if not auteur:
        auteur = User.objects.filter(is_superuser=True).first()
    rapport.auteur = auteur
    rapport.save()
    
    return rapport


def generer_rapports_par_tribu(mois, annee, auteur=None):
    """Génère un rapport pour CHAQUE tribu"""
    
    rapports_tribu = []
    date_debut = datetime(annee, mois, 1).date()
    if mois == 12:
        date_fin = datetime(annee + 1, 1, 1).date() - timedelta(days=1)
    else:
        date_fin = datetime(annee, mois + 1, 1).date() - timedelta(days=1)
    
    for tribu in Tribu.objects.all():
        # Vérifier si le rapport existe
        rapport_existing = RapportMensuel.objects.filter(
            mois=mois, annee=annee, tribu=tribu
        ).first()
        
        if rapport_existing:
            rapport = rapport_existing
        else:
            rapport = RapportMensuel(mois=mois, annee=annee, tribu=tribu, departement=None)
        
        # Données pour cette tribu
        membres_tribu = tribu.membre_set.all()
        rapport.nombre_total_membres = membres_tribu.count()
        rapport.nombre_membres_actifs = membres_tribu.filter(statut='actif').count()
        rapport.nombre_membres_nouveau = membres_tribu.filter(
            statut='nouveau',
            date_adhesion__month=mois,
            date_adhesion__year=annee
        ).count()
        rapport.nombre_membres_inactif = membres_tribu.filter(statut='inactif').count()
        rapport.nombre_membres_sorti = membres_tribu.filter(statut='sorti').count()
        
        # Cultes de cette tribu (si applicable)
        rapport.nombre_tribus = 1  # La tribu elle-même
        rapport.nombre_departements = 0
        
        # Cultes spécifiques à la tribu (si liés)
        cultes_tribu = Culte.objects.filter(
            date__gte=date_debut,
            date__lte=date_fin
        )
        rapport.nombre_cultes = cultes_tribu.count()
        
        presences_tribu = Presence.objects.filter(
            culte__date__gte=date_debut,
            culte__date__lte=date_fin,
            membre__tribu=tribu
        )
        rapport.nombre_total_presences = presences_tribu.filter(present=True).count()
        rapport.nombre_total_absences = presences_tribu.filter(present=False).count()
        
        if presences_tribu.count() > 0:
            rapport.taux_participation_moyen = round(
                (rapport.nombre_total_presences / presences_tribu.count()) * 100, 2
            )
        else:
            rapport.taux_participation_moyen = 0.0
        
        # Cultes par type
        cultes_par_type = {}
        for culte in cultes_tribu.values('type').distinct():
            type_culte = culte['type']
            cultes_type = cultes_tribu.filter(type=type_culte)
            presences_type = presences_tribu.filter(culte__type=type_culte, present=True).count()
            cultes_par_type[type_culte] = {
                'nombre': cultes_type.count(),
                'participants': presences_type
            }
        rapport.cultes_par_type = cultes_par_type
        
        if not auteur:
            auteur = User.objects.filter(is_superuser=True).first()
        rapport.auteur = auteur
        rapport.save()
        rapports_tribu.append(rapport)
    
    return rapports_tribu


def generer_rapports_par_departement(mois, annee, auteur=None):
    """Génère un rapport pour CHAQUE département"""
    
    rapports_dept = []
    date_debut = datetime(annee, mois, 1).date()
    if mois == 12:
        date_fin = datetime(annee + 1, 1, 1).date() - timedelta(days=1)
    else:
        date_fin = datetime(annee, mois + 1, 1).date() - timedelta(days=1)
    
    for departement in Departement.objects.all():
        # Vérifier si le rapport existe
        rapport_existing = RapportMensuel.objects.filter(
            mois=mois, annee=annee, departement=departement
        ).first()
        
        if rapport_existing:
            rapport = rapport_existing
        else:
            rapport = RapportMensuel(mois=mois, annee=annee, tribu=None, departement=departement)
        
        # Données pour ce département
        membres_dept = departement.membre_set.all()
        rapport.nombre_total_membres = membres_dept.count()
        rapport.nombre_membres_actifs = membres_dept.filter(statut='actif').count()
        rapport.nombre_membres_nouveau = membres_dept.filter(
            statut='nouveau',
            date_adhesion__month=mois,
            date_adhesion__year=annee
        ).count()
        rapport.nombre_membres_inactif = membres_dept.filter(statut='inactif').count()
        rapport.nombre_membres_sorti = membres_dept.filter(statut='sorti').count()
        
        rapport.nombre_departements = 1  # Le département lui-même
        rapport.nombre_tribus = 0
        
        # Cultes du mois
        cultes_mois = Culte.objects.filter(
            date__gte=date_debut,
            date__lte=date_fin
        )
        rapport.nombre_cultes = cultes_mois.count()
        
        # Présences des membres du département
        presences_dept = Presence.objects.filter(
            culte__date__gte=date_debut,
            culte__date__lte=date_fin,
            membre__departement=departement
        )
        rapport.nombre_total_presences = presences_dept.filter(present=True).count()
        rapport.nombre_total_absences = presences_dept.filter(present=False).count()
        
        if presences_dept.count() > 0:
            rapport.taux_participation_moyen = round(
                (rapport.nombre_total_presences / presences_dept.count()) * 100, 2
            )
        else:
            rapport.taux_participation_moyen = 0.0
        
        # Cultes par type
        cultes_par_type = {}
        for culte in cultes_mois.values('type').distinct():
            type_culte = culte['type']
            cultes_type = cultes_mois.filter(type=type_culte)
            presences_type = presences_dept.filter(culte__type=type_culte, present=True).count()
            cultes_par_type[type_culte] = {
                'nombre': cultes_type.count(),
                'participants': presences_type
            }
        rapport.cultes_par_type = cultes_par_type
        
        if not auteur:
            auteur = User.objects.filter(is_superuser=True).first()
        rapport.auteur = auteur
        rapport.save()
        rapports_dept.append(rapport)
    
    return rapports_dept


def generer_tous_rapports_mensuel(mois, annee, auteur=None):
    """
    Génère TOUS les rapports mensuels:
    - 1 rapport global (église entière)
    - 1 rapport par tribu
    - 1 rapport par département
    """
    
    print("\n" + "=" * 80)
    print("Générateur de Rapports Mensuels - Mode Complet")
    print("=" * 80)
    
    # Rapport global
    print(f"\n1️⃣ Génération du rapport GLOBAL...")
    rapport_global = generer_rapport_mensuel_global(mois, annee, auteur)
    print(f"✓ Rapport global créé: {rapport_global.periode_str}")
    
    # Rapports par tribu
    print(f"\n2️⃣ Génération des rapports par TRIBU...")
    rapports_tribu = generer_rapports_par_tribu(mois, annee, auteur)
    print(f"✓ {len(rapports_tribu)} rapports de tribu créés")
    for r in rapports_tribu:
        print(f"   - Tribu: {r.tribu.nom if r.tribu else 'N/A'}")
    
    # Rapports par département
    print(f"\n3️⃣ Génération des rapports par DÉPARTEMENT...")
    rapports_dept = generer_rapports_par_departement(mois, annee, auteur)
    print(f"✓ {len(rapports_dept)} rapports de département créés")
    for r in rapports_dept:
        print(f"   - Département: {r.departement.nom if r.departement else 'N/A'}")
    
    print(f"\n" + "=" * 80)
    print("✅ Génération Complète Terminée!")
    print("=" * 80)
    print(f"Total rapports créés/mis à jour: {1 + len(rapports_tribu) + len(rapports_dept)}")
    print("=" * 80)


if __name__ == '__main__':
    import sys
    
    # Déterminer le mois et l'année
    if len(sys.argv) > 2:
        mois = int(sys.argv[1])
        annee = int(sys.argv[2])
    else:
        # Par défaut: mois courant
        now = datetime.now()
        mois = now.month
        annee = now.year
    
    generer_tous_rapports_mensuel(mois, annee)
