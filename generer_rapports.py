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


def generer_rapports_tous_structures(mois=None, annee=None):
    """
    Génère les rapports mensuels pour TOUTES les structures:
    - Rapport global
    - Rapports par tribu
    - Rapports par département
    
    Args:
        mois (int, optional): Le mois (1-12). Par défaut: mois courant
        annee (int, optional): L'année. Par défaut: année courante
    """
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    
    if mois is None:
        mois = datetime.now().month
    if annee is None:
        annee = datetime.now().year
    
    print("=" * 80)
    print(f"Génération complète des rapports mensuels pour {mois}/{annee}")
    print("=" * 80)
    
    # 1. Rapport global
    print("\n1. Rapport GLOBAL")
    generer_rapport_mensuel(mois, annee)
    
    # 2. Rapports par tribu
    print("\n2. Rapports par TRIBU")
    for tribu in Tribu.objects.all():
        rapport = RapportMensuel.objects.filter(
            mois=mois, annee=annee, tribu=tribu, departement__isnull=True
        ).first()
        
        if not rapport:
            rapport = RapportMensuel(mois=mois, annee=annee, tribu=tribu)
        
        # Remplir les données pour la tribu
        date_debut = datetime(annee, mois, 1).date()
        if mois == 12:
            date_fin = datetime(annee + 1, 1, 1).date() - relativedelta(days=1)
        else:
            date_fin = datetime(annee, mois + 1, 1).date() - relativedelta(days=1)
        
        # Membres de la tribu
        membres_tribu = Membre.objects.filter(tribu=tribu)
        rapport.nombre_total_membres = membres_tribu.count()
        rapport.nombre_membres_actifs = membres_tribu.filter(statut='actif').count()
        rapport.nombre_membres_nouveau = membres_tribu.filter(
            statut='nouveau',
            date_adhesion__month=mois,
            date_adhesion__year=annee
        ).count()
        rapport.nombre_membres_inactif = membres_tribu.filter(statut='inactif').count()
        rapport.nombre_membres_sorti = membres_tribu.filter(statut='sorti').count()
        
        # Départements dans cette tribu
        rapport.nombre_departements = Departement.objects.filter(
            membre__tribu=tribu
        ).distinct().count()
        
        membres_par_departement = {}
        for dept in Departement.objects.filter(membre__tribu=tribu).distinct():
            count = membres_tribu.filter(departement=dept, statut='actif').count()
            if count > 0:
                membres_par_departement[dept.nom] = count
        rapport.membres_par_departement = membres_par_departement
        
        # Cultes et présences
        presences_tribu = Presence.objects.filter(
            membre__in=membres_tribu,
            culte__date__gte=date_debut,
            culte__date__lte=date_fin
        )
        
        cultes_tribu = Culte.objects.filter(
            presence__membre__in=membres_tribu,
            date__gte=date_debut,
            date__lte=date_fin
        ).distinct()
        
        rapport.nombre_cultes = cultes_tribu.count()
        rapport.nombre_total_presences = presences_tribu.filter(present=True).count()
        rapport.nombre_total_absences = presences_tribu.filter(present=False).count()
        
        if presences_tribu.count() > 0:
            rapport.taux_participation_moyen = round(
                (rapport.nombre_total_presences / presences_tribu.count()) * 100, 2
            )
        
        cultes_par_type = {}
        for culte in cultes_tribu:
            type_culte = culte.get_type_culte_display()
            presences_culte = presences_tribu.filter(culte=culte, present=True).count()
            if presences_culte > 0:
                if type_culte not in cultes_par_type:
                    cultes_par_type[type_culte] = {'nombre': 0, 'participants': 0}
                cultes_par_type[type_culte]['nombre'] += 1
                cultes_par_type[type_culte]['participants'] += presences_culte
        
        rapport.cultes_par_type = cultes_par_type
        rapport.save()
        
        print(f"   ✓ Tribu '{tribu.nom}': {rapport.nombre_total_membres} membres")
    
    # 3. Rapports par département
    print("\n3. Rapports par DÉPARTEMENT")
    for dept in Departement.objects.all():
        rapport = RapportMensuel.objects.filter(
            mois=mois, annee=annee, tribu__isnull=True, departement=dept
        ).first()
        
        if not rapport:
            rapport = RapportMensuel(mois=mois, annee=annee, departement=dept)
        
        # Remplir les données pour le département
        date_debut = datetime(annee, mois, 1).date()
        if mois == 12:
            date_fin = datetime(annee + 1, 1, 1).date() - relativedelta(days=1)
        else:
            date_fin = datetime(annee, mois + 1, 1).date() - relativedelta(days=1)
        
        # Membres du département
        membres_dept = Membre.objects.filter(departement=dept)
        rapport.nombre_total_membres = membres_dept.count()
        rapport.nombre_membres_actifs = membres_dept.filter(statut='actif').count()
        rapport.nombre_membres_nouveau = membres_dept.filter(
            statut='nouveau',
            date_adhesion__month=mois,
            date_adhesion__year=annee
        ).count()
        rapport.nombre_membres_inactif = membres_dept.filter(statut='inactif').count()
        rapport.nombre_membres_sorti = membres_dept.filter(statut='sorti').count()
        
        # Tribus dans ce département
        rapport.nombre_tribus = Tribu.objects.filter(
            membre__departement=dept
        ).distinct().count()
        
        membres_par_tribu = {}
        for tribu in Tribu.objects.filter(membre__departement=dept).distinct():
            count = membres_dept.filter(tribu=tribu, statut='actif').count()
            if count > 0:
                membres_par_tribu[tribu.nom] = count
        rapport.membres_par_tribu = membres_par_tribu
        
        # Cultes et présences
        presences_dept = Presence.objects.filter(
            membre__in=membres_dept,
            culte__date__gte=date_debut,
            culte__date__lte=date_fin
        )
        
        cultes_dept = Culte.objects.filter(
            presence__membre__in=membres_dept,
            date__gte=date_debut,
            date__lte=date_fin
        ).distinct()
        
        rapport.nombre_cultes = cultes_dept.count()
        rapport.nombre_total_presences = presences_dept.filter(present=True).count()
        rapport.nombre_total_absences = presences_dept.filter(present=False).count()
        
        if presences_dept.count() > 0:
            rapport.taux_participation_moyen = round(
                (rapport.nombre_total_presences / presences_dept.count()) * 100, 2
            )
        
        cultes_par_type = {}
        for culte in cultes_dept:
            type_culte = culte.get_type_culte_display()
            presences_culte = presences_dept.filter(culte=culte, present=True).count()
            if presences_culte > 0:
                if type_culte not in cultes_par_type:
                    cultes_par_type[type_culte] = {'nombre': 0, 'participants': 0}
                cultes_par_type[type_culte]['nombre'] += 1
                cultes_par_type[type_culte]['participants'] += presences_culte
        
        rapport.cultes_par_type = cultes_par_type
        rapport.save()
        
        print(f"   ✓ Département '{dept.nom}': {rapport.nombre_total_membres} membres")
    
    print("\n" + "=" * 80)
    print("✓ Génération complète des rapports terminée!")
    print("=" * 80)


if __name__ == '__main__':
    print("=" * 80)
    print("Générateur de Rapports Mensuels")
    print("=" * 80)
    
    # Générer le rapport du mois courant
    print("\n1. Génération du rapport du mois courant...")
    generer_rapport_mensuel_courant()
    
    # Générer tous les rapports (global + tribu + département) pour le mois courant
    print("\n" + "=" * 80)
    print("2. Génération COMPLÈTE (global + tribus + départements)...")
    generer_rapports_tous_structures()
    
    print("\n" + "=" * 80)
    print("Génération terminée!")
    print("=" * 80)
