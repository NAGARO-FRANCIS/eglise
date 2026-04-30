# 👨‍💻 DOCUMENTATION TECHNIQUE - Système de Gestion des Cultes

## 📁 STRUCTURE DES FICHIERS

```
eglise/
├── forms.py              ✅ Contient CulteForm (formulaire)
├── culte_views.py        ✨ NOUVEAU - 5 vues pour gérer les cultes
├── urls.py               ✅ Contient les 5 URLs pour les cultes
├── models.py             ✅ Modèle Culte existant
├── templates/eglise/
│   ├── culte_list.html               ✨ NOUVEAU - Liste des cultes
│   ├── culte_form.html               ✨ NOUVEAU - Formulaire add/edit
│   └── culte_statistics.html         ✨ NOUVEAU - Graphiques
└── ...
```

---

## 🔧 COMPOSANTS TECHNIQUES

### 1. FORMULAIRE: `CulteForm` (eglise/forms.py)

```python
class CulteForm(forms.ModelForm):
    class Meta:
        model = Culte
        fields = ['date', 'type_culte', 'theme', 'predicateur', 
                  'nombre_participants', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'type_culte': forms.Select(),
            'nombre_participants': forms.NumberInput(attrs={'min': '0'}),
            ...
        }
```

**Champs principaux:**
- `date` (DateField) - Date du culte
- `type_culte` (CharField) - [Dimanche, Mercredi, Spécial, Autre]
- `nombre_participants` (IntegerField) - **CLEF** ⭐
- `theme`, `predicateur`, `notes` - Optionnels

---

### 2. VUES: `eglise/culte_views.py`

#### `CulteListView` (LoginRequiredMixin, TemplateView)
```
GET /cultes/
├─ Récupère tous les cultes
├─ Ajoute statistiques pour chaque culte
└─ Affiche template culte_list.html
```

**Contexte retourné:**
```python
{
    'cultes': QuerySet de Culte triés par -date,
    'form': CulteForm vide,
    'page_title': '📈 Gestion des Cultes',
    'stats': {
        'total_cultes': int,
        'total_cultes_3m': int,
        'moyenne_participants': int,
    }
}
```

#### `CulteCreateView` (LoginRequiredMixin, View)
```
GET  /cultes/nouveau/  → Affiche formulaire vide
POST /cultes/nouveau/  → Crée un Culte et redirige à la liste
```

#### `CulteUpdateView` (LoginRequiredMixin, View)
```
GET  /cultes/<id>/modifier/  → Affiche formulaire pré-rempli
POST /cultes/<id>/modifier/  → Modifie et redirige
```

#### `CulteDeleteView` (LoginRequiredMixin, View)
```
POST /cultes/<id>/supprimer/  → Supprime et redirige
```

#### `CulteStatisticsView` (LoginRequiredMixin, TemplateView)
```
GET /cultes/statistiques/
├─ Récupère cultes des 3 derniers mois
├─ Génère JSON pour graphiques
└─ Affiche statistiques.html avec Chart.js
```

**Contexte retourné:**
```python
{
    'evolution_data_json': JSON pour courbe
    'type_data_json': JSON pour histogramme
    'stats': {
        'total_cultes', 'total_participants',
        'average_participants', 'max_participants', 'min_participants'
    }
}
```

---

### 3. SÉCURITÉ: `dispatch()` method

Chaque vue vérifie:
```python
if not request.user.is_authenticated:
    return redirect('eglise:login')

if request.user.is_superuser:
    return super().dispatch(...)

try:
    profile = request.user.profile
    if profile.role == 'pasteur':
        return super().dispatch(...)
    elif (profile.role == 'responsable' and 
          profile.departement.nom == 'STATISTIQUE'):
        return super().dispatch(...)
except:
    pass

return redirect('eglise:dashboard')  # Accès refusé
```

**Résultat:**
- ✅ Admin/Superuser: Accès complet
- ✅ Pasteur: Accès complet
- ✅ Responsable STATISTIQUE: Accès complet
- ❌ Autres: Redirection au dashboard

---

### 4. TEMPLATES

#### Structure: `culte_list.html`

