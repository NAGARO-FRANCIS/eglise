# Implémentation: Unicité des Responsables par Tribu et Département

## Objectif
Implémenter une restriction garantissant qu'une tribu ne peut avoir qu'un seul patriarche et qu'un département ne peut avoir qu'un seul responsable.

Exemple: Adelphe est responsable du département de statistique, aucun autre utilisateur ne peut se connecter en tant que responsable de statistique.

## Modifications Apportées

### 1. Modèle `UserProfile` ([eglise/models.py](eglise/models.py))

#### Ajout de validations dans le modèle:
- Ajout de la méthode `clean()` qui vérifie:
  - Si le rôle est 'patriarche' avec une tribu définie: Vérifie qu'aucun autre utilisateur n'est patriarche de cette tribu
  - Si le rôle est 'responsable' avec un département défini: Vérifie qu'aucun autre utilisateur n'est responsable de ce département
  
- Ajout de la méthode `save()` qui appelle `full_clean()` avant la sauvegarde pour déclencher la validation

- Importation du module `ValidationError` de Django

#### Résultat:
- Les validations sont automatiquement exécutées lors de la création ou modification d'un `UserProfile`
- Une exception `ValidationError` est levée avec un message clair si la validation échoue

### 2. Formulaire `PatriarcheForm` ([eglise/forms.py](eglise/forms.py))

#### Ajout de validation personnalisée:
- Ajout de la méthode `clean()` qui vérifie:
  - Si une tribu est sélectionnée: Recherche un autre patriarche existant
  - Si un autre patriarche existe: Lève une exception `forms.ValidationError`
  
#### Résultat:
- La validation est exécutée lors de la soumission du formulaire d'inscription
- Un message d'erreur clair est affiché à l'utilisateur tentant de s'enregistrer comme patriarche d'une tribu déjà dirigée

### 3. Formulaire `ResponsableForm` ([eglise/forms.py](eglise/forms.py))

#### Ajout de validation personnalisée:
- Ajout de la méthode `clean()` qui vérifie:
  - Si un département est sélectionné: Recherche un autre responsable existant
  - Si un autre responsable existe: Lève une exception `forms.ValidationError`
  
#### Résultat:
- La validation est exécutée lors de la soumission du formulaire d'inscription
- Un message d'erreur clair est affiché à l'utilisateur tentant de s'enregistrer comme responsable d'un département déjà dirigé

### 4. Admin Django `UserProfileAdmin` ([eglise/admin.py](eglise/admin.py))

#### Ajout d'une interface d'administration pour `UserProfile`:
- Enregistrement de la classe `UserProfileAdmin` pour gérer les profils utilisateurs
- Affichage des informations importantes:
  - Nom d'utilisateur et rôle avec code couleur
  - Tribu ou département assigné
  - Date de création
  
#### Mise à jour des classes `TribuAdmin` et `DepartementAdmin`:
- Affichage du patriarche/responsable actuel pour chaque tribu/département
- Les validations du modèle s'appliquent automatiquement lors des modifications via l'admin

#### Résultat:
- Interface d'administration conviviale pour gérer les responsables
- Les validations empêchent l'assignation de multiples responsables via l'admin aussi
- Visibilité claire du responsable actuel pour chaque tribu/département

## Flux de Validation

```
Création/Modification UserProfile
    ↓
Appel de save()
    ↓
Appel de full_clean()
    ↓
Appel de clean()
    ↓
Vérification:
  - Si patriarche + tribu: existe-t-il un autre patriarche?
  - Si responsable + département: existe-t-il un autre responsable?
    ↓
Si validation OK: Sauvegarde
Si validation KO: ValidationError levée
```

## Endroits où la Validation s'Applique

### 1. **Inscription (SignUpView)**
   - Formulaire `PatriarcheForm` ou `ResponsableForm`
   - Appel de `form.is_valid()` exécute la validation

### 2. **Interface Admin Django**
   - Appel de `full_clean()` dans `UserProfile.save()`
   - Validation exécutée avant sauvegarde

### 3. **Code programmatique**
   - Tout code appelant `UserProfile.save()` ou `UserProfile.full_clean()`
   - La validation est toujours appliquée

## Messages d'Erreur Affichés

### Patriarche:
```
La tribu 'Nom Tribu' a déjà un patriarche: Jean Dupont. 
Une tribu ne peut avoir qu'un seul patriarche.
```

### Responsable:
```
Le département 'Nom Département' a déjà un responsable: Paul Leblanc. 
Un département ne peut avoir qu'un seul responsable.
```

## Tests Effectués

Tous les tests ont réussi ✓:
1. Création du premier patriarche pour une tribu: ✓ Succès
2. Tentative de créer un deuxième patriarche: ✓ Bloquée
3. Création du premier responsable pour un département: ✓ Succès
4. Tentative de créer un deuxième responsable: ✓ Bloquée
5. Modification d'un profil existant: ✓ Succès

## Considérations Futures

1. **Remplacement d'un responsable**: Permettre le remplacement d'un patriarche/responsable (avec confirmation)
2. **Audit**: Logger les changements de responsables pour la traçabilité
3. **Permissions**: Ajouter des permissions pour contrôler qui peut assigner des responsables
4. **Notification**: Notifier les utilisateurs affectés par les changements

## Notes pour le Déploiement

- Pas de migration de base de données requise
- Les modifications sont rétro-compatibles
- La validation s'applique immédiatement après le déploiement
