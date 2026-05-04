"""
Management command pour générer automatiquement les rapports mensuels
pour chaque tribu et département.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Count, Q

from eglise.models import (
    RapportMensuel, Membre, Tribu, Departement, Culte, 
    Presence, UserProfile
)


class Command(BaseCommand):
    help = 'Génère automatiquement les rapports mensuels pour chaque tribu et département'

    def add_arguments(self, parser):
        parser.add_argument(
            '--mois',
            type=int,
            help='Le mois à générer (1-12). Par défaut: mois courant',
            dest='mois',
        )
        parser.add_argument(
            '--annee',
            type=int,
            help='L\'année à générer. Par défaut: année courante',
            dest='annee',
        )
        parser.add_argument(
            '--prev',
            action='store_true',
            help='Générer le rapport du mois précédent',
            dest='mois_precedent',
        )
        parser.add_argument(
            '--tribu',
            type=int,
            help='ID d\'une tribu spécifique (optionnel)',
            dest='tribu_id',
        )
        parser.add_argument(
            '--departement',
            type=int,
            help='ID d\'un département spécifique (optionnel)',
            dest='departement_id',
        )

    def handle(self, *args, **options):
        # Déterminer la période
        if options['mois_precedent']:
            maintenant = datetime.now()
            mois_cible = maintenant - relativedelta(months=1)
            mois = mois_cible.month
            annee = mois_cible.year
        else:
            mois = options['mois'] or datetime.now().month
            annee = options['annee'] or datetime.now().year

        self.stdout.write(
            self.style.SUCCESS(
                f"\n📊 Génération des rapports mensuels pour {mois}/{annee}"
            )
        )
        self.stdout.write("=" * 80)

        # 1. Générer le rapport GLOBAL
        self.stdout.write(self.style.SUCCESS("\n1. Rapport GLOBAL"))
        self.generer_rapport_global(mois, annee)

        # 2. Générer les rapports par TRIBU
        if not options['departement_id']:
            self.stdout.write(self.style.SUCCESS("\n2. Rapports par TRIBU"))
            if options['tribu_id']:
                tribu = Tribu.objects.filter(id=options['tribu_id']).first()
                if tribu:
                    self.generer_rapport_tribu(mois, annee, tribu)
                else:
                    self.stdout.write(self.style.ERROR(f"   ✗ Tribu avec ID {options['tribu_id']} non trouvée"))
            else:
                for tribu in Tribu.objects.all():
                    self.generer_rapport_tribu(mois, annee, tribu)

        # 3. Générer les rapports par DÉPARTEMENT
        if not options['tribu_id']:
            self.stdout.write(self.style.SUCCESS("\n3. Rapports par DÉPARTEMENT"))
            if options['departement_id']:
                departement = Departement.objects.filter(id=options['departement_id']).first()
                if departement:
                    self.generer_rapport_departement(mois, annee, departement)
                else:
                    self.stdout.write(self.style.ERROR(f"   ✗ Département avec ID {options['departement_id']} non trouvé"))
            else:
                for departement in Departement.objects.all():
                    self.generer_rapport_departement(mois, annee, departement)

        self.stdout.write("\n" + "=" * 80)
        self.stdout.write(self.style.SUCCESS("✓ Génération des rapports terminée!\n"))

    def generer_rapport_global(self, mois, annee):
        """Génère le rapport mensuel global."""
        rapport_existing = RapportMensuel.objects.filter(
            mois=mois,
            annee=annee,
            tribu__isnull=True,
            departement__isnull=True
        ).first()

        if rapport_existing:
            self.stdout.write("   Mise à jour du rapport existant...")
            rapport = rapport_existing
        else:
            self.stdout.write("   Création d'un nouveau rapport...")
            rapport = RapportMensuel(mois=mois, annee=annee)

        # Remplir les données
        self._remplir_donnees_rapport(rapport, mois, annee)
        rapport.save()
        self.stdout.write(f"   ✓ Rapport global généré: {rapport.nombre_total_membres} membres")

    def generer_rapport_tribu(self, mois, annee, tribu):
        """Génère le rapport mensuel pour une tribu."""
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

        # Remplir les données spécifiques à la tribu
        self._remplir_donnees_rapport(rapport, mois, annee, tribu=tribu)
        rapport.save()
        self.stdout.write(f"   ✓ {tribu.nom}: {rapport.nombre_total_membres} membres")

    def generer_rapport_departement(self, mois, annee, departement):
        """Génère le rapport mensuel pour un département."""
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

        # Remplir les données spécifiques au département
        self._remplir_donnees_rapport(rapport, mois, annee, departement=departement)
        rapport.save()
        self.stdout.write(f"   ✓ {departement.nom}: {rapport.nombre_total_membres} membres")

    def _remplir_donnees_rapport(self, rapport, mois, annee, tribu=None, departement=None):
        """Remplit les données du rapport."""
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
