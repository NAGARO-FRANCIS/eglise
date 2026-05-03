"""
Vue d'administration pour permettre au superuser de voir tous les tribues et départements
"""

from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Membre, Tribu, Departement


class AdminTribuDepartementView(LoginRequiredMixin, TemplateView):
    """Vue d'administration pour voir tous les tribues et départements (pour superuser)"""
    template_name = 'eglise/admin_tribu_departement.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Vérifier que l'utilisateur est superuser
        if not request.user.is_superuser:
            return redirect('eglise:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Récupérer le mode de visualisation (tribu ou departement)
        mode = self.request.GET.get('mode', 'tribu')
        
        if mode == 'departement':
            # Afficher tous les départements
            departements = Departement.objects.all().order_by('nom')
            departements_data = []
            
            for dept in departements:
                membres_count = Membre.objects.filter(departement=dept).count()
                actifs_count = Membre.objects.filter(departement=dept, statut='actif').count()
                nouveaux_count = Membre.objects.filter(departement=dept, statut='nouveau').count()
                
                # Calculer le pourcentage d'actifs
                pourcentage_actifs = 0
                if membres_count > 0:
                    pourcentage_actifs = round((actifs_count * 100) / membres_count)
                
                departements_data.append({
                    'obj': dept,
                    'total': membres_count,
                    'actifs': actifs_count,
                    'nouveaux': nouveaux_count,
                    'pourcentage_actifs': pourcentage_actifs,
                })
            
            context['departements'] = departements_data
            context['mode'] = 'departement'
            context['page_title'] = '🏢 Vue d\'Administration - Tous les Départements'
        else:
            # Afficher tous les tribues (par défaut)
            tribus = Tribu.objects.all().order_by('nom')
            tribus_data = []
            
            for tribu in tribus:
                membres_count = Membre.objects.filter(tribu=tribu).count()
                actifs_count = Membre.objects.filter(tribu=tribu, statut='actif').count()
                nouveaux_count = Membre.objects.filter(tribu=tribu, statut='nouveau').count()
                
                # Calculer le pourcentage d'actifs
                pourcentage_actifs = 0
                if membres_count > 0:
                    pourcentage_actifs = round((actifs_count * 100) / membres_count)
                
                tribus_data.append({
                    'obj': tribu,
                    'total': membres_count,
                    'actifs': actifs_count,
                    'nouveaux': nouveaux_count,
                    'pourcentage_actifs': pourcentage_actifs,
                })
            
            context['tribus'] = tribus_data
            context['mode'] = 'tribu'
            context['page_title'] = '📍 Vue d\'Administration - Toutes les Tribues'
        
        return context
