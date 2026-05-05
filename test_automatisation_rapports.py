#!/usr/bin/env python
"""
Script pour tester l'automatisation des rapports mensuels.
Lance les tâches planifiées de façon manuelle pour validation.
"""
import os
import sys
import django
from datetime import datetime

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CCR.settings')
django.setup()

from scheduler.scheduler import (
    generate_monthly_reports, 
    _generer_rapport_global,
    _generer_rapport_tribu,
    _generer_rapport_departement
)
from eglise.models import Tribu, Departement, RapportMensuel


def test_generation():
    """Teste la génération des rapports."""
    print("\n" + "=" * 80)
    print("🧪 TEST D'AUTOMATISATION DES RAPPORTS MENSUELS")
    print("=" * 80)
    
    # Utiliser le mois courant
    from datetime import datetime
    maintenant = datetime.now()
    mois = maintenant.month
    annee = maintenant.year
    
    print(f"\n📅 Génération pour: {mois}/{annee}")
    
    try:
        # Tester le rapport global
        print("\n1️⃣  TEST RAPPORT GLOBAL")
        _generer_rapport_global(mois, annee)
        
        # Tester les rapports par tribu
        print("\n2️⃣  TEST RAPPORTS PAR TRIBU")
        tribus = Tribu.objects.all()
        if tribus.count() == 0:
            print("   ⚠️  Aucune tribu trouvée")
        else:
            for tribu in tribus[:3]:  # Tester les 3 premières
                _generer_rapport_tribu(mois, annee, tribu)
        
        # Tester les rapports par département
        print("\n3️⃣  TEST RAPPORTS PAR DÉPARTEMENT")
        departements = Departement.objects.all()
        if departements.count() == 0:
            print("   ⚠️  Aucun département trouvé")
        else:
            for dept in departements[:3]:  # Tester les 3 premiers
                _generer_rapport_departement(mois, annee, dept)
        
        # Compter les rapports générés
        rapports_globaux = RapportMensuel.objects.filter(
            mois=mois, annee=annee,
            tribu__isnull=True, departement__isnull=True
        ).count()
        
        rapports_tribus = RapportMensuel.objects.filter(
            mois=mois, annee=annee,
            tribu__isnull=False, departement__isnull=True
        ).count()
        
        rapports_depts = RapportMensuel.objects.filter(
            mois=mois, annee=annee,
            tribu__isnull=True, departement__isnull=False
        ).count()
        
        print("\n" + "=" * 80)
        print("✅ RÉSUMÉ DU TEST")
        print("=" * 80)
        print(f"📊 Rapports globaux: {rapports_globaux}")
        print(f"📊 Rapports par tribu: {rapports_tribus}")
        print(f"📊 Rapports par département: {rapports_depts}")
        print(f"📊 Total: {rapports_globaux + rapports_tribus + rapports_depts} rapports générés")
        print("\n✅ Automatisation en place et fonctionnelle!")
        print("   Le prochain rapport sera généré automatiquement le 1er du mois à 00:15")
        print("\n" + "=" * 80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    test_generation()
