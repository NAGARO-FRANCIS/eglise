# 📅 Guide: Automatisation des Rapports Mensuels par Tribu/Département

## 🎯 Objectif

Générer **automatiquement** chaque 1er du mois:
- ✅ Rapport mensuel **GLOBAL** (tous les membres)
- ✅ Rapports **par TRIBU** (1 rapport par tribu)
- ✅ Rapports **par DÉPARTEMENT** (1 rapport par département)

## 🚀 Utilisation Rapide

### 1️⃣ Tester manuellement (toutes les structures)
```bash
python manage.py generer_rapports_auto
```

### 2️⃣ Générer pour un mois spécifique
```bash
# Pour mai 2026
python manage.py generer_rapports_auto --mois 5 --annee 2026

# Pour le mois précédent
python manage.py generer_rapports_auto --prev
```

### 3️⃣ Générer pour une tribu ou département spécifique
```bash
# Rapports pour la tribu ID=1
python manage.py generer_rapports_auto --tribu 1

# Rapports pour le département ID=2
python manage.py generer_rapports_auto --departement 2
```

### 4️⃣ Générer aussi avec le script Python
```bash
# Depuis le répertoire racine du projet
python generer_rapports.py

# Cela va générer:
# 1. Rapport global du mois courant
# 2. Rapports pour chaque tribu
# 3. Rapports pour chaque département
```

---

## ⏰ Configuration Automatique (Le 1er du mois)

### **Option A: WINDOWS (Windows Task Scheduler)**

#### Étapes:

1. **Ouvrir le Planificateur de tâches**
   - Appuyez sur `Windows + R`
   - Tapez `taskschd.msc` et appuyez sur Entrée

2. **Créer une nouvelle tâche basique**
   - Clic droit → "Créer une tâche..."
   - Onglet "Général"
     - Nom: `Rapports Mensuels CCR`
     - Cochez "Exécuter avec les autorisations maximales"

3. **Configuration du déclencheur (Onglet "Déclencheurs")**
   - Clic sur "Nouveau..."
   - Type: `Mensuelle`
   - Mois: `Tous les mois`
   - Jour: `1er jour`
   - Heure: `02:00:00` (à 2h du matin)

4. **Configuration de l'action (Onglet "Actions")**
   - Clic sur "Nouveau..."
   - Action: `Démarrer un programme`
   - Programme: `C:\Python314\python.exe` (adapter votre chemin Python)
   - Arguments: 
   ```
   C:\projet\CCR\manage.py generer_rapports_auto
   ```
   - Démarrer dans: `C:\projet\CCR`

5. **Conditions (Onglet "Conditions")**
   - ✓ Démarrer la tâche seulement si l'ordinateur est en veille: DÉCOCHEZ
   - ✓ Réveiller l'ordinateur pour exécuter: COCHEZ

6. **Paramètres (Onglet "Paramètres")**
   - ✓ Si la tâche échoue, recommencer après: `10 minutes`
   - ✓ Arrêter la tâche si elle s'exécute plus longtemps que: `1 heure`

7. **Cliquez OK** et entrez votre mot de passe Windows si demandé

#### ✅ Test de la tâche:
```powershell
# Exécuter manuellement
C:\projet\CCR> python manage.py generer_rapports_auto

# Ou depuis le répertoire racine
python generer_rapports.py
```

---

### **Option B: LINUX/MAC (CRON)**

1. **Ouvrir le crontab**
```bash
crontab -e
```

2. **Ajouter la ligne pour exécuter le 1er du chaque mois à 2h du matin**
```bash
# Format: minute heure jour mois jour_semaine commande
0 2 1 * * cd /chemin/vers/CCR && python manage.py generer_rapports_auto >> /tmp/rapports_mensuels.log 2>&1
```

**Explication:**
- `0 2` = À 2h du matin
- `1` = Le 1er du mois
- `*` = Chaque mois
- `*` = N'importe quel jour de semaine

3. **Alternative avec le script Python:**
```bash
0 2 1 * * cd /chemin/vers/CCR && python generer_rapports.py >> /tmp/rapports_mensuels.log 2>&1
```

4. **Vérifier les tâches cron**
```bash
crontab -l
```

---

### **Option C: DOCKER (pour production)**

