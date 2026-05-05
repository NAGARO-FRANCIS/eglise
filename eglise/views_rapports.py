# Vues pour les rapports mensuels
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
import json
from .models import RapportMensuel, UserProfile
from .mixins import ProtectedDataAccessMixin


class RapportMensuelListView(ProtectedDataAccessMixin, ListView):
    """Liste des rapports mensuels - Filtrée selon le rôle"""
    model = RapportMensuel
    template_name = 'eglise/rapport_mensuel_list.html'
    context_object_name = 'rapports'
    paginate_by = 12
    
    def get_queryset(self):
        """Retourner les rapports filtrés selon le rôle de l'utilisateur"""
        user = self.request.user
        
        # Les admins et superusers voient tous les rapports
        if user.is_superuser:
            return RapportMensuel.objects.all().order_by('-annee', '-mois')
        
        # Les pasteurs voient tous les rapports
        if hasattr(user, 'profile') and user.profile.role == 'pasteur':
            return RapportMensuel.objects.all().order_by('-annee', '-mois')
        
        # Les patriarches ne voient que les rapports de leur tribu
        if hasattr(user, 'profile') and user.profile.role == 'patriarche' and user.profile.tribu:
            return RapportMensuel.objects.filter(
                tribu=user.profile.tribu
            ).order_by('-annee', '-mois')
        
        # Les responsables ne voient que les rapports de leur département
        if hasattr(user, 'profile') and user.profile.role == 'responsable' and user.profile.departement:
            return RapportMensuel.objects.filter(
                departement=user.profile.departement
            ).order_by('-annee', '-mois')
        
        # Les autres utilisateurs ne voient rien
        return RapportMensuel.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        context['page_title'] = 'Rapports Mensuels'
        
        # Ajouter les stats générales
        context['nombre_rapports'] = self.get_queryset().count()
        context['rapports_valides'] = self.get_queryset().filter(statut='valide').count()
        
        # Ajouter un message selon le rôle
        user = self.request.user
        if hasattr(user, 'profile'):
            if user.profile.role == 'patriarche' and user.profile.tribu:
                context['role_message'] = f"Vous visualisez les rapports de la tribu: {user.profile.tribu.nom}"
            elif user.profile.role == 'responsable' and user.profile.departement:
                context['role_message'] = f"Vous visualisez les rapports du département: {user.profile.departement.nom}"
        
        return context


class RapportMensuelDetailView(ProtectedDataAccessMixin, DetailView):
    """Détail d'un rapport mensuel - Avec vérification d'accès"""
    model = RapportMensuel
    template_name = 'eglise/rapport_mensuel_detail.html'
    context_object_name = 'rapport'
    
    def get_object(self, queryset=None):
        """Vérifier que l'utilisateur a accès à ce rapport"""
        rapport = super().get_object(queryset)
        user = self.request.user
        
        # Les admins et superusers peuvent voir tous les rapports
        if user.is_superuser:
            return rapport
        
        # Les pasteurs peuvent voir tous les rapports
        if hasattr(user, 'profile') and user.profile.role == 'pasteur':
            return rapport
        
        # Les patriarches ne peuvent voir que les rapports de leur tribu
        if hasattr(user, 'profile') and user.profile.role == 'patriarche':
            if rapport.tribu and rapport.tribu == user.profile.tribu:
                return rapport
            elif rapport.tribu is None:
                # Les patriarches peuvent voir le rapport global
                return rapport
            else:
                raise Http404("Vous n'avez pas accès à ce rapport.")
        
        # Les responsables ne peuvent voir que les rapports de leur département
        if hasattr(user, 'profile') and user.profile.role == 'responsable':
            if rapport.departement and rapport.departement == user.profile.departement:
                return rapport
            elif rapport.departement is None:
                # Les responsables peuvent voir le rapport global
                return rapport
            else:
                raise Http404("Vous n'avez pas accès à ce rapport.")
        
        # Accès refusé
        raise Http404("Vous n'avez pas accès à ce rapport.")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rapport = self.get_object()
        
        context.update(self.get_user_context())
        context['page_title'] = f'Rapport {rapport.periode_str}'
        
        # Préparer les données pour les graphiques
        if rapport.membres_par_tribu:
            tribu_labels = list(rapport.membres_par_tribu.keys())
            tribu_values = list(rapport.membres_par_tribu.values())
            context['tribu_chart_data'] = json.dumps({
                'labels': tribu_labels,
                'values': tribu_values
            })
        
        if rapport.membres_par_departement:
            dept_labels = list(rapport.membres_par_departement.keys())
            dept_values = list(rapport.membres_par_departement.values())
            context['departement_chart_data'] = json.dumps({
                'labels': dept_labels,
                'values': dept_values
            })
        
        if rapport.cultes_par_type:
            type_labels = list(rapport.cultes_par_type.keys())
            type_values = [culte['participants'] for culte in rapport.cultes_par_type.values()]
            context['type_culte_chart_data'] = json.dumps({
                'labels': type_labels,
                'values': type_values
            })
        
        return context


