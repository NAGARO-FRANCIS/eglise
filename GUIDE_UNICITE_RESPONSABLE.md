# Guide d'Utilisation: Restriction d'Unicité des Responsables

## Vue d'Ensemble

À partir de maintenant, votre système garantit que:
- **Une tribu ne peut avoir qu'un seul patriarche**
- **Un département ne peut avoir qu'un seul responsable**

Cela signifie que si Adelphe est responsable du département de statistique, aucun autre utilisateur ne peut se connecter ni être assigné comme responsable de statistique.

## Scénarios d'Utilisation

### Scénario 1: Inscription d'un Nouveau Patriarche

#### Cas Nominal (Tribu Sans Patriarche)
```
Utilisateur: Marie
1. Clique sur "S'inscrire"
2. Sélectionne "Patriarche de Tribu"
3. Remplit les informations
4. Sélectionne "Tribu Alpha" (qui n'a pas de patriarche)
5. Clique sur "S'inscrire"
6. ✓ Profil créé avec succès
7. Connexion automatique
```

#### Cas d'Erreur (Tribu Avec Patriarche)
```
Utilisateur: Paul
1. Clique sur "S'inscrire"
2. Sélectionne "Patriarche de Tribu"
3. Remplit les informations
4. Sélectionne "Tribu Alpha" (qui a déjà Jean comme patriarche)
5. Clique sur "S'inscrire"
6. ✗ Message d'erreur affichée:
   "La tribu 'Tribu Alpha' a déjà un patriarche: Jean Dupont.
    Une tribu ne peut avoir qu'un seul patriarche."
7. Formulaire reste affiché pour correction
```

### Scénario 2: Assignation via l'Interface Admin

#### Cas Nominal
```
Admin: Cherche dans Django Admin > User Profiles
1. Crée un nouveau profil utilisateur
2. Sélectionne le rôle "Patriarche de Tribu"
3. Sélectionne "Tribu Beta" (sans patriarche)
4. Clique "Enregistrer"
5. ✓ Profil créé avec succès
```

#### Cas d'Erreur
```
Admin: Cherche dans Django Admin > User Profiles
1. Crée un nouveau profil utilisateur
2. Sélectionne le rôle "Patriarche de Tribu"
3. Sélectionne "Tribu Alpha" (qui a déjà Jean)
4. Clique "Enregistrer"
5. ✗ Message d'erreur affichée dans l'interface admin
6. Formulaire reste actif pour correction
```

### Scénario 3: Remplacement d'un Responsable

Pour remplacer un responsable existant:

#### Méthode A: Via Admin
```
1. Accéder à Django Admin > User Profiles
2. Rechercher le profil actuel (ex: Adelphe)
3. Modifier le profil: 
   - Département: Sélectionner "---" pour le supprimer
   - Rôle: Changer vers "Pasteur" (par exemple)
4. Enregistrer
5. Créer un nouveau profil ou assigner le département à un autre utilisateur
```

#### Méthode B: Modification Directe
```
1. Accéder à Django Admin > User Profiles
2. Trouver l'utilisateur qui doit être responsable
3. Éditer le profil:
   - Rôle: Sélectionner "Responsable de Département"
   - Département: Sélectionner "Statistique"
   - Enregistrer
4. L'ancien responsable sera automatiquement remplacé (si changement)
```

## Cas Spéciaux

### Pasteur (Aucune Restriction)
Les pasteurs n'ont pas de restriction:
- Aucun rôle de tribu ou département
- Plusieurs pasteurs peuvent coexister
- Pas d'impact de l'unicité

```
Utilisateur: Tom
1. S'inscrit comme Pasteur
2. ✓ Succès (aucune tribu ou département)
```

### Changement de Tribu
Un patriarche peut changer de tribu assignée:

```
Utilisateur: Jean (patriarche de Tribu Alpha)
Admin veut l'assigner à Tribu Beta

1. Accéder à Django Admin > User Profiles
2. Éditer le profil de Jean
3. Changer Tribu: "Tribu Alpha" → "Tribu Beta"
4. Enregistrer
5. ✓ Jean est maintenant patriarche de Tribu Beta
6. Tribu Alpha n'a plus de patriarche (peut en recevoir un nouveau)
```

## Affichage Admin Amélioré

Le tableau de bord admin affiche clairement:

```
User Profiles:
┌─────────────────┬────────────────────────┬──────────────────────┐
│ Utilisateur     │ Rôle                   │ Affectation          │
├─────────────────┼────────────────────────┼──────────────────────┤
│ Jean Dupont     │ Patriarche de Tribu    │ Tribu: Tribu Alpha   │
│ Paul Leblanc    │ Responsable de Dept.   │ Dept: Statistique    │
│ Tom Martin      │ Pasteur                │ —                    │
│ Marie Durand    │ Patriarche de Tribu    │ Tribu: Tribu Beta    │
└─────────────────┴────────────────────────┴──────────────────────┘

Tribus:
┌────────────────┬──────────────────┐
│ Tribu          │ Patriarche       │
├────────────────┼──────────────────┤
│ Tribu Alpha    │ Jean Dupont      │
│ Tribu Beta     │ Marie Durand     │
│ Tribu Gamma    │ —                │
└────────────────┴──────────────────┘

Départements:
┌──────────────────┬──────────────────┐
│ Département      │ Responsable      │
├──────────────────┼──────────────────┤
│ Statistique      │ Paul Leblanc     │
│ Diaconie         │ —                │
│ Louange          │ —                │
└──────────────────┴──────────────────┘
```

## Gestion des Erreurs

### Message d'Erreur Patriarche
```
La tribu 'Tribu Alpha' a déjà un patriarche: Jean Dupont. 
Une tribu ne peut avoir qu'un seul patriarche.

Actions possibles:
1. Sélectionner une autre tribu sans patriarche
2. Demander à l'administrateur de libérer la tribu
3. Contacter Jean Dupont pour coordination
```

### Message d'Erreur Responsable
```
Le département 'Statistique' a déjà un responsable: Adelphe Martin. 
Un département ne peut avoir qu'un seul responsable.

Actions possibles:
1. Sélectionner un autre département sans responsable
2. Demander à l'administrateur de libérer le département
3. Contacter Adelphe Martin pour coordination
```

## FAQ

**Q: Comment savoir qui est responsable de quelle tribu/département?**
R: Consultez Django Admin > Tribus ou Django Admin > Départements. Chaque affiche son responsable actuel.

**Q: Je dois remplacer le patriarche d'une tribu. Comment faire?**
R: Via Django Admin > User Profiles:
   1. Éditer le profil actuel et supprimer la tribu (ou le rôle)
   2. Enregistrer
   3. Assigner la tribu à un nouveau patriarche

**Q: Puis-je avoir deux rôles (ex: patriarche ET responsable)?**
R: Non, chaque utilisateur a UN SEUL rôle dans la table UserProfile.

**Q: Que se passe-t-il si je supprime un utilisateur qui est responsable?**
R: La tribu/département devient orpheline (sans responsable). Vous pouvez en assigner un nouveau.

**Q: L'interface d'inscription est-elle modifiée?**
R: Non, l'interface reste la même, mais la validation empêche les doublons.

## Support

En cas de problème avec la validation:
1. Vérifier les messages d'erreur (qui indiquent le responsable actuel)
2. Contacter l'administrateur système
3. Consulter Django Admin > User Profiles pour voir l'état actuel
