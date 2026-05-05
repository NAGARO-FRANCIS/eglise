# 🤖 Système d'Automatisation des Rapports Mensuels

## Vue d'ensemble

Le système d'automatisation génère **automatiquement** les rapports mensuels chaque mois pour:
- ✅ Le rapport **GLOBAL** (tous les membres)
- ✅ Les rapports par **TRIBU** (chaque tribu)
- ✅ Les rapports par **DÉPARTEMENT** (chaque département)

## 📅 Calendrier d'exécution

Les rapports sont générés **automatiquement le 1er du mois à 00:15 UTC** (selon votre TIME_ZONE configuré).

Par exemple:
- **1er janvier 2026 à 00:15** → Génération du rapport de décembre 2025
- **1er février 2026 à 00:15** → Génération du rapport de janvier 2026
- etc.

## 🔧 Configuration

### 1. Installation des dépendances

```bash
pip install -r requirements.txt
```

Cela installe:
- `APScheduler==3.10.4` - Planificateur de tâches
- `python-dateutil==2.8.2` - Utilitaires de dates

### 2. Fuseau horaire

Le fuseau horaire est configuré dans `CCR/settings.py`:

```python
TIME_ZONE = 'Africa/Kinshasa'  # Changez selon votre région
```

**Exemples de fuseaux horaires:**
- `'Africa/Kinshasa'` - RDC
- `'Africa/Dakar'` - Sénégal
- `'Europe/Paris'` - France
- `'UTC'` - Temps universel

### 3. Démarrage de l'application

L'automatisation démarre **automatiquement** quand vous lancez le serveur Django:

```bash
python manage.py runserver
```

Vous verrez dans la console:

```
✅ Scheduler APScheduler démarré avec succès!
   📅 Tâche: Génération des rapports chaque 1er du mois à 00:15 UTC
```

## 📊 Données générées

Pour chaque tribu et département, le rapport contient:

### Données sur les membres
- Nombre total de membres
- Nombre de membres actifs
- Nombre de nouveaux membres (ce mois)
- Nombre de membres inactifs
- Nombre de membres partis
- Membre par tribu (pour rapport global/département)
- Membres par département (pour rapport global/tribu)

### Statistiques d'assistance
- Nombre de cultes
- Nombre total de présences
- Nombre total d'absences
- Taux de participation moyen

### Données par type de culte
- Nombre de cultes par type
- Nombre de participants par type

## 🚀 Utilisation manuelle

### Générer les rapports manuellement

Vous pouvez aussi générer les rapports manuellement à tout moment:

```bash
# Générer pour le mois courant
python manage.py generer_rapports_auto

# Générer pour le mois précédent
python manage.py generer_rapports_auto --prev

# Générer pour un mois/année spécifique
python manage.py generer_rapports_auto --mois 3 --annee 2026

# Générer pour une tribu spécifique
python manage.py generer_rapports_auto --tribu 1

# Générer pour un département spécifique
python manage.py generer_rapports_auto --departement 1
```

### Lancer la génération directement en Python

```bash
python generer_rapports.py
```

## 📋 Statut des rapports

Après génération, les rapports ont le statut **"Brouillon"** par défaut.

Vous pouvez les valider dans l'administration Django:
1. Allez à http://localhost:8000/admin/
2. Allez à **Eglise → Rapports Mensuels**
3. Cliquez sur un rapport
4. Changez le statut à **"Validé"** ou **"Archivé"**

## 📝 Fichiers modifiés/créés

### Fichiers modifiés
- `requirements.txt` - Ajout de APScheduler et python-dateutil
- `CCR/settings.py` - Ajout de SchedulerConfig, logging, TIME_ZONE

### Fichiers créés
- `scheduler/` - Nouvelle application Django
  - `__init__.py`
  - `apps.py` - Configuration de l'app
  - `scheduler.py` - Logique de planification
  - `models.py`
  - `admin.py`
  - `urls.py`
  - `migrations/` - Migrations Django

## 🐛 Logs et débogage

Les logs du scheduler sont écrits dans:
- **Console** - Messages en direct
- **logs/scheduler.log** - Historique complet

Pour voir les logs en temps réel:

```bash
# Linux/Mac
tail -f logs/scheduler.log

# Windows (PowerShell)
Get-Content logs/scheduler.log -Wait
```

## ⚙️ Personnalisation avancée

### Changer l'heure de génération

Modifiez dans `scheduler/scheduler.py`:

```python
scheduler.add_job(
    generate_monthly_reports,
    trigger=CronTrigger(hour=2, minute=30, day=1),  # 2h30 le 1er du mois
    ...
)
```

### Générer à une autre fréquence

Par exemple, générer tous les dimanches:

```python
trigger=CronTrigger(day_of_week=6, hour=22)  # Dimanche 22h
```

Pour plus d'options: https://apscheduler.readthedocs.io/en/stable/modules/triggers/cron.html

## ✅ Vérification du système

Pour vérifier que tout fonctionne:

1. **Démarrez le serveur:**
   ```bash
   python manage.py runserver
   ```

2. **Vérifiez le message de démarrage du scheduler dans la console**

3. **Allez à http://localhost:8000/rapports/ pour voir les rapports générés**

4. **Consultez les logs:**
   ```bash
   tail -f logs/scheduler.log
   ```

## 🔐 Notes de sécurité

- Le scheduler fonctionne **en arrière-plan** avec la même base de données que Django
- Les données sont **vérifiées et filtrées** par tribu/département
- Les rapports peuvent être **archivés** sans risque

## 📞 Dépannage

### Le scheduler ne démarre pas
1. Vérifiez que `scheduler.apps.SchedulerConfig` est dans `INSTALLED_APPS`
2. Vérifiez les permissions sur le répertoire `logs/`
3. Vérifiez les logs pour les erreurs

### Les rapports ne sont pas générés
1. Vérifiez l'heure de l'ordinateur
2. Vérifiez le TIME_ZONE configuré
3. Vérifiez que le serveur Django est en cours d'exécution
4. Consultez `logs/scheduler.log` pour les erreurs

### Erreurs de génération
1. Vérifiez que les données de membres/cultes existent
2. Vérifiez les logs pour les détails
3. Essayez de générer manuellement: `python manage.py generer_rapports_auto`

---

**Version:** 1.0  
**Dernière mise à jour:** 2026-05-04
