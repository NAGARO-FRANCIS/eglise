# 📋 GESTION DES RAPPORTS MENSUELS - INTERFACE ADMIN

## 🔑 Accès à l'administration

1. Allez à: http://localhost:8000/admin/
2. Connectez-vous avec vos identifiants
3. Allez à: **Eglise → Rapports Mensuels**

## 📊 Liste des rapports

Vous verrez une liste avec:
- **Période**: Mois et Année
- **Structure**: Global / Tribu / Département
- **Statut**: Brouillon / Validé / Archivé
- **Date**: Date de création/modification

### Filtres disponibles

- **Par Statut**: Brouillon, Validé, Archivé
- **Par Structure**: Global, Tribu A, Tribu B, Département 1, etc.
- **Par Année**: 2025, 2026, etc.

### Recherche

Vous pouvez chercher par:
- Mois/Année
- Nom de tribu
- Nom de département

## 🔍 Consulter un rapport

1. Cliquez sur un rapport dans la liste
2. Vous verrez les détails:

### Données affichées

- **Identification**: Mois, Année, Structure
- **Membres**: Total, Actifs, Nouveaux, Inactifs, Partis
- **Détails par structure**: Répartition par tribu/département
- **Assistances**: Cultes, Présences, Absences, Taux
- **Cultes par type**: Types et participants
- **Notes**: Observations/commentaires

## ✏️ Modifier un rapport

1. Cliquez sur le rapport
2. Modifiez les données que vous souhaitez
3. Changez le **Statut** si nécessaire:
   - **Brouillon**: Rapports en cours
   - **Validé**: Rapports approuvés
   - **Archivé**: Rapports anciens

4. Cliquez **Enregistrer**

## 🆚 Comparaison de rapports

Pour comparer deux périodes:

1. Consultez le rapport du mois A
2. Ouvrez dans un nouvel onglet le rapport du mois B
3. Comparez les chiffres clés:
   - Évolution des membres actifs
   - Évolution du taux de participation
   - Évolution des cultes

### Exemple d'analyse

```
Janvier 2026:
- Membres actifs: 15
- Taux de participation: 85%
- Cultes: 4

Février 2026:
- Membres actifs: 16 (+1)
- Taux de participation: 88% (+3%)
- Cultes: 5 (+1)

→ Tendance positive! 📈
```

## 📈 Graphiques

Sur le site public (http://localhost:8000/rapports/):

1. Allez à la liste des rapports
2. Cliquez sur un rapport
3. Vous verrez les graphiques interactifs:
   - Évolution des membres
   - Taux de participation
   - Distribution par type de culte

### Utiliser les graphiques

- **Survol**: Voir les valeurs exactes
- **Clic** sur la légende: Masquer/afficher une série
- **Zoom**: Certains graphiques permettent le zoom

## 🎯 Bonnes pratiques

### Après génération automatique (1er du mois)

1. ✅ Vérifiez les données (les chiffres sont corrects?)
2. ✅ Lisez les notes et observations
3. ✅ Changez le statut en **"Validé"** si tout est OK
4. ✅ Ajoutez des commentaires si nécessaire

### Pour l'archivage

- Changez le statut en **"Archivé"** pour les anciens rapports
- Les rapports archivés resteront accessibles mais ne seront pas au premier plan

## 📱 Statut des rapports - Code couleur

| Statut | Couleur | Signification |
|--------|---------|---|
| Brouillon | ⚪ Gris | Rapport généré, en attente de validation |
| Validé | 🟢 Vert | Rapport approuvé et finalisé |
| Archivé | 🟠 Orange | Rapport ancien, archivé |

## 🔐 Permissions

- **Admin**: Accès complet (lecture, modification, suppression)
- **Patriarche de tribu**: Voir les rapports de sa tribu
- **Responsable de département**: Voir les rapports de son département

## 📞 Problèmes courants

### "Aucun rapport trouvé pour ce mois"
→ Vérifiez que les rapports ont été générés (ils le sont automatiquement le 1er du mois)

### "Les chiffres ne sont pas à jour"
→ Les rapports capturent les données au moment de la génération
→ Les modifications ultérieures ne changent pas le rapport déjà généré
→ Un nouveau rapport sera généré le mois suivant

### "Je veux régénérer un rapport"
→ Vous pouvez relancer manuellement:
   ```bash
   python manage.py generer_rapports_auto --mois 5 --annee 2026
   ```

## 🎓 Cas d'usage courants

### 1. Validation mensuelle

```
1. Serveur génère les rapports (1er du mois)
2. Admin consulte les rapports
3. Admin valide ou modifie si nécessaire
4. Statut passe à "Validé"
5. Rapports visibles pour statistiques/analyses
```

### 2. Suivi trimestriel

```
1. Consultez les 3 rapports du trimestre
2. Analysez l'évolution
3. Identifiez les tendances
4. Rapportez les insights à la direction
```

### 3. Rapport pour une structure

```
1. Allez à "Eglise → Rapports Mensuels"
2. Filtrez par Structure (ex: "Tribu A")
3. Consultez tous les rapports de la tribu
4. Analysez les performances
```

## 🔗 Liens utiles

- [Interface web des rapports](http://localhost:8000/rapports/) - Graphiques et statistiques
- [Guide complet d'automatisation](GUIDE_AUTOMATISATION_RAPPORTS_MENSUELS.md)
- [Implémentation détaillée](IMPLEMENTATION_AUTOMATISATION_COMPLETE.md)

---

**Note**: Les rapports sont générés automatiquement le 1er du mois à 00:15 UTC.
Il n'est pas nécessaire de les générer manuellement sauf en cas de besoin particulier.
