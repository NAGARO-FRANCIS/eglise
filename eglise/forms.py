from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Tribu, Departement


class SignUpForm(forms.ModelForm):
    """Formulaire d'inscription initial"""
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Mot de passe'
    }))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirmer le mot de passe'
    }))
    
    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        widget=forms.RadioSelect(),
        label="Rôle dans l'église"
    )
    
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
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = UserProfile
        fields = []
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.role = 'patriarche'


class ResponsableForm(forms.ModelForm):
    """Formulaire pour compléter le profil d'un responsable de département"""
    departement = forms.ModelChoiceField(
        queryset=Departement.objects.all(),
        label="Quel département dirigez-vous?",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = UserProfile
        fields = []
    
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
