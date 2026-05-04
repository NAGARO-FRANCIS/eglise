from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Tribu, Departement, Membre, Presence, Culte


class LoginForm(forms.Form):
    """Formulaire de connexion"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom d\'utilisateur',
            'autofocus': 'autofocus'
        }),
        label="Nom d'utilisateur"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        }),
        label="Mot de passe"
    )


class CategorySelectForm(forms.Form):
    """Formulaire pour la sélection de catégorie"""
    CATEGORY_CHOICES = (
        ('patriarche', 'Patriarche de Tribu'),
        ('responsable', 'Responsable de Département'),
    )
    
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.RadioSelect(),
        label="Choisissez votre catégorie",
        required=True
    )


class SignUpForm(forms.ModelForm):
    """Formulaire d'inscription avec détails en fonction de la catégorie"""
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Mot de passe'
    }))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirmer le mot de passe'
    }))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom d\'utilisateur'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adresse email'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prénom'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password != password_confirm:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        
        if len(password) < 8:
            raise forms.ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        
        return cleaned_data


class PatriarcheForm(forms.ModelForm):
    """Formulaire pour compléter le profil d'un patriarche de tribu"""
    tribu = forms.ModelChoiceField(
        queryset=Tribu.objects.all(),
        label="Quelle tribu dirigez-vous?",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    class Meta:
        model = UserProfile
        fields = ['tribu', 'photo']
        widgets = {
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'photo': 'Votre photo (optionnel)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.role = 'patriarche'
    
    def clean(self):
        """Validation pour s'assurer qu'une tribu n'a qu'un seul patriarche"""
        cleaned_data = super().clean()
        tribu = cleaned_data.get('tribu')
        
        if tribu:
            # Chercher un autre patriarche pour la même tribu
            existing = UserProfile.objects.filter(
                role='patriarche',
                tribu=tribu
            ).exclude(pk=self.instance.pk)
            
            if existing.exists():
                existing_user = existing.first().user.get_full_name() or existing.first().user.username
                raise forms.ValidationError(
                    f"La tribu '{tribu.nom}' a déjà un patriarche: {existing_user}. "
                    f"Une tribu ne peut avoir qu'un seul patriarche."
                )
        
        return cleaned_data


class ResponsableForm(forms.ModelForm):
    """Formulaire pour compléter le profil d'un responsable de département"""
    departement = forms.ModelChoiceField(
        queryset=Departement.objects.all(),
        label="Quel département dirigez-vous?",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    photo = forms.ImageField(
        label="Votre photo (optionnel)",
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        help_text="Format: JPG, PNG. Taille max: 5MB"
    )
    
    class Meta:
        model = UserProfile
        fields = ['departement']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.role = 'responsable'
    
    def clean(self):
        """Validation pour s'assurer qu'un département n'a qu'un seul responsable"""
        cleaned_data = super().clean()
        departement = cleaned_data.get('departement')
        
        if departement:
            # Chercher un autre responsable pour le même département
            existing = UserProfile.objects.filter(
                role='responsable',
                departement=departement
            ).exclude(pk=self.instance.pk)
            
            if existing.exists():
                existing_user = existing.first().user.get_full_name() or existing.first().user.username
                raise forms.ValidationError(
                    f"Le département '{departement.nom}' a déjà un responsable: {existing_user}. "
                    f"Un département ne peut avoir qu'un seul responsable."
                )
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=commit)
        # La photo est stockée dans UserProfile
        if self.files.get('photo'):
            # Créer ou mettre à jour une image de profil associée
            pass
        return instance


class PasteurForm(forms.ModelForm):
    """Formulaire pour compléter le profil d'un pasteur"""
    
    class Meta:
        model = UserProfile
        fields = []
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.role = 'pasteur'


class MembreForm(forms.ModelForm):
    """Formulaire pour ajouter ou modifier un membre"""
    
    class Meta:
        model = Membre
        fields = ['nom', 'prenom', 'email', 'telephone', 'adresse', 'genre', 'date_naissance', 'tribu', 'departement', 'statut', 'photo']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom',
                'required': True
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prénom',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Téléphone'
            }),
            'adresse': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adresse'
            }),
            'genre': forms.Select(attrs={
                'class': 'form-control'
            }),
            'date_naissance': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'tribu': forms.Select(attrs={
                'class': 'form-control'
            }),
            'departement': forms.Select(attrs={
                'class': 'form-control'
            }),
            'statut': forms.Select(attrs={
                'class': 'form-control'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }


class PresenceForm(forms.ModelForm):
    """Formulaire pour enregistrer la présence"""
    
    class Meta:
        model = Presence
        fields = ['present']
        widgets = {
            'present': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class PresenceMembreSelectionForm(forms.Form):
    """Formulaire pour sélectionner des membres et les ajouter à un culte"""
    membres = forms.ModelMultipleChoiceField(
        queryset=Membre.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="Sélectionnez les membres à ajouter"
    )


class CulteForm(forms.ModelForm):
    """Formulaire pour créer ou modifier un culte"""
    
    class Meta:
        model = Culte
        fields = ['date', 'type_culte', 'theme', 'predicateur', 'nombre_participants', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'type_culte': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'theme': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Thème du culte (optionnel)'
            }),
            'predicateur': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prédicateur (optionnel)'
            }),
            'nombre_participants': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de personnes présentes',
                'min': '0',
                'required': True
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Notes (optionnel)',
                'rows': 3
            }),
        }
        labels = {
            'date': 'Date du culte *',
            'type_culte': 'Type de culte *',
            'theme': 'Thème',
            'predicateur': 'Prédicateur',
            'nombre_participants': 'Nombre de personnes présentes *',
            'notes': 'Notes',
        }


class ParticipationDimanchemForm(forms.ModelForm):
    """Formulaire simplifié pour ajouter rapidement la participation au dimanche"""
    
    class Meta:
        model = Culte
        fields = ['date', 'nombre_participants', 'nombre_nouveaux']
        widgets = {
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'nombre_participants': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 5000',
                'min': '0',
                'required': True
            }),
            'nombre_nouveaux': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 50',
                'min': '0',
                'required': True
            }),
        }
        labels = {
            'date': 'Date du dimanche *',
            'nombre_participants': 'Nombre de participants *',
            'nombre_nouveaux': 'Nombre de nouveaux *',
        }
