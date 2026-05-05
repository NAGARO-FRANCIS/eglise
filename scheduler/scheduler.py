"""
Système de planification automatique pour la génération des rapports mensuels.
Les rapports sont générés automatiquement:
- Le 1er du mois à 00:15 UTC
- Pour chaque tribu et département
"""
import os
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.utils import timezone
from datetime import datetime

logger = logging.getLogger(__name__)
scheduler = None
SCHEDULER_STARTED = False


def generate_monthly_reports():
    """
    Fonction appelée automatiquement chaque mois pour générer les rapports.
    Elle appelle la commande Django generer_rapports_auto.
    """
    try:
        # Importer Django
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CCR.settings')
        
        if not django.apps.apps.ready:
            django.setup()
        
        # Importer les modèles après Django setup
        from eglise.models import Tribu, Departement, RapportMensuel
        from datetime import datetime
        from dateutil.relativedelta import relativedelta
        
        # Déterminer le mois précédent (puisque la tâche s'exécute le 1er du mois)
        maintenant = datetime.now()
        mois_cible = maintenant - relativedelta(months=1)
        mois = mois_cible.month
        annee = mois_cible.year
        
        logger.info(f"🤖 Génération automatique des rapports mensuels pour {mois}/{annee}")
        logger.info("=" * 80)
        
        # 1. Générer le rapport GLOBAL
        logger.info("1️⃣  Rapport GLOBAL")
        _generer_rapport_global(mois, annee)
        
        # 2. Générer les rapports par TRIBU
        logger.info("2️⃣  Rapports par TRIBU")
        tribus = Tribu.objects.all()
        for tribu in tribus:
            _generer_rapport_tribu(mois, annee, tribu)
        
        # 3. Générer les rapports par DÉPARTEMENT
        logger.info("3️⃣  Rapports par DÉPARTEMENT")
        departements = Departement.objects.all()
        for departement in departements:
            _generer_rapport_departement(mois, annee, departement)
        
        logger.info("=" * 80)
        logger.info("✅ Génération automatique des rapports complétée!")
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la génération automatique des rapports: {str(e)}", exc_info=True)


def _generer_rapport_global(mois, annee):
    """Génère le rapport mensuel global."""
    from eglise.models import RapportMensuel, Membre, Tribu, Departement, Culte, Presence
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    
    rapport_existing = RapportMensuel.objects.filter(
        mois=mois,
        annee=annee,
        tribu__isnull=True,
        departement__isnull=True
    ).first()

    if rapport_existing:
        rapport = rapport_existing
    else:
        rapport = RapportMensuel(mois=mois, annee=annee)

    _remplir_donnees_rapport(rapport, mois, annee)
    rapport.save()
    logger.info(f"   ✅ Rapport global: {rapport.nombre_total_membres} membres")


def _generer_rapport_tribu(mois, annee, tribu):
    """Génère le rapport mensuel pour une tribu."""
    from eglise.models import RapportMensuel
    
    rapport_existing = RapportMensuel.objects.filter(
        mois=mois,
        annee=annee,
        tribu=tribu,
        departement__isnull=True
    ).first()

    if rapport_existing:
        rapport = rapport_existing
    else:
        rapport = RapportMensuel(mois=mois, annee=annee, tribu=tribu)

    _remplir_donnees_rapport(rapport, mois, annee, tribu=tribu)
    rapport.save()
    logger.info(f"   ✅ {tribu.nom}: {rapport.nombre_total_membres} membres")


def _generer_rapport_departement(mois, annee, departement):
    """Génère le rapport mensuel pour un département."""
    from eglise.models import RapportMensuel
    
    rapport_existing = RapportMensuel.objects.filter(
        mois=mois,
        annee=annee,
        tribu__isnull=True,
        departement=departement
    ).first()

    if rapport_existing:
        rapport = rapport_existing
    else:
        rapport = RapportMensuel(mois=mois, annee=annee, departement=departement)

    _remplir_donnees_rapport(rapport, mois, annee, departement=departement)
    rapport.save()
    logger.info(f"   ✅ {departement.nom}: {rapport.nombre_total_membres} membres")