```html
{% extends 'eglise/base.html' %}

{% block content %}
  <!-- En-tête avec bouton ajouter -->
  <div class="card">
    <h2>{{ page_title }}</h2>
    <a href="{% url 'eglise:culte_create' %}">➕ Ajouter</a>
  </div>

  <!-- Statistiques rapides (3 cards) -->
  <div class="grid">
    <card>Total Cultes: {{ stats.total_cultes }}</card>
    ...
  </div>

  <!-- Tableau des cultes -->
  <table>
    <tr>
      <th>Date</th>
      <th>Type</th>
      <th>👥 Présents</th>
      <th>Actions</th>
    </tr>
    {% for culte in cultes %}
      <tr>
        <td>{{ culte.date|date:"d/m/Y" }}</td>
        <td>{{ culte.get_type_culte_display }}</td>
        <td>{{ culte.nombre_participants }}</td>
        <td>
          <a href="{% url 'eglise:culte_update' culte.id %}">✏️</a>
          <form method="post" action="...delete...">
            <button>🗑️</button>
          </form>
        </td>
      </tr>
    {% endfor %}
  </table>

  <!-- Lien statistiques -->
  <a href="{% url 'eglise:culte_statistics' %}">Statistiques →</a>
{% endblock %}
```

#### Structure: `culte_statistics.html`

```html
{% extends 'eglise/base.html' %}

{% block content %}
  <!-- Statistiques globales (4 cards) -->
  <div class="grid">
    <card>Total: {{ stats.total_cultes }}</card>
    <card>Participants: {{ stats.total_participants }}</card>
    <card>Moyenne: {{ stats.average_participants }}</card>
    <card>Max-Min: {{ stats.max_participants }}-{{ stats.min_participants }}</card>
  </div>

  <!-- Graphique Evolution -->
  <canvas id="evolutionChart"></canvas>
  <script>
    const evolutionData = {{ evolution_data_json|safe }};
    // Crée graphique avec Chart.js
    new Chart(evolutionCtx, {
      type: 'line',
      data: { labels: dates, datasets: [...] },
      options: { ... }
    });
  </script>

  <!-- Graphique Type -->
  <canvas id="typeChart"></canvas>
  <script>
    const typeData = {{ type_data_json|safe }};
    // Crée histogramme
  </script>
{% endblock %}
```

---

## 🔀 FLUX DE DONNÉES

### Ajouter un culte:

```
1. Utilisateur: GET /cultes/nouveau/
   └─ CulteCreateView.get()
      └─ render culte_form.html avec CulteForm vide

2. Utilisateur: POST /cultes/nouveau/ avec données
   └─ CulteCreateView.post()
      └─ form.is_valid()
         ├─ OUI: form.save() → Culte créé
         │       redirect /cultes/
         └─ NON: re-render avec erreurs

3. Page /cultes/ mise à jour
   └─ Nouveau culte visible dans tableau
   └─ Statistiques recalculées
```

### Voir les statistiques:

```
1. Utilisateur: GET /cultes/statistiques/
   └─ CulteStatisticsView.get_context_data()
      ├─ Fetch Culte pour 3 derniers mois
      ├─ Générer evolution_data (JSON)
      │  [{'date': ..., 'participants': ...}, ...]
      ├─ Générer type_data (JSON)
      │  [{'type': 'Dimanche', 'avg': 45}, ...]
      └─ Render culte_statistics.html

2. Template JavaScript (Chart.js):
   ├─ Lit evolution_data_json
   ├─ Crée graphique "line" avec Chart.js
   ├─ Lit type_data_json
   └─ Crée graphique "bar" avec Chart.js
```

---

## 📊 FORMAT DES DONNÉES JSON

### Evolution data (pour courbe):
```json
[
  {
    "date": "01/01/2024",
    "participants": 45,
    "type": "Dimanche",
    "theme": "Amour"
  },
  {
    "date": "08/01/2024",
    "participants": 52,
    "type": "Dimanche",
    "theme": "Grâce"
  }
]
```

### Type data (pour histogramme):
```json
[
  {
    "type": "Dimanche",
    "count": 8,
    "avg_participants": 48
  },
  {
    "type": "Mercredi",
    "count": 4,
    "avg_participants": 32
  }
]
```

