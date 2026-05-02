# Test de Visibilité du Bouton "Ajouter Participation"

## Vérification des accès

### Pour accéder à la page avec le bouton:
**URL:** `http://localhost:8000/cultes/statistiques/`

### Permissions requises:
- Être **Superuser** (Admin)
- OU être **Pasteur**
- OU être **Responsable du Département STATISTIQUE**

### Comment tester:

1. **Ouvrez votre navigateur** et allez sur:
   ```
   http://localhost:8000/cultes/statistiques/
   ```

2. **Vous devriez voir:**
   - En haut de la page, une section violette/bleue
   - Le texte: "📊 Interface de Gestion - Département Statistique"
   - Un gros bouton BLANC avec le texte: **"➕ Ajouter une Participation"**

3. **Cliquez sur le bouton** et un formulaire modal devrait s'afficher avec:
   - Champ: Date du Dimanche
   - Champ: Nombre de Participants
   - Champ: Nombre de Nouveaux
   - Boutons: Annuler | Enregistrer

4. **Remplissez le formulaire:**
   - Date: 29/04/2026
   - Participants: 5000
   - Nouveaux: 50

5. **Cliquez "Enregistrer"** et attendez le message de confirmation

---

## Dépannage

### Le bouton n'apparaît pas?

**1. Vérifiez l'URL:**
- Assurez-vous d'être sur: `/cultes/statistiques/`
- Pas sur: `/statistiques/` (c'est une page différente)

**2. Vérifiez vos permissions:**
```python
# Ouvrez Django Shell:
python manage.py shell

# Vérifiez votre utilisateur:
from eglise.models import UserProfile
user = UserProfile.objects.get(user__username='votre_username')
print(user.role)  # Doit être: pasteur, admin, ou responsable
print(user.departement)  # Doit être: STATISTIQUE (si responsable)
```

**3. Videz le cache du navigateur:**
- Appuyez sur `Ctrl+Shift+Delete` (Windows)
- Ou `Cmd+Shift+Delete` (Mac)
- Sélectionnez "Cache" et "Cookies"
- Appuyez sur "Vider"

**4. Ouvrez la Console du Navigateur:**
- Appuyez sur `F12` ou `Ctrl+Shift+I`
- Allez sur l'onglet "Console"
- Recherchez les messages d'erreur (en rouge)
- Les messages de debug (en bleu) commenceront par "Page statistiques chargée"

### Le bouton apparaît mais ne fonctionne pas?

**Vérifiez la console du navigateur (F12):**
```
✅ Si vous voyez: "Page statistiques chargée" et "Tous les éléments trouvés"
   → Tout devrait fonctionner

❌ Si vous voyez des erreurs (rouge)
   → Prenez une capture d'écran et rapportez-la
```

---

## Informations du Système

**Date actuelle:** 30/04/2026
**Version Django:** 4.0+
**Database:** SQLite (db.sqlite3)
**Fichier template:** `eglise/templates/eglise/culte_statistics.html`
**Fichier modèle:** `eglise/models.py` (Culte)
**Fichier forme:** `eglise/forms.py` (ParticipationDimanchemForm)
