from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


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
    
    # Photo de profil
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    
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
    
    def clean(self):
        """Validation pour s'assurer qu'une tribu/département n'a qu'un seul responsable"""
        # Vérifier l'unicité du patriarche pour une tribu
        if self.role == 'patriarche' and self.tribu:
            # Chercher un autre patriarche pour la même tribu
            existing = UserProfile.objects.filter(
                role='patriarche',
                tribu=self.tribu
            ).exclude(pk=self.pk)  # Exclure le profil actuel (pour les mises à jour)
            
            if existing.exists():
                existing_user = existing.first().user.get_full_name() or existing.first().user.username
                raise ValidationError(
                    f"La tribu '{self.tribu.nom}' a déjà un patriarche: {existing_user}. "
                    f"Une tribu ne peut avoir qu'un seul patriarche."
                )
        
        # Vérifier l'unicité du responsable pour un département
        if self.role == 'responsable' and self.departement:
            # Chercher un autre responsable pour le même département
            existing = UserProfile.objects.filter(
                role='responsable',
                departement=self.departement
            ).exclude(pk=self.pk)  # Exclure le profil actuel (pour les mises à jour)
            
            if existing.exists():
                existing_user = existing.first().user.get_full_name() or existing.first().user.username
                raise ValidationError(
                    f"Le département '{self.departement.nom}' a déjà un responsable: {existing_user}. "
                    f"Un département ne peut avoir qu'un seul responsable."
                )
    
    def save(self, *args, **kwargs):
        """Appel de la validation avant la sauvegarde"""
        self.full_clean()
        super().save(*args, **kwargs)


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
    photo = models.ImageField(upload_to='membres_photos/', blank=True, null=True)
    
    # Informations d'église
    tribu = models.ForeignKey(Tribu, on_delete=models.SET_NULL, null=True, blank=True)
    departement = models.ForeignKey(Departement, on_delete=models.SET_NULL, null=True, blank=True)
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
    
    SCOPE_CHOICES = (
        ('global', 'Global'),
        ('tribu', 'Tribu'),
        ('departement', 'Département'),
    )

    date = models.DateField()
    type_culte = models.CharField(max_length=20, choices=TYPE_CULTE_CHOICES, default='dimanche')
    theme = models.CharField(max_length=255, blank=True, null=True)
    predicateur = models.CharField(max_length=100, blank=True, null=True)
    nombre_participants = models.IntegerField(default=0)
    nombre_nouveaux = models.IntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    # Champs pour distinguer les cultes locaux des cultes globaux
    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES, default='global', help_text='Global ou local à une structure')
    tribu = models.ForeignKey('Tribu', on_delete=models.SET_NULL, null=True, blank=True, related_name='cultes_locaux', help_text='Tribu si culte local')
    departement = models.ForeignKey('Departement', on_delete=models.SET_NULL, null=True, blank=True, related_name='cultes_locaux', help_text='Département si culte local')

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


class RapportMensuel(models.Model):
    """Rapport mensuel détaillé"""
    STATUS_CHOICES = (
        ('brouillon', 'Brouillon'),
        ('valide', 'Validé'),
        ('archive', 'Archivé'),
    )
    
    # Identification du rapport
    mois = models.IntegerField(choices=[(i, f"Mois {i}") for i in range(1, 13)])
    annee = models.IntegerField()
    
    # Structure (optionnel - si null: rapport global)
    tribu = models.ForeignKey(Tribu, on_delete=models.CASCADE, null=True, blank=True, related_name='rapports_mensuels')
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, null=True, blank=True, related_name='rapports_mensuels')
    
    # Données générales
    nombre_total_membres = models.IntegerField(default=0)
    nombre_membres_actifs = models.IntegerField(default=0)
    nombre_membres_nouveau = models.IntegerField(default=0)
    nombre_membres_inactif = models.IntegerField(default=0)
    nombre_membres_sorti = models.IntegerField(default=0)
    
    # Données par tribu
    nombre_tribus = models.IntegerField(default=0)
    membres_par_tribu = models.JSONField(default=dict, blank=True)
    
    # Données par département
    nombre_departements = models.IntegerField(default=0)
    membres_par_departement = models.JSONField(default=dict, blank=True)
    
    # Statistiques d'assistance
    nombre_cultes = models.IntegerField(default=0)
    nombre_total_presences = models.IntegerField(default=0)
    nombre_total_absences = models.IntegerField(default=0)
    taux_participation_moyen = models.FloatField(default=0.0)
    
    # Données par type de culte
    cultes_par_type = models.JSONField(default=dict, blank=True)
    
    # Notes et observations
    notes = models.TextField(blank=True, null=True)
    observations = models.TextField(blank=True, null=True)
    
    # Gestion du rapport
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='brouillon')
    auteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rapports_mensuels')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    date_validation = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-annee', '-mois']
        unique_together = [('mois', 'annee', 'tribu', 'departement')]
        verbose_name_plural = "Rapports Mensuels"
    
    def __str__(self):
        mois_names = {
            1: 'Janvier', 2: 'Février', 3: 'Mars', 4: 'Avril',
            5: 'Mai', 6: 'Juin', 7: 'Juillet', 8: 'Août',
            9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Décembre'
        }
        return f"Rapport {mois_names.get(self.mois, 'N/A')} {self.annee}"
    
    @property
    def periode_str(self):
        """Retourne la période en format lisible"""
        mois_names = {
            1: 'Janvier', 2: 'Février', 3: 'Mars', 4: 'Avril',
            5: 'Mai', 6: 'Juin', 7: 'Juillet', 8: 'Août',
            9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Décembre'
        }
        return f"{mois_names.get(self.mois, 'N/A')} {self.annee}"


class RapportHebdomadaire(models.Model):
    """Rapport hebdomadaire pour l'évolution du culte et les tribus."""
    TYPE_CHOICES = (
        ('evolution_culte', 'Évolution du culte'),
        ('tribu', 'Rapport par tribu'),
    )

    date_debut = models.DateField()
    date_fin = models.DateField()
    type_rapport = models.CharField(max_length=30, choices=TYPE_CHOICES)
    tribu = models.ForeignKey(Tribu, on_delete=models.CASCADE, null=True, blank=True, related_name='rapports_hebdomadaires')

    total_participants = models.IntegerField(default=0)
    total_nouveaux = models.IntegerField(default=0)
    nombre_cultes = models.IntegerField(default=0)
    nombre_tribus = models.IntegerField(default=0)
    details = models.JSONField(default=dict, blank=True)

    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_fin', 'type_rapport']
        unique_together = [('date_debut', 'date_fin', 'type_rapport', 'tribu')]
        verbose_name_plural = 'Rapports Hebdomadaires'

    def __str__(self):
        if self.type_rapport == 'tribu' and self.tribu:
            return f"Rapport hebdo {self.tribu.nom} ({self.date_debut} -> {self.date_fin})"
        return f"Rapport hebdo {self.get_type_rapport_display()} ({self.date_debut} -> {self.date_fin})"
