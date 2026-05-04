# ✅ Rapport: Automatisation des Rapports Mensuels par Tribu/Département

## 📋 Résumé

J'ai implémenté un système **complet et automatisé** pour générer chaque 1er du mois:

✅ **1 Rapport GLOBAL** (tous les membres)
✅ **1 Rapport par TRIBU** (ex: JUDA, SIMEON, etc.)
✅ **1 Rapport par DÉPARTEMENT** (ex: COM, STATISTIQUE, etc.)

---

## 🎯 Ce qui a été créé

### 1️⃣ Management Command Django
**Fichier:** `eglise/management/commands/generer_rapports_auto.py`

- ✅ Génère automatiquement les rapports pour toutes les structures
- ✅ Support pour générer un mois/année spécifique
- ✅ Support pour générer le mois précédent (`--prev`)
- ✅ Support pour générer une tribu ou département spécifique

### 2️⃣ Script Python Amélioré
**Fichier:** `generer_rapports.py` (mis à jour)

- ✅ Nouvelle fonction `generer_rapports_tous_structures()`
- ✅ Génère le rapport global + tous les rapports par tribu/département
- ✅ Peut être exécuté directement: `python generer_rapports.py`

### 3️⃣ Documentation Complète
**Fichier:** `GUIDE_AUTOMATISATION_RAPPORTS.md`

- ✅ Instructions détaillées pour Windows (Task Scheduler)
- ✅ Instructions pour Linux/Mac (Cron)
- ✅ Configuration Docker et Celery Beat
- ✅ Troubleshooting et debugging

---

## 🚀 Utilisation Immédiate

### Générer manuellement (test):
```bash
python manage.py generer_rapports_auto
```

### Générer pour un mois spécifique:
```bash
python manage.py generer_rapports_auto --mois 5 --annee 2026
```

### Générer pour le mois précédent:
```bash
python manage.py generer_rapports_auto --prev
```

### Générer uniquement pour une tribu:
```bash
python manage.py generer_rapports_auto --tribu 1
```

### Générer uniquement pour un département:
```bash
python manage.py generer_rapports_auto --departement 2
```

---

## ⏰ Configuration Automatique (le 1er du mois)

### 🪟 Windows:
1. Ouvrez **Planificateur de tâches** (`taskschd.msc`)
2. Créez une tâche qui exécute:
   ```
   C:\projet\CCR\manage.py generer_rapports_auto
   ```
3. Planifiez pour le 1er de chaque mois à 2h du matin

👉 **Voir le guide complet:** `GUIDE_AUTOMATISATION_RAPPORTS.md`

### 🐧 Linux/Mac:
```bash
crontab -e
# Ajouter:
0 2 1 * * cd /chemin/vers/CCR && python manage.py generer_rapports_auto >> /tmp/rapports.log 2>&1
```

---

## 📊 Résultats du Test

Exécution du 05/05/2026:
```
✓ Rapport global généré: 18 membres
✓ JUDA (Tribu): 4 membres
✓ SIMEON (Tribu): 3 membres
✓ COM (Département): 4 membres
✓ STATISTIQUE (Département): 6 membres
... et tous les autres
```

---

## 💡 Statistiques Calculées Automatiquement

Pour chaque rapport (global, tribu, département):

📈 **Données Générales:**
- Nombre total de membres
- Membres actifs, nouveaux, inactifs, partis

📊 **Présences:**
- Nombre total de cultes
- Nombre de présences/absences
- Taux de participation (%)

🏛️ **Structure:**
- Répartition par tribu (si rapport global/département)
- Répartition par département (si rapport global/tribu)
- Cultes par type (Dimanche, Mercredi, Spécial)

---

## 🔍 Consultation des Rapports

### Via l'interface web:
```
http://localhost:8000/rapports/
```

### Via l'administration:
```
http://localhost:8000/admin/eglise/rapportmensuel/
```

### Via la base de données:
```python
python manage.py shell
from eglise.models import RapportMensuel
rapports = RapportMensuel.objects.filter(mois=5, annee=2026)
for r in rapports:
    print(f"{r} ({r.tribu or r.departement or 'GLOBAL'}): {r.nombre_total_membres} membres")
```

---

## 📁 Fichiers Créés/Modifiés

| Fichier | État | Description |
|---------|------|-------------|
| `eglise/management/commands/generer_rapports_auto.py` | ✅ Créé | Management command principal |
| `eglise/management/__init__.py` | ✅ Créé | Package Python |
| `eglise/management/commands/__init__.py` | ✅ Créé | Package Python |
| `generer_rapports.py` | ✅ Modifié | Ajout fonction `generer_rapports_tous_structures()` |
| `GUIDE_AUTOMATISATION_RAPPORTS.md` | ✅ Créé | Documentation détaillée |

---

## ⚠️ Points Importants

1. **Base de données:** Assurez-vous que les Tribus et Départements existent avant de générer
2. **Permissions:** L'utilisateur qui exécute la tâche doit avoir accès au projet Django
3. **Horaire:** Recommandé entre 2h et 3h du matin pour éviter les conflits
4. **Logs:** Les erreurs sont enregistrées dans les logs system

---

## 🆘 Besoin d'aide?

1. **Tester manuellement:**
   ```bash
   python manage.py generer_rapports_auto --mois 5 --annee 2026
   ```

2. **Vérifier les données:**
   ```bash
   python manage.py shell
   from eglise.models import Tribu, Departement
   print(f"Tribus: {Tribu.objects.count()}")
   print(f"Départements: {Departement.objects.count()}")
   ```

3. **Consulter la documentation:**
   - Lire: `GUIDE_AUTOMATISATION_RAPPORTS.md`
   - Section: "Troubleshooting"

---

## ✨ Prochaines Étapes (Optionnel)

Pour aller plus loin:
- [ ] Ajouter des notifications email quand rapports sont générés
- [ ] Créer des exports PDF automatiques
- [ ] Ajouter des comparaisons mois/mois
- [ ] Déployer sur serveur production avec Celery Beat

---

**🎉 Système prêt à l'emploi! Exécutez `python manage.py generer_rapports_auto` pour tester.**
