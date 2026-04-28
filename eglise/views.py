from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, View
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict
from .models import Membre, Culte, Presence, Tribu, Departement, Statistique, UserProfile
from .forms import SignUpForm, PatriarcheForm, ResponsableForm, PasteurForm, CategorySelectForm, LoginForm
from .mixins import DataFilteringMixin, ProtectedDataAccessMixin, RoleRequiredMixin


class LoginView(View):
    """Vue de connexion"""
    template_name = 'eglise/login.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('eglise:dashboard')
        form = LoginForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('eglise:dashboard')
            else:
                form.add_error(None, "Nom d'utilisateur ou mot de passe incorrect.")
        
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    """Vue de déconnexion"""
    
    def get(self, request):
        logout(request)
        return redirect('eglise:login')


class CategorySelectView(View):
    """Vue de sélection de catégorie (Patriarche ou Responsable)"""
    template_name = 'eglise/category_select.html'
    
    def get(self, request):
        form = CategorySelectForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = CategorySelectForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            request.session['selected_category'] = category
            return redirect('eglise:signup')
        return render(request, self.template_name, {'form': form})


class SignUpView(View):
    """Vue d'inscription avec détails adaptés à la catégorie"""
    template_name = 'eglise/signup.html'
    
    def get(self, request):
        if 'selected_category' not in request.session:
            return redirect('eglise:category-select')
        
        category = request.session['selected_category']
        form = SignUpForm()
        
        context = {
            'form': form,
            'category': category,
            'tribu_choices': Tribu.objects.all() if category == 'patriarche' else None,
            'departement_choices': Departement.objects.all() if category == 'responsable' else None,
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request):
        if 'selected_category' not in request.session:
            return redirect('eglise:category-select')
        
        category = request.session['selected_category']
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            # Créer l'utilisateur
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Stocker les infos dans la session
            request.session['new_user_id'] = user.id
            request.session['user_category'] = category
            
            return redirect('eglise:role-completion')
        
        context = {
            'form': form,
            'category': category,
            'tribu_choices': Tribu.objects.all() if category == 'patriarche' else None,
            'departement_choices': Departement.objects.all() if category == 'responsable' else None,
        }
        
        return render(request, self.template_name, context)