---

## 🔗 URLS MAPPING

```
Route                              Nom            Vue                  Méthode
─────────────────────────────────────────────────────────────────────────────
/cultes/                           culte_list     CulteListView        GET
/cultes/nouveau/                   culte_create   CulteCreateView      GET, POST
/cultes/<id>/modifier/             culte_update   CulteUpdateView      GET, POST
/cultes/<id>/supprimer/            culte_delete   CulteDeleteView      POST
/cultes/statistiques/              culte_stats    CulteStatisticsView  GET
```

---

## 🧪 TESTING

### Test unitaire simple:

```python
from django.test import TestCase
from eglise.models import Culte
from datetime import date

class CulteTestCase(TestCase):
    def setUp(self):
        Culte.objects.create(
            date=date(2024, 1, 1),
            type_culte='dimanche',
            nombre_participants=45
        )
    
    def test_culte_creation(self):
        culte = Culte.objects.get(date=date(2024, 1, 1))
        self.assertEqual(culte.nombre_participants, 45)
    
    def test_culte_list_view(self):
        response = self.client.get('/cultes/')
        self.assertEqual(response.status_code, 302)  # Redirection sans auth
```

---

## 🚀 EXTENSIONS POSSIBLES

1. **Export PDF**
   ```python
   def export_pdf(request):
       cultes = Culte.objects.all()
       # Utiliser reportlab ou weasyprint
       return PDF response
   ```

2. **Comparaison périodes**
   ```python
   class CulteComparisonView(TemplateView):
       # Comparer deux périodes
       # Afficher les différences
   ```

3. **Filtres avancés**
   ```python
   # Filtrer par date range
   # Filtrer par type de culte
   # Filtrer par prédicateur
   ```

4. **Notifications**
   ```python
   # Alerter si baisse de participation
   # Envoyer emails au pasteur
   ```

5. **API REST**
   ```python
   # Créer endpoints API pour mobile
   # GET /api/cultes/
   # POST /api/cultes/
   ```

---

## 🐛 DÉPANNAGE

### Erreur: "No attribute 'CulteListView'"
**Cause:** Oubli de l'import `from . import culte_views` dans urls.py
**Solution:** Ajouter l'import en haut de urls.py

### Erreur: "Access denied"
**Cause:** Utilisateur non autorisé
**Solution:** Vérifier que l'utilisateur est:
- Connecté
- Responsable du département STATISTIQUE (ou admin/pasteur)

### Graphiques vides
**Cause:** Pas de données pour la période
**Solution:** Ajouter des cultes d'abord

### Erreur Template
**Cause:** Fichier HTML manquant ou mal placé
**Solution:** Vérifier chemin: `eglise/templates/eglise/culte_*.html`

---

## 📦 DÉPENDANCES

- Django (déjà installé)
- Chart.js (CDN dans template)
- Aucune nouvelle dépendance Python requise!

---

## 🔄 PROCESSUS DE MAINTENANCE

### Mise à jour du formulaire:
1. Modifier `CulteForm` dans forms.py
2. Les vues l'utilisent automatiquement
3. Templates s'adaptent

### Ajout de nouveau champ:
1. Modifier modèle `Culte`
2. Créer migration: `python manage.py makemigrations`
3. Appliquer: `python manage.py migrate`
4. Ajouter au formulaire CulteForm
5. Mettre à jour templates

### Changement des statistiques:
1. Modifier `get_context_data()` dans CulteStatisticsView
2. Modifier le template JS si nécessaire
3. Tester les graphiques

---

## ✅ CHECKLIST DÉPLOIEMENT

- [ ] Tous les fichiers créés
- [ ] Imports vérifiés
- [ ] URLs enregistrées
- [ ] Permissions vérifiées
- [ ] Département STATISTIQUE existe
- [ ] Templates affichés correctement
- [ ] Graphiques Chart.js fonctionnent
- [ ] Sécurité vérifiée
- [ ] Tests passent
- [ ] Documentation complète

---

**✨ IMPLÉMENTATION PRÊTE POUR LA PRODUCTION!**
