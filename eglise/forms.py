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
        fields = ['tribu']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.role = 'patriarche'


class ResponsableForm(forms.ModelForm):
    """Formulaire pour compléter le profil d'un responsable de département"""
    departement = forms.ModelChoiceField(
        queryset=Departement.objects.all(),
        label="Quel département dirigez-vous?",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    class Meta:
        model = UserProfile
        fields = ['departement']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.role = 'responsable'


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
        fields = ['nom', 'prenom', 'email', 'telephone', 'adresse', 'genre', 'date_naissance', 'tribu', 'departement', 'statut']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom'
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prénom'
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