def _remplir_donnees_rapport(rapport, mois, annee, tribu=None, departement=None):
    """Remplit les données du rapport."""
    from eglise.models import Membre, Tribu, Departement, Culte, Presence
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    
    # Déterminer la période
    date_debut = datetime(annee, mois, 1).date()
    if mois == 12:
        date_fin = datetime(annee + 1, 1, 1).date() - relativedelta(days=1)
    else:
        date_fin = datetime(annee, mois + 1, 1).date() - relativedelta(days=1)

    # Filtrer les membres selon la tribu/département
    membres_qs = Membre.objects.all()
    if tribu:
        membres_qs = membres_qs.filter(tribu=tribu)
    if departement:
        membres_qs = membres_qs.filter(departement=departement)

    # Données générales
    rapport.nombre_total_membres = membres_qs.count()
    rapport.nombre_membres_actifs = membres_qs.filter(statut='actif').count()
    rapport.nombre_membres_nouveau = membres_qs.filter(
        statut='nouveau',
        date_adhesion__month=mois,
        date_adhesion__year=annee
    ).count()
    rapport.nombre_membres_inactif = membres_qs.filter(statut='inactif').count()
    rapport.nombre_membres_sorti = membres_qs.filter(statut='sorti').count()

    # Données par tribu (si rapport global ou par département)
    if not tribu:
        rapport.nombre_tribus = Tribu.objects.count()
        membres_par_tribu = {}
        for t in Tribu.objects.all():
            membres_filtre = t.membre_set.all()
            if departement:
                membres_filtre = membres_filtre.filter(departement=departement)
            count = membres_filtre.filter(statut='actif').count()
            if count > 0:
                membres_par_tribu[t.nom] = count
        rapport.membres_par_tribu = membres_par_tribu

    # Données par département (si rapport global ou par tribu)
    if not departement:
        rapport.nombre_departements = Departement.objects.count()
        membres_par_departement = {}
        for d in Departement.objects.all():
            membres_filtre = d.membre_set.all()
            if tribu:
                membres_filtre = membres_filtre.filter(tribu=tribu)
            count = membres_filtre.filter(statut='actif').count()
            if count > 0:
                membres_par_departement[d.nom] = count
        rapport.membres_par_departement = membres_par_departement

    # Statistiques d'assistance
    cultes_du_mois = Culte.objects.filter(
        date__gte=date_debut,
        date__lte=date_fin
    )

    # Filtrer les cultes selon les présences des membres filtrés
    if tribu or departement:
        cultes_du_mois = cultes_du_mois.filter(
            presence__membre__in=membres_qs
        ).distinct()

    rapport.nombre_cultes = cultes_du_mois.count()

    # Presences
    presences_du_mois = Presence.objects.filter(
        culte__date__gte=date_debut,
        culte__date__lte=date_fin,
        membre__in=membres_qs
    )

    rapport.nombre_total_presences = presences_du_mois.filter(present=True).count()
    rapport.nombre_total_absences = presences_du_mois.filter(present=False).count()

    # Taux de participation
    if presences_du_mois.count() > 0:
        rapport.taux_participation_moyen = round(
            (rapport.nombre_total_presences / presences_du_mois.count()) * 100,
            2
        )
    else:
        rapport.taux_participation_moyen = 0.0

    # Données par type de culte
    cultes_par_type = {}
    for culte in cultes_du_mois:
        type_culte = culte.get_type_culte_display()
        presences_culte = presences_du_mois.filter(culte=culte, present=True).count()
        if presences_culte > 0:
            if type_culte not in cultes_par_type:
                cultes_par_type[type_culte] = {'nombre': 0, 'participants': 0}
            cultes_par_type[type_culte]['nombre'] += 1
            cultes_par_type[type_culte]['participants'] += presences_culte

    rapport.cultes_par_type = cultes_par_type


def start_scheduler():
    """Démarre le scheduler APScheduler."""
    global scheduler, SCHEDULER_STARTED
    
    # Éviter de démarrer plusieurs instances du scheduler
    if SCHEDULER_STARTED:
        return
    
    try:
        # Créer le scheduler
        scheduler = BackgroundScheduler()
        
        # Ajouter le job: générer les rapports le 1er du mois à 00:15
        # Cron: minute=15, hour=0, day=1 (premier jour du mois)
        scheduler.add_job(
            generate_monthly_reports,
            trigger=CronTrigger(hour=0, minute=15, day=1),
            id='generer_rapports_mensuels',
            name='Génération automatique des rapports mensuels',
            replace_existing=True,
            misfire_grace_time=900  # 15 minutes de tolérance
        )
        
        # Démarrer le scheduler
        scheduler.start()
        SCHEDULER_STARTED = True
        logger.info("✅ Scheduler APScheduler démarré avec succès!")
        logger.info("   📅 Tâche: Génération des rapports chaque 1er du mois à 00:15 UTC")
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du démarrage du scheduler: {str(e)}", exc_info=True)


def stop_scheduler():
    """Arrête le scheduler APScheduler."""
    global scheduler, SCHEDULER_STARTED
    
    if scheduler is not None and scheduler.running:
        try:
            scheduler.shutdown(wait=False)
            SCHEDULER_STARTED = False
            logger.info("⏹️  Scheduler arrêté")
        except Exception as e:
            logger.error(f"Erreur lors de l'arrêt du scheduler: {str(e)}")