class RapportTribuView(LoginRequiredMixin, ProtectedDataAccessMixin, DetailView):
    """Rapport mensuel de la tribu du patriarche"""
    model = RapportMensuel
    template_name = 'eglise/rapport_tribu.html'
    context_object_name = 'rapport'
    
    def get_object(self, queryset=None):
        """Récupérer le rapport le plus récent de la tribu"""
        user = self.request.user
        
        # Vérifier que l'utilisateur est patriarche
        if not (hasattr(user, 'profile') and user.profile.role == 'patriarche' and user.profile.tribu):
            raise Http404("Accès refusé.")
        
        # Récupérer le rapport le plus récent de la tribu
        rapport = RapportMensuel.objects.filter(
            tribu=user.profile.tribu,
            departement__isnull=True
        ).order_by('-annee', '-mois').first()
        
        if not rapport:
            raise Http404("Aucun rapport n'existe encore pour votre tribu.")
        
        return rapport
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rapport = self.get_object()
        user = self.request.user
        
        context.update(self.get_user_context())
        context['page_title'] = f'Rapport Tribu {user.profile.tribu.nom} - {rapport.periode_str}'
        context['tribu_name'] = user.profile.tribu.nom
        
        # Préparer les données pour les graphiques
        if rapport.membres_par_departement:
            dept_labels = list(rapport.membres_par_departement.keys())
            dept_values = list(rapport.membres_par_departement.values())
            context['departement_chart_data'] = json.dumps({
                'labels': dept_labels,
                'values': dept_values
            })
        
        if rapport.cultes_par_type:
            type_labels = list(rapport.cultes_par_type.keys())
            type_values = [culte['participants'] for culte in rapport.cultes_par_type.values()]
            context['type_culte_chart_data'] = json.dumps({
                'labels': type_labels,
                'values': type_values
            })
        
        # Historique des rapports de la tribu
        context['historique_rapports'] = RapportMensuel.objects.filter(
            tribu=user.profile.tribu,
            departement__isnull=True
        ).order_by('-annee', '-mois')[:12]
        
        return context


class RapportDepartementView(LoginRequiredMixin, ProtectedDataAccessMixin, DetailView):
    """Rapport mensuel du département du responsable"""
    model = RapportMensuel
    template_name = 'eglise/rapport_departement.html'
    context_object_name = 'rapport'
    
    def get_object(self, queryset=None):
        """Récupérer le rapport le plus récent du département"""
        user = self.request.user
        
        # Vérifier que l'utilisateur est responsable
        if not (hasattr(user, 'profile') and user.profile.role == 'responsable' and user.profile.departement):
            raise Http404("Accès refusé.")
        
        # Récupérer le rapport le plus récent du département
        rapport = RapportMensuel.objects.filter(
            departement=user.profile.departement,
            tribu__isnull=True
        ).order_by('-annee', '-mois').first()
        
        if not rapport:
            raise Http404("Aucun rapport n'existe encore pour votre département.")
        
        return rapport
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rapport = self.get_object()
        user = self.request.user
        
        context.update(self.get_user_context())
        context['page_title'] = f'Rapport Département {user.profile.departement.nom} - {rapport.periode_str}'
        context['departement_name'] = user.profile.departement.nom
        
        # Préparer les données pour les graphiques
        if rapport.membres_par_tribu:
            tribu_labels = list(rapport.membres_par_tribu.keys())
            tribu_values = list(rapport.membres_par_tribu.values())
            context['tribu_chart_data'] = json.dumps({
                'labels': tribu_labels,
                'values': tribu_values
            })
        
        if rapport.cultes_par_type:
            type_labels = list(rapport.cultes_par_type.keys())
            type_values = [culte['participants'] for culte in rapport.cultes_par_type.values()]
            context['type_culte_chart_data'] = json.dumps({
                'labels': type_labels,
                'values': type_values
            })
        
        # Historique des rapports du département
        context['historique_rapports'] = RapportMensuel.objects.filter(
            departement=user.profile.departement,
            tribu__isnull=True
        ).order_by('-annee', '-mois')[:12]
        
        return context
