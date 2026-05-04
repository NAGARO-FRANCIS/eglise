# 📋 Guide: Séparation des Cultes Locaux vs Globaux

## 🎯 Concept

Le système a été amélioré pour **séparer complètement** les données de participation entre:

1. **Cultes GLOBAUX**: Utilisés pour les statistiques générales dans "Gestion - Département"
2. **Cultes LOCAUX**: Utilisés UNIQUEMENT pour les courbes de participation par tribu/département

### ✨ Bénéfices

- ✅ Les statistiques globales ne sont **JAMAIS** affectées par les cultes locaux
- ✅ Les courbes tribu/département sont **indépendantes** des stats globales
- ✅ Chaque structure (tribu/département) peut avoir ses propres cultes
- ✅ Pas d'interférence de données

---

## 🔧 Implémentation Technique

### Modèle Culte

Le modèle `Culte` a reçu 3 nouveaux champs:

```python
class Culte(models.Model):
    # ... champs existants ...
    
    # NOUVEAUX CHAMPS
    scope = models.CharField(
        max_length=20,
        choices=[
            ('global', 'Global'),
            ('tribu', 'Tribu'),
            ('departement', 'Département'),
        ],
        default='global',
        help_text='Global ou local à une structure'
    )
    
    tribu = models.ForeignKey('Tribu', null=True, blank=True, help_text='Tribu si culte local')
    departement = models.ForeignKey('Departement', null=True, blank=True, help_text='Département si culte local')
```

### Types de Cultes

#### Culte GLOBAL (scope='global')
- ✅ Affecte les statistiques dans "Gestion"
- ✅ Compté dans les KPIs globaux
- ✅ Utilisé pour la courbe d'évolution globale
- ❌ Ne devrait pas être lié à une tribu/département

#### Culte LOCAL TRIBU (scope='tribu', tribu=...)
- ✅ Affecte SEULEMENT la courbe de participation de la tribu
- ✅ Compté dans les graphiques tribu de "Analyse"
- ❌ N'affecte PAS les statistiques globales
- ❌ Ignore les cultes globaux pour cette tribu

#### Culte LOCAL DÉPARTEMENT (scope='departement', departement=...)
- ✅ Affecte SEULEMENT la courbe de participation du département
- ✅ Compté dans les graphiques département de "Analyse"
- ❌ N'affecte PAS les statistiques globales
- ❌ Ignore les cultes globaux pour ce département

---

## 📊 Statistiques par Type

### Partie "Gestion - Département" (Global)

**Inclut SEULEMENT:**
- Cultes avec `scope='global'`
- Présences de ces cultes

**Exclut:**
- Tous les cultes locaux (tribu ou département)
- Toutes les présences locales

**Impact:**
```
KPIs:
- taux_participation_1m/3m: Calculé SANS cultes locaux
- cultes_1m: Compte SEULEMENT les cultes globaux
- Top participants: Basé SEULEMENT sur cultes globaux
```

### Graphique "Participation par Tribu"

**Inclut SEULEMENT:**
- Cultes avec `scope='tribu'` et `tribu=X`
- Présences de ces cultes

**Résultat:**
- Chaque tribu a sa courbe **indépendante**
- N'affecte pas les statistiques globales

### Graphique "Participation par Département"

**Inclut SEULEMENT:**
- Cultes avec `scope='departement'` et `departement=X`
- Présences de ces cultes

**Résultat:**
- Chaque département a sa courbe **indépendante**
- N'affecte pas les statistiques globales

---

## 🚀 Comment Utiliser

### 1️⃣ Créer un Culte GLOBAL (Principal)

**Où**: Page principal "Ajouter un Culte"

```
- Scope: "Global" (par défaut)
- Tribu: (vide)
- Département: (vide)
- Membres: Sélectionnez les participants globaux
```

**Effet**: 
- ✅ Affecte "Gestion - Département"
- ✅ Compte pour KPIs

---

### 2️⃣ Créer un Culte LOCAL de TRIBU

**Où**: Page "Tribu Membres" (pour une tribu spécifique)

```
- Scope: "Tribu"
- Tribu: (auto-rempli avec la tribu actuelle)
- Département: (vide)
- Membres: Sélectionnez les participants de CETTE tribu
```

**Effet**:
- ❌ N'affecte PAS "Gestion"
- ✅ Affecte la courbe tribu dans "Analyse"
- ✅ Les présences comptent SEULEMENT pour cette tribu

---

### 3️⃣ Créer un Culte LOCAL de DÉPARTEMENT

**Où**: Page "Département Membres" (pour un département spécifique)

