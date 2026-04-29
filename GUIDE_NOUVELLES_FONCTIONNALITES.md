## 🎯 Guide d'Utilisation - Gestion des Membres et Présence

### ✨ Nouvelles Fonctionnalités Implémentées

Cette mise à jour ajoute 3 nouvelles pages de gestion :

#### 1. **Gestion des Membres par Tribu** 
- **Accès**: Cliquer sur une tribu dans le tableau de bord → "Membres par Tribu"
- **URL**: `/tribu/<id>/membres/`
- **Qui peut accéder**: 
  - Administrateurs
  - Patriarches de la tribu

**Fonctionnalités**:
- 📋 Voir tous les membres d'une tribu
- ➕ Ajouter rapidement un nouveau membre
- Affichage du statut (Nouveau, Actif, Inactif, Sorti)

#### 2. **Gestion des Membres par Département**
- **Accès**: Cliquer sur un département dans le tableau de bord → "Membres par Département"
- **URL**: `/departement/<id>/membres/`
- **Qui peut accéder**:
  - Administrateurs
  - Responsables du département

**Fonctionnalités**:
- 📋 Voir tous les membres d'un département
- ➕ Ajouter rapidement un nouveau membre
- Affichage du statut (Nouveau, Actif, Inactif, Sorti)

#### 3. **Liste de Présence par Culte**
- **Accès**: Cliquer sur "Gérer présence" dans les cultes récents du tableau de bord
- **URL**: `/culte/<id>/presence/`
- **Qui peut accéder**: Tous les utilisateurs authentifiés

**Fonctionnalités**:
- 📋 Voir la liste de présence du culte
- ➕ Ajouter des membres à la présence (en masse)
- ✓/✗ Basculer le statut de chaque présence (Présent ↔ Absent)
- 📊 Statistiques de présence en temps réel

---

### 🚀 Installation et Démarrage

#### 1. Appliquer les migrations
```bash
python manage.py migrate
```

#### 2. Créer les données de test (optionnel)
```bash
python create_admin.py
python create_test_data.py
```

Cela crée:
- **Admin**: `admin` / `admin123`
- **Pasteur**: `pasteur` / `pasteur123`
- 6 tribus
- 5 départements
- 10 cultes récents
- 20 membres de test

#### 3. Lancer le serveur
```bash
python manage.py runserver
```

#### 4. Accéder à l'application
- Ouvrir: http://localhost:8000
- Se connecter avec les identifiants créés

---

### 📝 Formulaire d'Ajout de Membre

Quand vous ajoutez un membre à une tribu ou département, les champs suivants sont disponibles:

- **Prénom** * (requis)
- **Nom** * (requis)
- **Email** (optionnel)
- **Téléphone** (optionnel)
- **Adresse** (optionnel)
- **Genre** (Masculin/Féminin)
- **Date de naissance** (optionnel)
- **Statut** (Nouveau, Actif, Inactif, Sorti)

\* = champ obligatoire

---

### 🎨 Navigation Améliorée

Le tableau de bord a été amélioré:

1. **Tribus et Départements**: Maintenant cliquables pour accéder directement à la page de gestion des membres
2. **Cultes Récents**: Nouveau bouton "Gérer présence" pour accéder rapidement à la liste de présence

---

### 🔒 Contrôle d'Accès

L'application respecte les rôles utilisateurs:

- **Administrateur/Pasteur**: Accès complet à toutes les données
- **Patriarche de Tribu**: Peut gérer sa tribu uniquement
- **Responsable de Département**: Peut gérer son département uniquement
- **Utilisateur normal**: Peut consulter et gérer les présences aux cultes

---

### 📱 Responsive Design

Toutes les pages sont responsive et s'adaptent aux appareils mobiles.

---

### ❓ Dépannage

**Je ne vois rien à l'écran**:
1. Vérifiez que vous êtes connecté (rechargez la page)
2. Vérifiez que des tribus/départements existent (créez-les via l'admin si nécessaire)
3. Consultez les logs Django pour les erreurs

**Impossible d'ajouter des membres**:
1. Vérifiez que vous avez les permissions (Admin, Patriarche ou Responsable)
2. Vérifiez que la tribu/département existe

**Présence non mise à jour**:
1. Rechargez la page après une action
2. Vérifiez que le culte existe

---

Pour toute question, consultez le code source ou les fichiers de configuration Django.
