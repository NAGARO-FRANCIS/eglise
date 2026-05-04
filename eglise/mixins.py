"""Mixins pour contrôler l'accès aux données selon le rôle de l'utilisateur"""
from django.shortcuts import redirect
from django.views.generic.base import ContextMixin
from django.db.models import Count, Q
from .models import Membre, UserProfile, Tribu, Departement, Culte, Presence
from django.utils import timezone
from datetime import timedelta


class RoleRequiredMixin:
    """Mixin pour vérifier que l'utilisateur a un rôle spécifique"""
    required_roles = []
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('eglise:login')
        
        # Les administrateurs et pasteurs ont accès à tout
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        
        try:
            profile = request.user.profile
            if profile.role == 'pasteur' or profile.role not in self.required_roles:
                return super().dispatch(request, *args, **kwargs) if profile.role == 'pasteur' else redirect('eglise:dashboard')
        except UserProfile.DoesNotExist:
            return redirect('eglise:dashboard')
        
        return super().dispatch(request, *args, **kwargs)


class DataFilteringMixin(ContextMixin):
    """Mixin pour filtrer les données selon le rôle de l'utilisateur"""
    
    def get_filtered_queryset(self, queryset):
        """Filtre le queryset selon le rôle de l'utilisateur"""
        user = self.request.user
        
        # Les administrateurs et pasteurs voient tout
        if user.is_superuser:
            return queryset
        
        try:
            profile = user.profile
            
            if profile.role == 'pasteur':
                # Pasteur voit tout
                return queryset
            
            elif profile.role == 'patriarche':
                # Patriarche voit seulement les membres de sa tribu
                return queryset.filter(tribu=profile.tribu)
            
            elif profile.role == 'responsable':
                # Responsable voit seulement les membres de son département
                return queryset.filter(departement=profile.departement)
            
            # Par défaut, pas d'accès
            return queryset.none()
        
        except UserProfile.DoesNotExist:
            return queryset.none()
    
    def get_user_tribu(self):
        """Retourne la tribu de l'utilisateur s'il est patriarche"""
        try:
            profile = self.request.user.profile
            if profile.role == 'patriarche':
                return profile.tribu
        except UserProfile.DoesNotExist:
            pass
        return None
    
    def get_user_departement(self):
        """Retourne le département de l'utilisateur s'il est responsable"""
        try:
            profile = self.request.user.profile
            if profile.role == 'responsable':
                return profile.departement
        except UserProfile.DoesNotExist:
            pass
        return None
    
    def get_filtered_tribus(self):
        """Retourne les tribus accessibles par l'utilisateur"""
        user = self.request.user
        
        # Les administrateurs et pasteurs voient tout
        if user.is_superuser:
            return Tribu.objects.all()
        
        try:
            profile = user.profile
            if profile.role == 'pasteur':
                # Pasteur voit toutes les tribus
                return Tribu.objects.all()
            elif profile.role == 'patriarche':
                # Patriarche voit uniquement sa tribu
                return Tribu.objects.filter(id=profile.tribu.id) if profile.tribu else Tribu.objects.none()
            # Responsable voit toutes les tribus
            return Tribu.objects.all()
        except UserProfile.DoesNotExist:
            return Tribu.objects.none()
    
    def get_filtered_departements(self):
        """Retourne les départements accessibles par l'utilisateur"""
        user = self.request.user
        
        # Les administrateurs et pasteurs voient tout
        if user.is_superuser:
            return Departement.objects.all()
        
        try:
            profile = user.profile
            if profile.role == 'pasteur':
                # Pasteur voit tous les départements
                return Departement.objects.all()
            elif profile.role == 'responsable':
                # Responsable voit uniquement son département
                return Departement.objects.filter(id=profile.departement.id) if profile.departement else Departement.objects.none()
            # Patriarche voit tous les départements
            return Departement.objects.all()
        except UserProfile.DoesNotExist:
            return Departement.objects.none()
    
    def get_filtered_cultes(self):
        """Retourne les cultes accessibles par l'utilisateur"""
        user = self.request.user
        cultes = Culte.objects.all()
        
        # Tous les rôles voient tous les cultes (cultes globaux)
        # Mais la participation est filtrée selon les membres accessibles
        return cultes
    
    def get_user_context(self):
        """Retourne le contexte utilisateur avec ses informations d'accès"""
        context = {}
        user = self.request.user
        
        # Vérifier si c'est un administrateur
        if user.is_superuser:
            context['user_role'] = 'administrateur'
            context['is_admin'] = True
            return context
        
        try:
            profile = user.profile
            context['user_role'] = profile.role
            context['user_tribu'] = profile.tribu if profile.role == 'patriarche' else None
            context['user_departement'] = profile.departement if profile.role == 'responsable' else None
            context['is_admin'] = False
        except UserProfile.DoesNotExist:
            context['user_role'] = None
            context['is_admin'] = False
        
        return context


class ProtectedDataAccessMixin(DataFilteringMixin, RoleRequiredMixin):
    """Mixin combinant la vérification de rôle et le filtrage de données"""
    required_roles = ['pasteur', 'patriarche', 'responsable']
    
    def get_filtered_statistiques(self):
        """Retourne les statistiques filtrées selon le rôle"""
        membres_queryset = Membre.objects.all()
        membres_filtered = self.get_filtered_queryset(membres_queryset)
        
        # Pour l'admin (Nagaro): compter SEULEMENT les membres ayant une tribu
        user = self.request.user
        if user.is_superuser:
            membres_filtered = membres_filtered.filter(tribu__isnull=False)
        
        stats = {
            'total_membres': membres_filtered.count(),
            'membres_actifs': membres_filtered.filter(statut='actif').count(),
            'membres_nouveau': membres_filtered.filter(statut='nouveau').count(),
            'membres_sorti': membres_filtered.filter(statut='sorti').count(),
        }
        
        # Calcul du taux de participation moyen
        trois_mois_ago = timezone.now().date() - timedelta(days=90)
        presences_count = Presence.objects.filter(
            culte__date__gte=trois_mois_ago,
            present=True,
            membre__in=membres_filtered
        ).count()
        
        cultes_count = Culte.objects.filter(date__gte=trois_mois_ago).count()
        
        if cultes_count > 0 and stats['membres_actifs'] > 0:
            stats['taux_participation_moyen'] = round(
                (presences_count / (cultes_count * stats['membres_actifs'])) * 100, 1
            )
        else:
            stats['taux_participation_moyen'] = 0
        
        return stats
