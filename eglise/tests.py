from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from eglise.models import Culte, Membre, Presence, RapportHebdomadaire, Tribu
from scheduler.scheduler import generate_weekly_reports


class WeeklyReportsTests(TestCase):
    def test_generate_weekly_reports_creates_evolution_and_tribu_reports(self):
        tribu = Tribu.objects.create(nom='Tribu Test')
        membre = Membre.objects.create(
            nom='Doe',
            prenom='John',
            tribu=tribu,
            statut='actif',
        )

        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        culte = Culte.objects.create(
            date=start_of_week,
            type_culte='dimanche',
            nombre_participants=3,
            nombre_nouveaux=1,
        )
        Presence.objects.create(membre=membre, culte=culte, present=True)

        result = generate_weekly_reports(date=today)

        self.assertEqual(result['evolution'], 1)
        self.assertEqual(result['tribu'], 1)
        self.assertTrue(
            RapportHebdomadaire.objects.filter(type_rapport='evolution_culte').exists()
        )
        self.assertTrue(
            RapportHebdomadaire.objects.filter(type_rapport='tribu').exists()
        )