```
- Scope: "Département"
- Tribu: (vide)
- Département: (auto-rempli avec le département actuel)
- Membres: Sélectionnez les participants de CE département
```

**Effet**:
- ❌ N'affecte PAS "Gestion"
- ✅ Affecte la courbe département dans "Analyse"
- ✅ Les présences comptent SEULEMENT pour ce département

---

## 📈 Fluxogramme de Filtrage

### Statistiques Globales
```
Culte créé
    ↓
Est-ce scope='global'?
    ├─ OUI → ✅ Compté dans statistiques
    └─ NON → ❌ Ignoré
```

### Graphiques Tribu
```
Culte créé pour Tribu X
    ↓
Est-ce scope='tribu' ET tribu=X?
    ├─ OUI → ✅ Compté dans courbe Tribu X
    └─ NON → ❌ Ignoré
```

### Graphiques Département
```
Culte créé pour Département Y
    ↓
Est-ce scope='departement' ET departement=Y?
    ├─ OUI → ✅ Compté dans courbe Département Y
    └─ NON → ❌ Ignoré
```

---

## 🔍 Détails Techniques

### Filtre utilisé dans les Views

```python
# Cultes GLOBAUX uniquement
cultes = Culte.objects.exclude(scope__in=['tribu', 'departement'])

# Présences GLOBALES uniquement
presences = Presence.objects.exclude(culte__scope__in=['tribu', 'departement'])

# Cultes LOCAUX d'une tribu
cultes_tribu = Culte.objects.filter(scope='tribu', tribu=tribu)

# Cultes LOCAUX d'un département
cultes_dept = Culte.objects.filter(scope='departement', departement=dept)
```

### Méthodes Modifiées

| Méthode | Changement |
|---------|-----------|
| `_calculer_taux_participation()` | Paramètre `include_local` ajouté (défaut: False) |
| `_calculer_participation_par_tribu()` | Utilise SEULEMENT cultes locaux tribu |
| `_calculer_participation_par_departement()` | Utilise SEULEMENT cultes locaux département |
| `StatistiquesView.get_context_data()` | Exclut cultes locaux des KPIs |

---

## ✅ Checklist de Vérification

Après implémentation, vérifiez:

- [ ] Les cultes globaux affectent "Gestion"
- [ ] Les cultes locaux n'affectent PAS "Gestion"
- [ ] Les courbes tribu utilisent seulement cultes tribu locaux
- [ ] Les courbes département utilisent seulement cultes département locaux
- [ ] Les statistiques globales sont **complètement indépendantes** des courbes locales
- [ ] Les KPIs se calculent correctement sans cultes locaux
- [ ] La liste "Top participants" exclut les cultes locaux

---

## 📝 Exemple Pratique

### Scénario

Vous avez:
- 1 **Culte Global** (Dimanche 1er Mai) - 50 participants
- 3 **Cultes Locaux Tribu** (Réunions tribu) - 10, 12, 15 participants
- 2 **Cultes Locaux Département** (Réunions département) - 8, 9 participants

### Résultats

**Gestion - Département:**
- Cultes ce mois: 1 (SEULEMENT le global)
- Participants: 50 (SEULEMENT du culte global)
- Taux: Basé SEULEMENT sur le culte global

**Analyse - Tribu A:**
- Courbe: Basée sur 10 + 12 + 15 = 37 cultes cumulés
- Indépendante du culte global

**Analyse - Département X:**
- Courbe: Basée sur 8 + 9 = 17 cultes cumulés
- Indépendante du culte global

✅ **Les trois données sont complètement séparées!**

---

## 🐛 Dépannage

### Q: Mon culte local affecte toujours les stats globales
**R:** Vérifiez que `scope` n'est PAS 'global'. Vérifiez dans l'admin:
```
eglise/culte/XX/
Scope: doit être 'tribu' ou 'departement'
```

### Q: Les courbes tribu/département sont vides
**R:** Vérifiez:
1. Il y a des cultes créés avec `scope='tribu'` ou `scope='departement'`
2. Les cultes ont la bonne tribu/département assignée
3. Il y a des présences pour ces cultes

### Q: Comment voir les cultes par type?
**R:** Dans l'admin Django:
```
eglise/culte/
Filtrer par "Scope": Global | Tribu | Département
```

---

## 📞 Support

Pour toute question sur la séparation des cultes:
1. Vérifiez le `Scope` du culte dans l'admin
2. Vérifiez la `Tribu` ou `Département` assigné
3. Assurez-vous que les présences sont enregistrées pour le culte

**Rappel**: Les cultes GLOBAUX affectent "Gestion", les cultes LOCAUX affectent les courbes tribu/département.
