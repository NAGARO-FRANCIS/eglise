from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict
from .models import Membre, Culte, Presence, Tribu, Departement, Statistique, UserProfile
from .forms import SignUpForm, PatriarcheForm, ResponsableForm, PasteurForm


class SignUpView(CreateView):
    """Vue d'inscription avec sélection de rôle"""
    template_name = 'eglise/signup.html'
    form_class = SignUpForm
    success_url = '/role-completion/'
    
    def form_valid(self, form):
        # Créer l'utilisateur
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        
        # Stocker le rôle dans la session
        self.request.session['new_user_id'] = user.id
        self.request.session['user_role'] = form.cleaned_data['role']
        
        return redirect('eglise:role-completion')


class RoleCompletionView(TemplateView):
    """Vue pour compléter le profil selon le rôle"""
    template_name = 'eglise/role_completion.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if 'new_user_id' not in self.request.session:
            return redirect('eglise:signup')
        
        user_id = self.request.session.get('new_user_id')
        role = self.request.session.get('user_role')
        
        context['role'] = role
        context['user_id'] = user_id
        
        if role == 'patriarche':
            context['form'] = PatriarcheForm()
            context['form_title'] = "Complétez votre profil - Patriarche de Tribu"
        elif role == 'responsable':
            context['form'] = ResponsableForm()
            context['form_title'] = "Complétez votre profil - Responsable de Département"
        else:  # pasteur
            context['form'] = PasteurForm()
            context['form_title'] = "Complétez votre profil - Pasteur"
        
        return context
    
    def post(self, request, *args, **kwargs):
        if 'new_user_id' not in request.session:
            return redirect('eglise:signup')
        
        user_id = request.session.get('new_user_id')
        role = request.session.get('user_role')
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect('eglise:signup')
        
        if role == 'patriarche':
            form = PatriarcheForm(request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = user
                profile.save()
        elif role == 'responsable':
            form = ResponsableForm(request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = user
                profile.save()
        else:  # pasteur
            form = PasteurForm(request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = user
                profile.save()
        
        # Connecter l'utilisateur
        login(request, user)
        
        # Nettoyer la session
        del request.session['new_user_id']
        del request.session['user_role']
        
        return redirect('eglise:dashboard')


def get_user_profile(user):
    """Récupère le profil de l'utilisateur"""
    try:
        return user.profile
    except UserProfile.DoesNotExist:
        return None


class DashboardView(LoginRequiredMixin, TemplateView):
    """Vue du tableau de bord avec les statistiques principales"""
    template_name = 'eglise/dashboard.html'
    login_url = 'eglise:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistiques générales
        context['total_membres'] = Membre.objects.count()
        context['membres_actifs'] = Membre.objects.filter(statut='actif').count()
        context['membres_nouveau'] = Membre.objects.filter(statut='nouveau').count()
        context['membres_sorti'] = Membre.objects.filter(statut='sorti').count()
        
        # Statistiques par tribu
        context['membres_par_tribu'] = Tribu.objects.annotate(
            nombre=Count('membre')
        ).order_by('-nombre')
        
        # Statistiques par département
        context['membres_par_departement'] = Departement.objects.annotate(
            nombre=Count('membre')
        ).order_by('-nombre')
        
        # Cultes récents et participation
        cultes_recents = Culte.objects.all()[:10]
        context['cultes_recents'] = cultes_recents
        
        # Taux de participation moyen
        trois_mois_ago = timezone.now().date() - timedelta(days=90)
        cultes_total = Culte.objects.filter(date__gte=trois_mois_ago).count()
        if cultes_total > 0:
            presences = Presence.objects.filter(
                culte__date__gte=trois_mois_ago,
                present=True
            ).count()
            context['taux_participation_moyen'] = round((presences / (cultes_total * context['membres_actifs'])) * 100, 1) if context['membres_actifs'] > 0 else 0
        else:
            context['taux_participation_moyen'] = 0
        
        # Membres actifs et inactifs
        context['membres_par_statut'] = Membre.objects.values('statut').annotate(
            nombre=Count('id')
        ).order_by('statut')
        
        return context


class MembreListView(ListView):
    """Liste des membres avec filtres"""
    model = Membre
    template_name = 'eglise/membre_list.html'
    context_object_name = 'membres'
    paginate_by = 20

    def get_queryset(self):
        queryset = Membre.objects.all()
        
        # Filtres
        statut = self.request.GET.get('statut')
        tribu = self.request.GET.get('tribu')
        departement = self.request.GET.get('departement')
        
        if statut:
            queryset = queryset.filter(statut=statut)
        if tribu:
            queryset = queryset.filter(tribu_id=tribu)
        if departement:
            queryset = queryset.filter(departement_id=departement)
        
        return queryset.order_by('nom', 'prenom')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tribus'] = Tribu.objects.all()
        context['departements'] = Departement.objects.all()
        return context


class StatistiquesView(TemplateView):
    """Vue des statistiques détaillées"""
    template_name = 'eglise/statistiques.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistiques par mois - Approche en Python pour compatibilité SQLite
        debut = timezone.now().date() - timedelta(days=90)
        cultes = Culte.objects.filter(date__gte=debut).order_by('date')
        
        cultes_par_mois = defaultdict(int)
        for culte in cultes:
            month_key = culte.date.strftime('%Y-%m')
            cultes_par_mois[month_key] += 1
        
        context['cultes_par_mois'] = [
            {'month': month, 'count': count}
            for month, count in sorted(cultes_par_mois.items())
        ]
        
        # Membres par statut (évolution)
        context['evolution_membres'] = Statistique.objects.all().order_by('date')
        
        # Top participants
        cultes_recentes = Culte.objects.filter(
            date__gte=debut
        ).values_list('id', flat=True)
        
        top_participants = Membre.objects.annotate(
            participations=Count('presence', filter=Q(
                presence__culte_id__in=cultes_recentes,
                presence__present=True
            ))
        ).order_by('-participations')[:10]
        
        context['top_participants'] = top_participants
        
        return context


class AnalyseView(TemplateView):
    """Vue d'analyse détaillée"""
    template_name = 'eglise/analyse.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Analyse par tribu
        context['analyse_tribu'] = Tribu.objects.annotate(
            total=Count('membre'),
            actifs=Count('membre', filter=Q(membre__statut='actif'))
        )
        
        # Analyse par département
        context['analyse_departement'] = Departement.objects.annotate(
            total=Count('membre'),
            actifs=Count('membre', filter=Q(membre__statut='actif'))
        )
        
        # Tendances de participation - Approche en Python pour compatibilité SQLite
        trois_mois_ago = timezone.now().date() - timedelta(days=90)
        presences = Presence.objects.filter(
            culte__date__gte=trois_mois_ago,
            present=True
        ).select_related('culte')
        
        participations_par_semaine = defaultdict(int)
        for presence in presences:
            # Obtenir le numéro de semaine
            week_key = presence.culte.date.strftime('%Y-W%U')
            participations_par_semaine[week_key] += 1
        
        context['participations_par_semaine'] = [
            {'semaine': week, 'count': count}
            for week, count in sorted(participations_par_semaine.items())
        ]
        
        return context