class RoleCompletionView(TemplateView):
    """Vue pour compléter le profil selon la catégorie"""
    template_name = 'eglise/role_completion.html'
    
    def get(self, request):
        if 'new_user_id' not in request.session or 'user_category' not in request.session:
            return redirect('eglise:category-select')
        
        user_id = request.session.get('new_user_id')
        category = request.session.get('user_category')
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect('eglise:category-select')
        
        context = {
            'category': category,
            'user': user,
        }
        
        if category == 'patriarche':
            context['form'] = PatriarcheForm()
            context['form_title'] = "Complétez votre profil - Patriarche de Tribu"
            context['tribu_choices'] = Tribu.objects.all()
        elif category == 'responsable':
            context['form'] = ResponsableForm()
            context['form_title'] = "Complétez votre profil - Responsable de Département"
            context['departement_choices'] = Departement.objects.all()
        
        return render(request, self.template_name, context)
    
    def post(self, request):
        if 'new_user_id' not in request.session or 'user_category' not in request.session:
            return redirect('eglise:category-select')
        
        user_id = request.session.get('new_user_id')
        category = request.session.get('user_category')
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect('eglise:category-select')
        
        if category == 'patriarche':
            form = PatriarcheForm(request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = user
                profile.role = 'patriarche'
                profile.save()
        elif category == 'responsable':
            form = ResponsableForm(request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = user
                profile.role = 'responsable'
                profile.save()
        else:
            return redirect('eglise:category-select')
        
        # Connecter l'utilisateur
        login(request, user)
        
        # Nettoyer la session
        del request.session['new_user_id']
        del request.session['user_category']
        del request.session['selected_category']
        
        return redirect('eglise:dashboard')


def get_user_profile(user):
    """Récupère le profil de l'utilisateur"""
    try:
        return user.profile
    except UserProfile.DoesNotExist:
        return None


class DashboardView(ProtectedDataAccessMixin, TemplateView):
    """Vue du tableau de bord avec les statistiques principales"""
    template_name = 'eglise/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtenir les données filtrées
        membres_filtered = self.get_filtered_queryset(Membre.objects.all())
        stats = self.get_filtered_statistiques()
        
        context.update(stats)
        context.update(self.get_user_context())
        
        user = self.request.user
        is_admin_or_pasteur = user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'pasteur')
        
        # Statistiques par tribu (filtrées)
        if is_admin_or_pasteur:
            context['membres_par_tribu'] = Tribu.objects.annotate(
                nombre=Count('membre', filter=Q(membre__statut='actif'))
            ).order_by('-nombre')
        else:
            # Patriarche voit sa tribu, responsable voit ses membres groupés
            tribu = self.get_user_tribu()
            if tribu:
                context['membres_par_tribu'] = Tribu.objects.filter(id=tribu.id).annotate(
                    nombre=Count('membre', filter=Q(membre__statut='actif'))
                )
            else:
                context['membres_par_tribu'] = []
        
        # Statistiques par département (filtrées)
        if is_admin_or_pasteur:
            context['membres_par_departement'] = Departement.objects.annotate(
                nombre=Count('membre', filter=Q(membre__statut='actif'))
            ).order_by('-nombre')
        else:
            # Responsable voit son département, patriarche voit les départements de sa tribu
            departement = self.get_user_departement()
            if departement:
                context['membres_par_departement'] = Departement.objects.filter(id=departement.id).annotate(
                    nombre=Count('membre', filter=Q(membre__statut='actif'))
                )
            else:
                context['membres_par_departement'] = []
        
        # Cultes récents (tous les cultes, la participation est filtrée)
        cultes_recents = Culte.objects.all()[:10]
        context['cultes_recents'] = cultes_recents
        
        # Membres par statut (filtrés)
        context['membres_par_statut'] = membres_filtered.values('statut').annotate(
            nombre=Count('id')
        ).order_by('statut')
        
        return context


class MembreListView(ProtectedDataAccessMixin, ListView):
    """Liste des membres avec filtres - visible seulement pour les membres pertinents"""
    model = Membre
    template_name = 'eglise/membre_list.html'
    context_object_name = 'membres'
    paginate_by = 20

    def get_queryset(self):
        queryset = Membre.objects.all()
        
        # Appliquer le filtrage selon le rôle de l'utilisateur
        queryset = self.get_filtered_queryset(queryset)
        
        # Filtres supplémentaires
        statut = self.request.GET.get('statut')
        tribu = self.request.GET.get('tribu')
        departement = self.request.GET.get('departement')
        
        if statut:
            queryset = queryset.filter(statut=statut)
        
        # Pour les filtres tribu/département, s'assurer que l'utilisateur a accès
        user = self.request.user
        is_admin = user.is_superuser
        
        try:
            user_profile = user.profile
        except:
            user_profile = None
        
        if tribu:
            # Tribu : accessible pour les pasteurs, admins et le patriarche de cette tribu
            if is_admin or (user_profile and user_profile.role == 'pasteur'):
                queryset = queryset.filter(tribu_id=tribu)
            elif user_profile and user_profile.role == 'patriarche' and user_profile.tribu.id == int(tribu):
                queryset = queryset.filter(tribu_id=tribu)
            else:
                queryset = queryset.none()
        
        if departement:
            # Département : accessible pour les pasteurs, admins et le responsable de ce département
            if is_admin or (user_profile and user_profile.role == 'pasteur'):
                queryset = queryset.filter(departement_id=departement)
            elif user_profile and user_profile.role == 'responsable' and user_profile.departement.id == int(departement):
                queryset = queryset.filter(departement_id=departement)
            else:
                queryset = queryset.none()
        
        return queryset.order_by('nom', 'prenom')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        
        # Fournir les choix de filtrage accessibles
        context['tribus'] = self.get_filtered_tribus()
        context['departements'] = self.get_filtered_departements()
        
        return context


class StatistiquesView(ProtectedDataAccessMixin, TemplateView):
    """Vue des statistiques détaillées - filtrées selon le rôle"""
    template_name = 'eglise/statistiques.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        
        # Filtrer les membres selon l'utilisateur
        membres_filtered = self.get_filtered_queryset(Membre.objects.all())
        
        # Statistiques par mois
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
        
        # Évolution des membres
        context['evolution_membres'] = Statistique.objects.all().order_by('date')
        
        # Top participants (filtrés selon les membres accessibles)
        cultes_recentes = Culte.objects.filter(
            date__gte=debut
        ).values_list('id', flat=True)
        
        top_participants = membres_filtered.annotate(
            participations=Count('presence', filter=Q(
                presence__culte_id__in=cultes_recentes,
                presence__present=True
            ))
        ).order_by('-participations')[:10]
        
        context['top_participants'] = top_participants
        
        return context


class AnalyseView(ProtectedDataAccessMixin, TemplateView):
    """Vue d'analyse détaillée - filtrée selon le rôle"""
    template_name = 'eglise/analyse.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        
        # Filtrer les membres selon l'utilisateur
        membres_filtered = self.get_filtered_queryset(Membre.objects.all())
        
        user = self.request.user
        is_admin_or_pasteur = user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'pasteur')
        
        # Analyse par tribu (filtrée)
        if is_admin_or_pasteur:
            context['analyse_tribu'] = Tribu.objects.annotate(
                total=Count('membre'),
                actifs=Count('membre', filter=Q(membre__statut='actif'))
            )
        else:
            tribu = self.get_user_tribu()
            if tribu:
                context['analyse_tribu'] = Tribu.objects.filter(id=tribu.id).annotate(
                    total=Count('membre'),
                    actifs=Count('membre', filter=Q(membre__statut='actif'))
                )
            else:
                context['analyse_tribu'] = []
        
        # Analyse par département (filtrée)
        if is_admin_or_pasteur:
            context['analyse_departement'] = Departement.objects.annotate(
                total=Count('membre'),
                actifs=Count('membre', filter=Q(membre__statut='actif'))
            )
        else:
            departement = self.get_user_departement()
            if departement:
                context['analyse_departement'] = Departement.objects.filter(id=departement.id).annotate(
                    total=Count('membre'),
                    actifs=Count('membre', filter=Q(membre__statut='actif'))
                )
            else:
                context['analyse_departement'] = []
        
        # Tendances de participation filtrées
        trois_mois_ago = timezone.now().date() - timedelta(days=90)
        presences = Presence.objects.filter(
            culte__date__gte=trois_mois_ago,
            present=True,
            membre__in=membres_filtered
        ).select_related('culte')
        
        participations_par_semaine = defaultdict(int)
        for presence in presences:
            week_key = presence.culte.date.strftime('%Y-W%U')
            participations_par_semaine[week_key] += 1
        
        context['participations_par_semaine'] = [
            {'semaine': week, 'count': count}
            for week, count in sorted(participations_par_semaine.items())
        ]
        
        return context
