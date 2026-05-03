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

from .models import Culte, Presence, Membre, Departement
from .forms import CulteForm, ParticipationDimanchemForm


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
        
        # Récupérer TOUS les cultes pour les graphiques (pas de filtrage par date)
        all_cultes = Culte.objects.all().order_by('-date')
        
        # Données pour graphique d'évolution - utiliser TOUS les cultes
        evolution_data = []
        for culte in all_cultes.order_by('date'):
            evolution_data.append({
                'date': culte.date.strftime('%d/%m/%Y'),
                'participants': culte.nombre_participants,
                'nouveaux': culte.nombre_nouveaux,
                'type': culte.get_type_culte_display(),
                'theme': culte.theme or 'N/A'
            })
        
        context['evolution_data_json'] = json.dumps(evolution_data)
        context['cultes_list'] = all_cultes  # Liste de tous les cultes pour affichage
        
        # Données par type de culte - utiliser TOUS les cultes
        type_stats = all_cultes.values('type_culte').annotate(
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
        
        # ===== DONNÉES DES SERVITEURS (MEMBRES DES DÉPARTEMENTS) =====
        # Compter les serviteurs (membres actifs) par département
        all_membres = Membre.objects.filter(statut='actif')
        
        serviteurs_data = []
        departements = Departement.objects.all()
        for dept in departements:
            serviteurs_count = all_membres.filter(departement=dept).count()
            serviteurs_data.append({
                'departement': dept.nom,
                'nombre': serviteurs_count,
                'id': dept.id
            })
        
        context['serviteurs_data_json'] = json.dumps(serviteurs_data)
        
        # Données pour courbe d'évolution des serviteurs par mois
        serviteurs_evolution = []
        # Grouper par date de création du membre
        membres_by_date = all_membres.values('date_creation').annotate(
            count=Count('id')
        ).order_by('date_creation')
        
        cumulative_count = 0
        for item in membres_by_date:
            if item['date_creation']:
                cumulative_count += item['count']
                serviteurs_evolution.append({
                    'date': item['date_creation'].strftime('%d/%m/%Y'),
                    'nombre': cumulative_count
                })
        
        # Si pas de date_creation, créer des données temporelles
        if not serviteurs_evolution:
            # Utiliser les données de dates des membres
            all_membres_ordered = all_membres.order_by('id')[:100]  # Limitation pour éviter trop de données
            for idx, membre in enumerate(all_membres_ordered, 1):
                serviteurs_evolution.append({
                    'date': f'Membre {idx}',
                    'nombre': idx
                })
        
        context['serviteurs_evolution_json'] = json.dumps(serviteurs_evolution)
        
        # Statistiques des serviteurs
        context['stats_serviteurs'] = {
            'total_serviteurs': all_membres.count(),
            'serviteurs_par_departement': serviteurs_data,
        }
        
        # Statistiques globales
        context['stats'] = {
            'total_cultes': all_cultes.count(),
            'total_participants': sum(c.nombre_participants for c in all_cultes),
            'total_nouveaux': sum(c.nombre_nouveaux for c in all_cultes),
            'average_participants': int(all_cultes.aggregate(avg=Avg('nombre_participants'))['avg'] or 0),
            'max_participants': all_cultes.aggregate(max=Max('nombre_participants'))['max'] or 0,
            'min_participants': all_cultes.filter(nombre_participants__gt=0).aggregate(min=Min('nombre_participants'))['min'] or 0,
        }
        
        context['page_title'] = '📊 Statistiques Détaillées des Cultes'
        
        return context


class CulteStatistiquesViewView(LoginRequiredMixin, TemplateView):
    """Vue pour consulter les statistiques des cultes (lecture seule)"""
    template_name = 'eglise/culte_statistiques_view.html'
    
    def dispatch(self, request, *args, **kwargs):
        """Autorise uniquement pasteur et administrateur"""
        if not request.user.is_authenticated:
            return redirect('eglise:login')
        
        # Administrateur et pasteur peuvent accéder
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        
        try:
            profile = request.user.profile
            if profile.role == 'pasteur':
                return super().dispatch(request, *args, **kwargs)
        except:
            pass
        
        return redirect('eglise:dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Récupérer TOUS les cultes
        all_cultes = Culte.objects.all().order_by('-date')
        
        # Données des 3 derniers mois pour les graphiques
        three_months_ago = timezone.now().date() - timedelta(days=90)
        cultes = Culte.objects.filter(date__gte=three_months_ago).order_by('date')
        
        # Données pour graphique d'évolution
        evolution_data = []
        for culte in cultes:
            evolution_data.append({
                'date': culte.date.strftime('%d/%m/%Y'),
                'participants': culte.nombre_participants,
                'nouveaux': culte.nombre_nouveaux,
                'type': culte.get_type_culte_display(),
                'theme': culte.theme or 'N/A'
            })
        
        context['evolution_data_json'] = json.dumps(evolution_data)
        context['cultes_list'] = all_cultes
        
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
        context['stats'] = {
            'total_cultes': all_cultes.count(),
            'total_participants': sum(c.nombre_participants for c in all_cultes),
            'total_nouveaux': sum(c.nombre_nouveaux for c in all_cultes),
            'average_participants': int(all_cultes.aggregate(avg=Avg('nombre_participants'))['avg'] or 0),
            'max_participants': all_cultes.aggregate(max=Max('nombre_participants'))['max'] or 0,
            'min_participants': all_cultes.filter(nombre_participants__gt=0).aggregate(min=Min('nombre_participants'))['min'] or 0,
        }
        
        context['page_title'] = '📊 Consultation des Statistiques'
        
        return context


class AjouterParticipationDimanchemView(LoginRequiredMixin, View):
    """Vue pour ajouter rapidement la participation au dimanche"""
    
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
    
    def post(self, request):
        from django.http import JsonResponse
        form = ParticipationDimanchemForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            nombre_participants = form.cleaned_data['nombre_participants']
            nombre_nouveaux = form.cleaned_data['nombre_nouveaux']
            
            # Chercher si un culte existe déjà pour cette date et type 'dimanche'
            culte, created = Culte.objects.get_or_create(
                date=date,
                type_culte='dimanche',
                defaults={
                    'nombre_participants': nombre_participants,
                    'nombre_nouveaux': nombre_nouveaux
                }
            )
            
            # Si le culte existe déjà, mettre à jour les données
            if not created:
                culte.nombre_participants = nombre_participants
                culte.nombre_nouveaux = nombre_nouveaux
                culte.save()
            
            return JsonResponse({
                'success': True,
                'message': f'✅ Participation enregistrée pour le {date.strftime("%d/%m/%Y")}: {nombre_participants} participants ({nombre_nouveaux} nouveaux)',
                'date': date.strftime('%d/%m/%Y'),
                'participants': nombre_participants,
                'nouveaux': nombre_nouveaux
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)


class CulteParticipationAddView(LoginRequiredMixin, TemplateView):
    """Vue pour afficher le formulaire d'enregistrement de participation au culte"""
    template_name = 'eglise/culte_participation_add.html'
    
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
        """Affiche le formulaire d'enregistrement de participation"""
        form = ParticipationDimanchemForm()
        return render(request, self.template_name, {
            'form': form,
            'page_title': '📊 Enregistrer la Participation au Culte',
        })
    
    def post(self, request):
        """Enregistre les données de participation au culte"""
        form = ParticipationDimanchemForm(request.POST)
        success_message = None
        
        if form.is_valid():
            date = form.cleaned_data['date']
            nombre_participants = form.cleaned_data['nombre_participants']
            nombre_nouveaux = form.cleaned_data['nombre_nouveaux']
            
            # Chercher si un culte existe déjà pour cette date et type 'dimanche'
            culte, created = Culte.objects.get_or_create(
                date=date,
                type_culte='dimanche',
                defaults={
                    'nombre_participants': nombre_participants,
                    'nombre_nouveaux': nombre_nouveaux
                }
            )
            
            # Si le culte existe déjà, mettre à jour les données
            if not created:
                culte.nombre_participants = nombre_participants
                culte.nombre_nouveaux = nombre_nouveaux
                culte.save()
                success_message = f'✅ Participation mise à jour pour le {date.strftime("%d/%m/%Y")}: {nombre_participants} participants ({nombre_nouveaux} nouveaux)'
            else:
                success_message = f'✅ Participation enregistrée pour le {date.strftime("%d/%m/%Y")}: {nombre_participants} participants ({nombre_nouveaux} nouveaux)'
            
            # Réinitialiser le formulaire après un enregistrement réussi
            form = ParticipationDimanchemForm()
        
        return render(request, self.template_name, {
            'form': form,
            'page_title': '📊 Enregistrer la Participation au Culte',
            'success_message': success_message,
        })
