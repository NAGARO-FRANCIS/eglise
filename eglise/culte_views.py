"""
Culte Management Views for Statistics Department
These views allow the STATISTIQUE department to manage worship services and their attendance data
"""

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Avg, Max, Min
from django.utils import timezone
from datetime import timedelta
import json

from .models import Culte, Presence
from .forms import CulteForm


class CulteListView(LoginRequiredMixin, TemplateView):
    """Vue pour lister les cultes"""
    template_name = 'eglise/culte_list.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('eglise:login')
        
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        
        try:
            profile = request.user.profile
            if profile.role == 'pasteur':
                return super().dispatch(request, *args, **kwargs)
            elif profile.role == 'responsable' and profile.departement and profile.departement.nom == 'STATISTIQUE':
                return super().dispatch(request, *args, **kwargs)
        except:
            pass
        
        return redirect('eglise:dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cultes = Culte.objects.all().order_by('-date')
        
        for culte in cultes:
            culte.nombre_enregistrements = Presence.objects.filter(culte=culte).count()
        
        context['cultes'] = cultes
        context['form'] = CulteForm()
        context['page_title'] = '📈 Gestion des Cultes - Statistiques'
        
        cultes_3m = Culte.objects.filter(date__gte=timezone.now().date() - timedelta(days=90))
        context['stats'] = {
            'total_cultes': Culte.objects.count(),
            'total_cultes_3m': cultes_3m.count(),
            'moyenne_participants': int(cultes_3m.aggregate(avg=Avg('nombre_participants'))['avg'] or 0),
        }
        
        return context


class CulteCreateView(LoginRequiredMixin, View):
    """Vue pour créer un nouveau culte"""
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('eglise:login')
        
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        
        try:
            profile = request.user.profile
            if profile.role == 'pasteur':
                return super().dispatch(request, *args, **kwargs)
            elif profile.role == 'responsable' and profile.departement and profile.departement.nom == 'STATISTIQUE':
                return super().dispatch(request, *args, **kwargs)
        except:
            pass
        
        return redirect('eglise:dashboard')
    
    def get(self, request):
        form = CulteForm()
        return render(request, 'eglise/culte_form.html', {
            'form': form,
            'page_title': '➕ Ajouter un Culte',
            'action': 'create'
        })
    
    def post(self, request):
        form = CulteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('eglise:culte_list')
        
        return render(request, 'eglise/culte_form.html', {
            'form': form,
            'page_title': '➕ Ajouter un Culte',
            'action': 'create'
        })


class CulteUpdateView(LoginRequiredMixin, View):
    """Vue pour modifier un culte"""
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('eglise:login')
        
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        
        try:
            profile = request.user.profile
            if profile.role == 'pasteur':
                return super().dispatch(request, *args, **kwargs)
            elif profile.role == 'responsable' and profile.departement and profile.departement.nom == 'STATISTIQUE':
                return super().dispatch(request, *args, **kwargs)
        except:
            pass
        
        return redirect('eglise:dashboard')
    
    def get(self, request, culte_id):
        try:
            culte = Culte.objects.get(id=culte_id)
            form = CulteForm(instance=culte)
            return render(request, 'eglise/culte_form.html', {
                'form': form,
                'culte': culte,
                'page_title': f'✏️ Modifier le Culte du {culte.date}',
                'action': 'update'
            })
        except:
            return redirect('eglise:culte_list')
    
    def post(self, request, culte_id):
        try:
            culte = Culte.objects.get(id=culte_id)
            form = CulteForm(request.POST, instance=culte)
            if form.is_valid():
                form.save()
                return redirect('eglise:culte_list')
            
            return render(request, 'eglise/culte_form.html', {
                'form': form,
                'culte': culte,
                'page_title': f'✏️ Modifier le Culte du {culte.date}',
                'action': 'update'
            })
        except:
            return redirect('eglise:culte_list')


class CulteDeleteView(LoginRequiredMixin, View):
    """Vue pour supprimer un culte"""
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('eglise:login')
        
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        
        try:
            profile = request.user.profile
            if profile.role == 'pasteur':
                return super().dispatch(request, *args, **kwargs)
            elif profile.role == 'responsable' and profile.departement and profile.departement.nom == 'STATISTIQUE':
                return super().dispatch(request, *args, **kwargs)
        except:
            pass
        
        return redirect('eglise:dashboard')
    
    def post(self, request, culte_id):
        try:
            culte = Culte.objects.get(id=culte_id)
            culte.delete()
        except:
            pass
        
        return redirect('eglise:culte_list')


class CulteStatisticsView(LoginRequiredMixin, TemplateView):
    """Vue pour afficher les statistiques détaillées des cultes avec graphiques"""
    template_name = 'eglise/culte_statistics.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('eglise:login')
        
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        
        try:
            profile = request.user.profile
            if profile.role == 'pasteur':
                return super().dispatch(request, *args, **kwargs)
            elif profile.role == 'responsable' and profile.departement and profile.departement.nom == 'STATISTIQUE':
                return super().dispatch(request, *args, **kwargs)
        except:
            pass
        
        return redirect('eglise:dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Données des 3 derniers mois
        three_months_ago = timezone.now().date() - timedelta(days=90)
        cultes = Culte.objects.filter(date__gte=three_months_ago).order_by('date')
        
        # Données pour graphique d'évolution
        evolution_data = []
        for culte in cultes:
            evolution_data.append({
                'date': culte.date.strftime('%d/%m/%Y'),
                'participants': culte.nombre_participants,
                'type': culte.get_type_culte_display(),
                'theme': culte.theme or 'N/A'
            })
        
        context['evolution_data_json'] = json.dumps(evolution_data)
        
        # Données par type de culte
        type_stats = cultes.values('type_culte').annotate(
            count=Count('id'),
            avg_participants=Avg('nombre_participants')
        )
        
        type_data = []
        type_culte_choices = dict(Culte.TYPE_CULTE_CHOICES)
        for stat in type_stats:
            type_data.append({
                'type': type_culte_choices.get(stat['type_culte'], stat['type_culte']),
                'count': stat['count'],
                'avg_participants': int(stat['avg_participants'] or 0)
            })
        
        context['type_data_json'] = json.dumps(type_data)
        
        # Statistiques globales
        all_cultes = Culte.objects.all()
        context['stats'] = {
            'total_cultes': all_cultes.count(),
            'total_participants': sum(c.nombre_participants for c in all_cultes),
            'average_participants': int(all_cultes.aggregate(avg=Avg('nombre_participants'))['avg'] or 0),
            'max_participants': all_cultes.aggregate(max=Max('nombre_participants'))['max'] or 0,
            'min_participants': all_cultes.filter(nombre_participants__gt=0).aggregate(min=Min('nombre_participants'))['min'] or 0,
        }
        
        context['page_title'] = '📊 Statistiques Détaillées des Cultes'
        
        return context
