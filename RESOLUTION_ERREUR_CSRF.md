# Résolution de l'Erreur CSRF (403 Forbidden)

## 🔍 Diagnostic

L'erreur CSRF que vous rencontrez est probablement due à l'une des causes suivantes:

### 1. **Cache du navigateur obsolète**
Le navigateur a en cache une version ancienne du formulaire ou du token CSRF.

**Solution**: 
- Vider le cache du navigateur (Ctrl+Shift+Delete ou Cmd+Shift+Delete)
- Ou accéder à la page en mode navigation privée/incognito
- Ou utiliser une nouvelle session du navigateur

### 2. **Redirection après Login**
Après connexion, Django régénère le token CSRF. Si vous êtes redirigé d'une page à l'autre avant soumission, le token peut être invalidé.

**Solution**:
- Actualiser la page après connexion avant de soumettre un formulaire
- Les templates sont correctement configurés avec `{% csrf_token %}`

### 3. **Cookies désactivés**
Django a besoin des cookies pour stocker le token CSRF.

**Solution**:
- Vérifier que les cookies sont activés dans votre navigateur
- Vérifier que le site n'est pas bloqué pour les cookies

### 4. **Configuration ALLOWED_HOSTS**
Si vous accédez au site avec un domaine différent (ex: localhost vs 127.0.0.1).

**Solution**: Voir la section de configuration ci-dessous.

---

## ✅ Vérification de la Configuration

### Settings.py - Middleware
Votre fichier `CCR/settings.py` contient:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # ✅ Présent
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```
✅ **Status**: Correctement configuré

### Settings.py - Context Processors
Votre fichier `CCR/settings.py` contient:
```python
'context_processors': [
    'django.template.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
]
```
✅ **Status**: Correctement configuré (Django inclut automatiquement le CSRF processor)

### Templates - Tokens CSRF
Vérification de tous les formulaires POST:
- ✅ signup.html: Token CSRF présent (ligne 266)
- ✅ login.html: Token CSRF présent (ligne 313)
- ✅ role_completion.html: Token CSRF présent (ligne 276)
- ✅ category_select.html: Token CSRF présent (ligne 150)
- ✅ culte_form.html: Token CSRF présent (ligne 12)
- ✅ culte_presence.html: Token CSRF présent (ligne 43 et 89)
- ✅ culte_list.html: Token CSRF présent (ligne 69)
- ✅ culte_participation_add.html: Token CSRF présent (ligne 13)
- ✅ departement_membres.html: Token CSRF présent (ligne 33)
- ✅ Requêtes AJAX: Token CSRF présent (membre_list.html ligne 548)

**Status**: ✅ **Tous les formulaires sont correctement configurés**

---

## 🛠️ Solutions Recommandées

### Solution 1: Vider le Cache (Recommandée d'abord)
1. Ouvrir DevTools (F12)
2. Aller à Application > Cookies
3. Supprimer tous les cookies pour votre domaine
4. Actualiser la page (Ctrl+F5 ou Cmd+Shift+R)
5. Réessayer le formulaire

### Solution 2: Mode Incognito
1. Ouvrir une nouvelle fenêtre en mode navigation privée
2. Aller sur votre site
3. Réessayer le formulaire
4. Si cela fonctionne, le problème était le cache

### Solution 3: Vérifier ALLOWED_HOSTS
Si votre site est accessible via plusieurs domaines, éditer `CCR/settings.py`:

```python
# Avant
ALLOWED_HOSTS = ['*']

# Après (si vous avez des domaines spécifiques)
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'example.com']
```

### Solution 4: Désactiver DEBUG temporairement
Pour vérifier que ce n'est pas un problème de test:

```python
# Dans CCR/settings.py
DEBUG = False  # Temporairement pour tester
```

Redémarrer le serveur Django et réessayer.

---

## 📊 Checklist de Diagnostic

Avant de contacter le support, vérifier:

- [ ] Cookies activés dans le navigateur
- [ ] Cache du navigateur vidé
- [ ] Pas de blocage du site par un add-on
- [ ] Domaine/URL correcte (pas de mélange localhost/127.0.0.1)
- [ ] JavaScript activé (pour les formulaires AJAX)
- [ ] Serveur Django en cours d'exécution
- [ ] Pas de modification manuelle du formulaire HTML
- [ ] Pas d'utilisation de proxy/VPN qui pourrait affecter les cookies

---

## 🔐 Notes de Sécurité CSRF

### Pourquoi CSRF?
CSRF protège contre les attaques de falsification de requête intersite (Cross-Site Request Forgery).

### Quand le Token se Régénère?
- Après login d'un utilisateur
- Après logout
- Après certaines actions sensibles (changement de mot de passe, etc.)

### Bonnes Pratiques
- ✅ Toujours inclure `{% csrf_token %}` dans les formulaires POST
- ✅ Inclure le token dans les en-têtes AJAX: `'X-CSRFToken': '{{ csrf_token }}'`
- ✅ Ne pas désactiver `CsrfViewMiddleware` en production
- ✅ Actualiser la page après une redirection avant de soumettre

---

## 📝 Exemple de Formulaire Correct

```html
<!-- ✅ CORRECT -->
<form method="post">
    {% csrf_token %}
    <input type="text" name="username">
    <button type="submit">Soumettre</button>
</form>

<!-- ❌ INCORRECT (pas de token CSRF) -->
<form method="post">
    <input type="text" name="username">
    <button type="submit">Soumettre</button>
</form>
```

---

## 📞 Vous Avez Toujours le Problème?

Si l'erreur persiste après avoir essayé les solutions:

1. **Capturer les logs Django**: Vérifier les logs du serveur pour voir le message d'erreur complet
2. **Vérifier les headers HTTP**: Utiliser DevTools (Network tab) pour voir si le token CSRF est envoyé
3. **Tester avec curl**: 
   ```bash
   curl -X POST http://localhost:8000/votre-url/ \
        -H "X-CSRFToken: votre_token" \
        -d "data=value"
   ```

---

## ✨ Résumé

Votre configuration CSRF est correcte à 100%:
- ✅ Middleware activé
- ✅ Tous les templates configurés
- ✅ Contexte CSRF correct

L'erreur est généralement due au **cache du navigateur** ou aux **cookies de session**.

**Action recommandée**: Vider le cache et les cookies, puis réessayer.