Si vous utilisez Docker:

```dockerfile
# Dans votre Dockerfile
RUN apt-get install -y dcron

# Ajouter la tâche cron
RUN echo "0 2 1 * * cd /app/CCR && python manage.py generer_rapports_auto" | crontab -

# Démarrer cron
CMD ["crond", "-f", "-l", "2"]
```

---

### **Option D: Celery Beat (pour production avancée)**

Si vous avez Celery:

1. **Installer Celery**
```bash
pip install celery redis
```

2. **Créer `eglise/tasks.py`**
```python
from celery import shared_task
from django.core.management import call_command

@shared_task
def generer_rapports_mensuels():
    """Génère les rapports mensuels chaque 1er du mois"""
    call_command('generer_rapports_auto')
    return "Rapports générés avec succès"
```

3. **Configurer dans `settings.py`**
```python
CELERY_BEAT_SCHEDULE = {
    'generer-rapports-mensuels': {
        'task': 'eglise.tasks.generer_rapports_mensuels',
        'schedule': crontab(hour=2, minute=0, day_of_month=1),  # 1er du mois à 2h
    },
}
```

4. **Lancer Celery Beat**
```bash
celery -A CCR beat -l info
```

---

## 📊 Qu'est-ce qui est généré?

### Par exécution automatique, voici ce qui est créé:

**Rapports Mensuels:**
- 1 rapport **GLOBAL** (tous les membres)
- 1 rapport par **TRIBU** (ex: "Tribu A", "Tribu B", ...)
- 1 rapport par **DÉPARTEMENT** (ex: "Dept Ados", "Dept Enfants", ...)

**Statistiques calculées pour chaque rapport:**
- ✅ Nombre total de membres
- ✅ Membres actifs, nouveaux, inactifs, partis
- ✅ Nombre de cultes
- ✅ Nombre total de présences/absences
- ✅ Taux de participation (%)
- ✅ Répartition par type de culte (Dimanche, Mercredi, Spécial)
- ✅ Membres par tribu/département

---

## 🔍 Vérifier les rapports générés

### Via l'interface web:
1. Allez à `http://localhost:8000/rapports/`
2. Consultez les rapports créés

### Via l'admin Django:
1. `http://localhost:8000/admin/eglise/rapportmensuel/`
2. Filtrez par mois/année
3. Vérifiez les rapports par tribu et département

### Via la base de données:
```python
# Dans Django shell
python manage.py shell
from eglise.models import RapportMensuel
from datetime import datetime

# Rapports du mois courant
rapports = RapportMensuel.objects.filter(
    mois=datetime.now().month,
    annee=datetime.now().year
)

for rapport in rapports:
    print(f"{rapport.periode_str} - {rapport.tribu or rapport.departement or 'GLOBAL'}: {rapport.nombre_total_membres} membres")
```

---

## 📝 Logs et Debugging

### Voir les logs de la tâche (Windows):
1. Ouvrez l'Observateur d'événements (`Event Viewer`)
2. Allez à: `Windows Logs` → `System`
3. Cherchez les événements de la tâche planifiée

### Voir les logs (Linux):
```bash
tail -f /tmp/rapports_mensuels.log
```

### Forcer la génération manuelle pour tester:
```bash
python manage.py generer_rapports_auto --mois 5 --annee 2026 --tribu 1
```

---

## ⚠️ Troubleshooting

### Erreur: "Module django not found"
```bash
# Activer l'environnement virtuel avant la tâche
C:\projet\CCR\venv\Scripts\activate && python manage.py generer_rapports_auto
```

### Erreur: "Database is locked"
- Réduisez la fréquence de la tâche
- Vérifiez que personne ne modifier la BD au moment de l'exécution

### Aucun rapport généré
```bash
# Vérifier qu'il y a des données
python manage.py shell
from eglise.models import Membre, Tribu, Departement
print(f"Membres: {Membre.objects.count()}")
print(f"Tribus: {Tribu.objects.count()}")
print(f"Départements: {Departement.objects.count()}")
```

---

## 📞 Support

Pour plus d'aide:
1. Vérifiez les logs de l'application
2. Testez manuellement: `python manage.py generer_rapports_auto`
3. Consultez la documentation Django management commands
