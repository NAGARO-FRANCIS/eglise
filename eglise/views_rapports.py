# Vues pour les rapports mensuels
from django.views.generic import ListView, DetailView
from django.utils import timezone
import json
from .models import RapportMensuel
from .mixins import ProtectedDataAccessMixin


class RapportMensuelListView(ProtectedDataAccessMixin, ListView):
    """Liste des rapports mensuels"""
    model = RapportMensuel
    template_name = 'eglise/rapport_mensuel_list.html'
    context_object_name = 'rapports'
    paginate_by = 12
    
    def get_queryset(self):
        """Retourner les rapports filtrés selon le rôle"""
        # Les admins et pasteurs voient tous les rapports
        if self.request.user.is_superuser or (hasattr(self.request.user, 'profile') and self.request.user.profile.role == 'pasteur'):
            return RapportMensuel.objects.all().order_by('-annee', '-mois')
        
        # Les patriarches et responsables voient tous les rapports aussi
        return RapportMensuel.objects.all().order_by('-annee', '-mois')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        context['page_title'] = 'Rapports Mensuels'
        
        # Ajouter les stats générales
        context['nombre_rapports'] = RapportMensuel.objects.count()
        context['rapports_valides'] = RapportMensuel.objects.filter(statut='valide').count()
        
        return context


class RapportMensuelDetailView(ProtectedDataAccessMixin, DetailView):
    """Détail d'un rapport mensuel"""
    model = RapportMensuel
    template_name = 'eglise/rapport_mensuel_detail.html'
    context_object_name = 'rapport'
    
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
