from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Profil utilisateur avec rôles"""
    ROLE_CHOICES = (
        ('pasteur', 'Pasteur'),
        ('patriarche', 'Patriarche de Tribu'),
        ('responsable', 'Responsable de Département'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    # Pour les patriarches de tribu
    tribu = models.ForeignKey('Tribu', on_delete=models.SET_NULL, null=True, blank=True, related_name='patriarches')
    
    # Pour les responsables de département
    departement = models.ForeignKey('Departement', on_delete=models.SET_NULL, null=True, blank=True, related_name='responsables')
    
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Profils Utilisateurs"
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
    
    def est_pasteur(self):
        return self.role == 'pasteur'
    
    def est_patriarche(self):
        return self.role == 'patriarche'
    
    def est_responsable(self):
        return self.role == 'responsable'


class Tribu(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Tribus"
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def nombre_membres(self):
        return self.membre_set.filter(statut='actif').count()


class Departement(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    responsable = models.CharField(max_length=100, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def nombre_membres(self):
        return self.membre_set.filter(statut='actif').count()


class Membre(models.Model):
    STATUT_CHOICES = (
        ('nouveau', 'Nouveau'),
        ('actif', 'Actif'),
        ('sorti', 'Sorti'),
        ('inactif', 'Inactif'),
    )
    
    GENRE_CHOICES = (
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    )

    # Informations personnelles
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES, blank=True)
    date_naissance = models.DateField(blank=True, null=True)
    
    # Informations d'église
    tribu = models.ForeignKey(Tribu, on_delete=models.SET_NULL, null=True)
    departement = models.ForeignKey(Departement, on_delete=models.SET_NULL, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='nouveau')
    date_adhesion = models.DateField(default=timezone.now)
    date_depart = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def nom_complet(self):
        return f"{self.prenom} {self.nom}"

    def taux_participation(self):
        """Calcule le taux de participation au cours des 3 derniers mois"""
        trois_mois_ago = timezone.now().date() - timedelta(days=90)
        cultes_total = Culte.objects.filter(date__gte=trois_mois_ago).count()
        if cultes_total == 0:
            return 0
        presences = Presence.objects.filter(
            membre=self,
            culte__date__gte=trois_mois_ago,
            present=True
        ).count()
        return round((presences / cultes_total) * 100, 1)


class Culte(models.Model):
    TYPE_CULTE_CHOICES = (
        ('dimanche', 'Dimanche'),
        ('mercredi', 'Mercredi'),
        ('special', 'Spécial'),
        ('autre', 'Autre'),
    )

    date = models.DateField()
    type_culte = models.CharField(max_length=20, choices=TYPE_CULTE_CHOICES, default='dimanche')
    theme = models.CharField(max_length=255, blank=True, null=True)
    predicateur = models.CharField(max_length=100, blank=True, null=True)
    nombre_participants = models.IntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Culte du {self.date} - {self.get_type_culte_display()}"

    def mettre_a_jour_nombre_participants(self):
        """Met à jour le nombre de participants"""
        count = self.presence_set.filter(present=True).count()
        self.nombre_participants = count
        self.save()


class Presence(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    culte = models.ForeignKey(Culte, on_delete=models.CASCADE)
    present = models.BooleanField(default=True)
    date_enregistrement = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('membre', 'culte')
        ordering = ['-culte__date']

    def __str__(self):
        statut = "Présent" if self.present else "Absent"
        return f"{self.membre} - {self.culte.date} ({statut})"


class Statistique(models.Model):
    """Modèle pour stocker les statistiques périodiques"""
    date = models.DateField(auto_now_add=True)
    nombre_total_membres = models.IntegerField()
    nombre_membres_actifs = models.IntegerField()
    nombre_membres_nouveau = models.IntegerField()
    nombre_membres_sorti = models.IntegerField()
    taux_participation_moyen = models.FloatField()
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Statistiques"

    def __str__(self):
        return f"Statistiques du {self.date}"
