# 🚀 GUIDE RAPIDE - Interface Gestion des Cultes

## 📌 OBJECTIF
Le département de **STATISTIQUE** peut maintenant:
- ✅ Ajouter le nombre de personnes présentes au culte
- ✅ Voir l'évolution sous forme de courbe
- ✅ Voir les statistiques sous forme d'histogramme
- ✅ Gérer tous les cultes (ajouter, modifier, supprimer)

---

## 🔐 ACCÈS

**Connexion requise**: Responsable du département **STATISTIQUE**

### Se connecter comme STATISTIQUE:
1. Aller à: `http://localhost:8000/login/`
2. Se connecter avec les identifiants STATISTIQUE
3. Accéder à: `http://localhost:8000/cultes/`

---

## 📋 INTERFACE PRINCIPALE

### Page: `/cultes/`

```
┌────────────────────────────────────────────────┐
│  📈 Gestion des Cultes - Statistiques          │
├────────────────────────────────────────────────┤
│  [➕ Ajouter un Culte]                         │
├────────────────────────────────────────────────┤
│  📊 Statistiques Rapides:                      │
│  • Total Cultes: 15                            │
│  • Moyenne Participants (3m): 45               │
│  • Cultes (3m): 12                             │
├────────────────────────────────────────────────┤
│  📋 Tableau des Cultes:                        │
│  Date    │ Type     │ Thème  │ 👥    │ Actions │
│  01/01   │ Dimanche │ Amour  │ 50    │ ✏️ 🗑️   │
│  08/01   │ Mercredi │ Grâce  │ 35    │ ✏️ 🗑️   │
│  15/01   │ Dimanche │ Paix   │ 58    │ ✏️ 🗑️   │
└────────────────────────────────────────────────┘
```

---

## ➕ AJOUTER UN CULTE

1. Cliquer: **➕ Ajouter un Culte**

2. Remplir le formulaire:
   ```
   Date du culte *:           [__/__/____]
   Type de culte *:           [Dimanche ▼]
   Thème:                     [________________]
   Prédicateur:               [________________]
   👥 Nombre personnes *:     [___]
   Notes:                     [________________
                               ________________]
   
   [← Retour] [➕ Ajouter]
   ```

3. Cliquer: **➕ Ajouter**

✅ Le culte est créé avec le nombre de participants!

---

## 📊 VOIR LES STATISTIQUES

1. Depuis la liste des cultes, cliquer: **Voir Statistiques →**
   Ou aller à: `/cultes/statistiques/`

2. Vous verrez:

   **📊 Statistiques Globales:**
   - Cultes Totaux: 15
   - Total Participants: 650
   - Moyenne Participants: 43
   - Max - Min: 58 - 25

   **📈 Graphique 1: Courbe d'Évolution**
   ```
   Participants
   60 │     ╱╲      ╱╲
   50 │    ╱  ╲    ╱  ╲
   40 │   ╱    ╲  ╱    ╲
   30 │__╱______╲╱______╲__
      └─────────────────────
      Dates (3 derniers mois)
   ```
   
   **📊 Graphique 2: Histogramme par Type**
   ```
   Moyenne
   50 │  ┌─┐
   40 │  │ │  ┌─┐
   30 │  │ │  │ │  ┌─┐
   20 │  │ │  │ │  │ │
      └──┴─┴──┴─┴──┴─┴────
      Dimanche Mercredi Spécial
   ```

---

## ✏️ MODIFIER UN CULTE

1. Dans le tableau, cliquer: **✏️ Modifier**
2. Modifier les informations
3. Cliquer: **✏️ Modifier**

✅ Les statistiques se mettent à jour automatiquement!

---

## 🗑️ SUPPRIMER UN CULTE

1. Dans le tableau, cliquer: **🗑️ Supprimer**
2. Confirmer la suppression
3. Le culte est supprimé

⚠️ Action irréversible!

---

## 📈 INTERPRÉTATION DES GRAPHIQUES

### Courbe d'Évolution
- **Ligne ascendante** = Plus de participants
- **Ligne descendante** = Moins de participants
- **Points hauts** = Cultes bien fréquentés
- **Points bas** = Cultes moins fréquentés

**Utilité**: Voir si le nombre de participants augmente ou diminue dans le temps

### Histogramme
- **Barres hautes** = Type de culte bien fréquenté
- **Barres basses** = Type de culte moins fréquenté

**Exemple**:
- Dimanche: 50 personnes (culte principal)
- Mercredi: 35 personnes (moins de gens)
- Spécial: 40 personnes (variables)

---

## 💡 CONSEILS D'UTILISATION

✅ **À FAIRE:**
- Mettez à jour le nombre après chaque culte
- Utilisez les graphiques pour identifier les tendances
- Partagez les statistiques avec les responsables
- Comparez les périodes pour voir l'évolution

❌ **À ÉVITER:**
- Ne laissez pas le nombre à 0
- Ne supprimez pas les cultes accidentellement
- Ne modifiez pas les données anciennes sans raison

---

## 🔄 WORKFLOW COMPLET

```
1. DIMANCHE
   └─ Culte à l'église

2. LUNDI (Jour d'après)
   └─ Responsable STAT enregistre le nombre
   └─ Visite: /cultes/ → Ajouter → Remplir

3. FIN DU MOIS
   └─ Directeur voit les statistiques
   └─ Visite: /cultes/ → Voir Statistiques
   └─ Analyse la courbe et l'histogramme

4. ACTIONS
   └─ Si baisse → Alerter l'équipe
   └─ Si hausse → Célébrer!
```

---

## 🔗 LIENS RAPIDES

| Action | URL |
|--------|-----|
| Liste cultes | `/cultes/` |
| Ajouter culte | `/cultes/nouveau/` |
| Statistiques | `/cultes/statistiques/` |
| Modifier culte | `/cultes/<id>/modifier/` |

---

## ❓ QUESTIONS FRÉQUENTES

**Q: Que faire si j'ai oublié le nombre?**
A: Modifiez le culte et entrez le bon nombre

**Q: Les statistiques se mettent à jour automatiquement?**
A: Oui! Dès que vous ajoutez/modifiez un culte

**Q: Puis-je voir l'historique des modifications?**
A: Pas encore, mais c'est possible à faire

**Q: Qui peut voir ces statistiques?**
A: Admin, Pasteur, et Responsable STATISTIQUE

---

## 📞 SUPPORT

Besoin d'aide? Contactez:
- Administrateur du système
- Responsable IT
- Pasteur principal

---

**🎉 Bon suivi des statistiques!**
