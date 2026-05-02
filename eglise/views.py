from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, View, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q, Avg, Max, Min
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
from collections import defaultdict
import json
from .models import Membre, Culte, Presence, Tribu, Departement, Statistique, UserProfile
from .forms import SignUpForm, PatriarcheForm, ResponsableForm, PasteurForm, CategorySelectForm, LoginForm, MembreForm, PresenceForm, PresenceMembreSelectionForm, CulteForm
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
    template_name = 'eglise/dashboard_complet.html'
    
    def get_template_names(self):
        """Choisir le template selon le rôle de l'utilisateur"""
        user = self.request.user
        user_role = None
        try:
            if user.is_superuser:
                user_role = 'admin'
            else:
                user_role = user.profile.role
        except:
            pass
        
        # Pour les patriarches et responsables: utiliser le template simple
        if user_role in ['patriarche', 'responsable']:
            return ['eglise/dashboard_simple.html']
        
        # Pour le pasteur et l'admin: utiliser le template complet avec graphiques
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtenir les données filtrées
        membres_filtered = self.get_filtered_queryset(Membre.objects.all())
        stats = self.get_filtered_statistiques()
        
        context.update(stats)
        context.update(self.get_user_context())
        
        user = self.request.user
        is_admin_or_pasteur = user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'pasteur')
        
        # Déterminer le rôle de l'utilisateur
        user_role = None
        try:
            if user.is_superuser:
                user_role = 'admin'
            else:
                user_role = user.profile.role
        except:
            pass
        
        # Statistiques par tribu (filtrées) - Ne pas afficher si l'utilisateur est responsable
        if user_role == 'responsable':
            context['membres_par_tribu'] = []
            context['show_tribu_section'] = False
        else:
            context['show_tribu_section'] = True
            if is_admin_or_pasteur:
                tribu_data = Tribu.objects.annotate(
                    nombre=Count('membre', filter=Q(membre__statut='actif'))
                ).order_by('-nombre')
            else:
                # Patriarche voit sa tribu
                tribu = self.get_user_tribu()
                if tribu:
                    tribu_data = Tribu.objects.filter(id=tribu.id).annotate(
                        nombre=Count('membre', filter=Q(membre__statut='actif'))
                    )
                else:
                    tribu_data = []
            
            context['membres_par_tribu'] = tribu_data
            
            # Préparer les données JSON pour les graphiques
            tribu_json_list = []
            for tribu in tribu_data:
                tribu_json_list.append({
                    'nom': tribu.nom,
                    'nombre': tribu.nombre
                })
            context['membres_par_tribu_json'] = json.dumps(tribu_json_list)
        
        # Statistiques par département (filtrées) - Ne pas afficher si l'utilisateur est patriarche
        if user_role == 'patriarche':
            context['membres_par_departement'] = []
            context['show_departement_section'] = False
        else:
            context['show_departement_section'] = True
            if is_admin_or_pasteur:
                dept_data = Departement.objects.annotate(
                    nombre=Count('membre', filter=Q(membre__statut='actif'))
                ).order_by('-nombre')
            else:
                # Responsable voit son département
                departement = self.get_user_departement()
                if departement:
                    dept_data = Departement.objects.filter(id=departement.id).annotate(
                        nombre=Count('membre', filter=Q(membre__statut='actif'))
                    )
                else:
                    dept_data = []
            
            context['membres_par_departement'] = dept_data
            
            # Préparer les données JSON pour les graphiques
            dept_json_list = []
            for dept in dept_data:
                dept_json_list.append({
                    'nom': dept.nom,
                    'nombre': dept.nombre
                })
            context['membres_par_departement_json'] = json.dumps(dept_json_list)
        
        # Cultes récents (tous les cultes, la participation est filtrée)
        cultes_recents = Culte.objects.all()[:10]
        context['cultes_recents'] = cultes_recents
        
        # Membres par statut (filtrés)
        membres_statut = membres_filtered.values('statut').annotate(
            nombre=Count('id')
        ).order_by('statut')
        context['membres_par_statut'] = membres_statut
        
        # Préparer les données JSON pour les graphiques du statut
        statut_json = []
        for stat in membres_statut:
            statut_json.append({
                'statut': stat['statut'],
                'nombre': stat['nombre']
            })
        context['membres_par_statut_json'] = json.dumps(statut_json)
        
        # Données pour graphique d'assistance par type de culte
        context['attendance_by_type_json'] = self.get_attendance_by_culte_type()
        
        # Données pour graphique de tendance d'assistance par type de culte
        context['attendance_trend_json'] = self.get_attendance_trend_by_culte_type()
        
        # Données de tendance personnalisées pour patriarches et responsables
        if user_role in ['patriarche', 'responsable']:
            context['personalized_trend_json'] = self.get_personalized_attendance_trend(user, user_role)
            
            # Ajouter le nom du responsable
            if user_role == 'patriarche' and hasattr(user, 'profile') and user.profile.tribu:
                context['group_name'] = f"Tribu: {user.profile.tribu.nom}"
            elif user_role == 'responsable' and hasattr(user, 'profile') and user.profile.departement:
                context['group_name'] = f"Département: {user.profile.departement.nom}"
        
        # Données JSON pour les graphiques (si admin ou pasteur)
        if user_role in ['admin', 'pasteur']:
            # Analyse par tribu pour graphique
            analyse_tribu = Tribu.objects.annotate(
                total=Count('membre'),
                actifs=Count('membre', filter=Q(membre__statut='actif'))
            )
            tribu_json = []
            for tribu in analyse_tribu:
                tribu_json.append({
                    'nom': tribu.nom,
                    'total': tribu.total,
                    'actifs': tribu.actifs
                })
            context['tribu_data_json'] = json.dumps(tribu_json)
            
            # Analyse par département pour graphique
            analyse_departement = Departement.objects.annotate(
                total=Count('membre'),
                actifs=Count('membre', filter=Q(membre__statut='actif'))
            )
            dept_json = []
            for dept in analyse_departement:
                dept_json.append({
                    'nom': dept.nom,
                    'total': dept.total,
                    'actifs': dept.actifs
                })
            context['departement_data_json'] = json.dumps(dept_json)
            
            # Tendances de participation
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
            
            trends_list = [
                {'semaine': week, 'count': count}
                for week, count in sorted(participations_par_semaine.items())
            ]
            context['participation_trends_json'] = json.dumps(trends_list)
        
        # Vérifier si c'est un responsable du département STATISTIQUE
        context['is_statistique_responsable'] = False
        if user_role == 'responsable':
            try:
                departement = user.profile.departement
                if departement and departement.nom.upper() == 'STATISTIQUE':
                    context['is_statistique_responsable'] = True
            except:
                pass
        
        # Vérifier si c'est un pasteur ou administrateur
        context['is_pasteur_or_admin'] = (user_role in ['admin', 'pasteur'])
        
        return context
    
    def get_attendance_by_culte_type(self):
        """Prépare les données d'assistance par type de culte pour un graphique en barres"""
        # Mapping des types de culte aux labels en français
        type_culte_labels = {
            'dimanche': 'Dimanche',
            'mercredi': 'Mercredi',
            'special': 'Spécial',
            'autre': 'Autre'
        }
        
        # Compter les présences par type de culte
        presences_by_type = Presence.objects.filter(
            present=True
        ).values('culte__type_culte').annotate(
            total=Count('id')
        )
        
        data_list = []
        for item in presences_by_type:
            culte_type = item['culte__type_culte']
            label = type_culte_labels.get(culte_type, culte_type)
            data_list.append({
                'type': label,
                'count': item['total']
            })
        
        return json.dumps(data_list)
    
    def get_attendance_trend_by_culte_type(self):
        """Prépare les données de tendance d'assistance par type de culte pour un graphique en courbe"""
        # Obtenir les 60 derniers jours
        sixty_days_ago = timezone.now().date() - timedelta(days=60)
        
        # Récupérer toutes les présences des 60 derniers jours avec leurs cultes
        presences = Presence.objects.filter(
            present=True,
            culte__date__gte=sixty_days_ago
        ).select_related('culte').order_by('culte__date')
        
        # Organiser les données par date et type de culte
        dates_set = set()
        culte_types = set()
        attendance_by_date_type = defaultdict(lambda: defaultdict(int))
        
        for presence in presences:
            date_str = presence.culte.date.strftime('%Y-%m-%d')
            culte_type = presence.culte.get_type_culte_display()
            dates_set.add(date_str)
            culte_types.add(culte_type)
            attendance_by_date_type[date_str][culte_type] += 1
        
        # Trier les dates
        sorted_dates = sorted(dates_set)
        sorted_types = sorted(culte_types)
        
        # Préparer les données pour Chart.js
        labels = sorted_dates
        datasets = []
        colors_bg = [
            'rgba(102, 126, 234, 0.2)',
            'rgba(118, 75, 162, 0.2)',
            'rgba(76, 175, 80, 0.2)',
            'rgba(255, 152, 0, 0.2)'
        ]
        colors_border = [
            'rgba(102, 126, 234, 1)',
            'rgba(118, 75, 162, 1)',
            'rgba(76, 175, 80, 1)',
            'rgba(255, 152, 0, 1)'
        ]
        
        for idx, culte_type in enumerate(sorted_types):
            data_points = [
                attendance_by_date_type[date].get(culte_type, 0)
                for date in sorted_dates
            ]
            datasets.append({
                'label': culte_type,
                'data': data_points,
                'borderColor': colors_border[idx % len(colors_border)],
                'backgroundColor': colors_bg[idx % len(colors_bg)],
                'borderWidth': 2,
                'fill': True,
                'tension': 0.4
            })
        
        chart_data = {
            'labels': labels,
            'datasets': datasets
        }
        
        return json.dumps(chart_data)
    
    def get_personalized_attendance_trend(self, user, user_role):
        """Prépare les données de tendance personnalisée pour patriarche/responsable"""
        # Obtenir les 60 derniers jours
        sixty_days_ago = timezone.now().date() - timedelta(days=60)
        
        # Filtrer les membres selon le rôle
        if user_role == 'patriarche':
            tribu = user.profile.tribu
            if not tribu:
                return json.dumps({'labels': [], 'datasets': []})
            membres = Membre.objects.filter(tribu=tribu, statut='actif')
        else:  # responsable
            departement = user.profile.departement
            if not departement:
                return json.dumps({'labels': [], 'datasets': []})
            membres = Membre.objects.filter(departement=departement, statut='actif')
        
        # Récupérer les présences de ces membres pour les 60 derniers jours
        presences = Presence.objects.filter(
            present=True,
            membre__in=membres,
            culte__date__gte=sixty_days_ago
        ).select_related('culte').order_by('culte__date')
        
        # Organiser les données par date
        dates_set = set()
        participants_by_date = defaultdict(int)
        nouveaux_by_date = defaultdict(int)
        
        for presence in presences:
            date_str = presence.culte.date.strftime('%Y-%m-%d')
            dates_set.add(date_str)
            participants_by_date[date_str] += 1
        
        # Pour les nouveaux convertis, on doit les estimer basé sur le culte
        # (puisque nombre_nouveaux est au niveau culte, pas au niveau membre)
        # On va afficher le total de nouveaux du culte pour ces dates
        cultes = Culte.objects.filter(
            date__gte=sixty_days_ago,
            presence__membre__in=membres
        ).distinct().values('date', 'nombre_nouveaux').order_by('date')
        
        for culte in cultes:
            date_str = culte['date'].strftime('%Y-%m-%d')
            nouveaux_by_date[date_str] = culte['nombre_nouveaux']
        
        # Trier les dates
        sorted_dates = sorted(dates_set)
        
        # Préparer les données pour Chart.js
        labels = [date for date in sorted_dates]
        participants_data = [participants_by_date.get(date, 0) for date in sorted_dates]
        nouveaux_data = [nouveaux_by_date.get(date, 0) for date in sorted_dates]
        
        datasets = [
            {
                'label': 'Participants de votre effectif',
                'data': participants_data,
                'borderColor': '#667eea',
                'backgroundColor': 'rgba(102, 126, 234, 0.2)',
                'borderWidth': 2,
                'fill': True,
                'tension': 0.4,
                'pointRadius': 4,
                'pointBackgroundColor': '#667eea'
            }
        ]
        
        # Ajouter les nouveaux convertis uniquement pour les patriarches
        if user_role == 'patriarche':
            datasets.append({
                'label': 'Nouveaux convertis',
                'data': nouveaux_data,
                'borderColor': '#ff9800',
                'backgroundColor': 'rgba(255, 152, 0, 0.2)',
                'borderWidth': 2,
                'fill': True,
                'tension': 0.4,
                'pointRadius': 4,
                'pointBackgroundColor': '#ff9800'
            })
        
        chart_data = {
            'labels': labels,
            'datasets': datasets
        }
        
        return json.dumps(chart_data)


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
    
    def get_template_names(self):
        """Choisir le template selon le rôle de l'utilisateur"""
        user = self.request.user
        user_role = None
        try:
            if user.is_superuser:
                user_role = 'admin'
            else:
                user_role = user.profile.role
        except:
            pass
        
        # Pour les patriarches et responsables: utiliser le template simple
        if user_role in ['patriarche', 'responsable']:
            return ['eglise/statistiques_simple.html']
        
        # Pour le pasteur et l'admin: utiliser le template complet avec graphiques
        return [self.template_name]

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
        evolution_membres = Statistique.objects.all().order_by('date')
        context['evolution_membres'] = evolution_membres
        
        # Préparer les données JSON pour les graphiques
        evolution_json = []
        for stat in evolution_membres:
            evolution_json.append({
                'date': stat.date.strftime('%d/%m/%Y'),
                'total': stat.nombre_total_membres,
                'actifs': stat.nombre_membres_actifs,
                'nouveau': stat.nombre_membres_nouveau,
                'sorti': stat.nombre_membres_sorti
            })
        context['evolution_membres_json'] = json.dumps(evolution_json)
        
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
        
        # Préparer les données JSON pour les top participants
        top_json = []
        for member in top_participants:
            top_json.append({
                'nom_complet': f"{member.prenom} {member.nom}",
                'participations': member.participations
            })
        context['top_participants_json'] = json.dumps(top_json)
        
        # Calculer les taux de participation
        total_presences = Presence.objects.filter(
            culte__date__gte=debut,
            membre__in=membres_filtered
        ).count()
        
        presences_positives = Presence.objects.filter(
            culte__date__gte=debut,
            membre__in=membres_filtered,
            present=True
        ).count()
        
        participation_rates = {
            'presents': presences_positives,
            'absents': total_presences - presences_positives
        }
        context['participation_rates_json'] = json.dumps(participation_rates)
        
        # Données pour le template simple
        context['participation_stats'] = {
            'presents': presences_positives,
            'absents': total_presences - presences_positives,
            'presents_pct': (presences_positives / total_presences * 100) if total_presences > 0 else 0,
            'absents_pct': ((total_presences - presences_positives) / total_presences * 100) if total_presences > 0 else 0,
        }
        
        # Statistiques par statut avec pourcentages
        total_membres = membres_filtered.count()
        statuts = membres_filtered.values('statut').annotate(nombre=Count('id')).order_by('statut')
        statuts_list = []
        statut_display_map = dict(Membre.STATUT_CHOICES)
        for stat in statuts:
            stat['pourcentage'] = (stat['nombre'] / total_membres * 100) if total_membres > 0 else 0
            stat['get_statut_display'] = statut_display_map.get(stat['statut'], stat['statut'])
            statuts_list.append(stat)
        context['membres_par_statut'] = statuts_list
        
        return context


class AnalyseView(ProtectedDataAccessMixin, TemplateView):
    """Vue d'analyse détaillée - filtrée selon le rôle"""
    template_name = 'eglise/analyse.html'
    
    def get_template_names(self):
        """Choisir le template selon le rôle de l'utilisateur"""
        user = self.request.user
        user_role = None
        try:
            if user.is_superuser:
                user_role = 'admin'
            else:
                user_role = user.profile.role
        except:
            pass
        
        # Pour les patriarches et responsables: utiliser le template simple
        if user_role in ['patriarche', 'responsable']:
            return ['eglise/analyse_simple.html']
        
        # Pour le pasteur et l'admin: utiliser le template complet avec graphiques
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        
        # Filtrer les membres selon l'utilisateur
        membres_filtered = self.get_filtered_queryset(Membre.objects.all())
        
        user = self.request.user
        is_admin_or_pasteur = user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'pasteur')
        
        # Déterminer le rôle de l'utilisateur
        user_role = None
        try:
            if user.is_superuser:
                user_role = 'admin'
            else:
                user_role = user.profile.role
        except:
            pass
        
        # Analyse par tribu (filtrée) - Ne pas afficher si l'utilisateur est responsable
        if user_role == 'responsable':
            context['analyse_tribu'] = []
            context['show_tribu_section'] = False
            context['tribu_data_json'] = json.dumps([])
        else:
            context['show_tribu_section'] = True
            if is_admin_or_pasteur:
                analyse_tribu = Tribu.objects.annotate(
                    total=Count('membre'),
                    actifs=Count('membre', filter=Q(membre__statut='actif'))
                )
            else:
                tribu = self.get_user_tribu()
                if tribu:
                    analyse_tribu = Tribu.objects.filter(id=tribu.id).annotate(
                        total=Count('membre'),
                        actifs=Count('membre', filter=Q(membre__statut='actif'))
                    )
                else:
                    analyse_tribu = []
            
            context['analyse_tribu'] = analyse_tribu
            
            # Préparer JSON pour graphique
            tribu_json = []
            for tribu in analyse_tribu:
                tribu_json.append({
                    'nom': tribu.nom,
                    'total': tribu.total,
                    'actifs': tribu.actifs
                })
            context['tribu_data_json'] = json.dumps(tribu_json)
        
        # Analyse par département (filtrée) - Ne pas afficher si l'utilisateur est patriarche
        if user_role == 'patriarche':
            context['analyse_departement'] = []
            context['show_departement_section'] = False
            context['departement_data_json'] = json.dumps([])
        else:
            context['show_departement_section'] = True
            if is_admin_or_pasteur:
                analyse_departement = Departement.objects.annotate(
                    total=Count('membre'),
                    actifs=Count('membre', filter=Q(membre__statut='actif'))
                )
            else:
                departement = self.get_user_departement()
                if departement:
                    analyse_departement = Departement.objects.filter(id=departement.id).annotate(
                        total=Count('membre'),
                        actifs=Count('membre', filter=Q(membre__statut='actif'))
                    )
                else:
                    analyse_departement = []
            
            context['analyse_departement'] = analyse_departement
            
            # Préparer JSON pour graphique
            dept_json = []
            for dept in analyse_departement:
                dept_json.append({
                    'nom': dept.nom,
                    'total': dept.total,
                    'actifs': dept.actifs
                })
            context['departement_data_json'] = json.dumps(dept_json)
        
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
        
        trends_list = [
            {'semaine': week, 'count': count}
            for week, count in sorted(participations_par_semaine.items())
        ]
        context['participations_par_semaine'] = trends_list
        context['participation_trends_json'] = json.dumps(trends_list)
        
        # Données pour le template simple: Évolution des membres
        evolution_membres = Statistique.objects.all().order_by('date')
        context['evolution_membres'] = evolution_membres
        
        return context


class TribuMembreListView(ProtectedDataAccessMixin, TemplateView):
    """Vue pour lister et gérer les membres d'une tribu"""
    template_name = 'eglise/tribu_membres.html'
    
    def get(self, request, tribu_id):
        """Récupère la liste des membres de la tribu"""
        try:
            tribu = Tribu.objects.get(id=tribu_id)
        except Tribu.DoesNotExist:
            return redirect('eglise:dashboard')
        
        # Vérifier que l'utilisateur a accès à cette tribu
        user = request.user
        if not user.is_superuser:
            try:
                if user.profile.role == 'patriarche' and user.profile.tribu_id != tribu_id:
                    return redirect('eglise:dashboard')
            except:
                return redirect('eglise:dashboard')
        
        membres = Membre.objects.filter(tribu=tribu).order_by('nom', 'prenom')
        
        context = {
            'tribu': tribu,
            'membres': membres,
            'form': MembreForm(),
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, tribu_id):
        """Ajoute un nouveau membre à la tribu"""
        try:
            tribu = Tribu.objects.get(id=tribu_id)
        except Tribu.DoesNotExist:
            return redirect('eglise:dashboard')
        
        # Vérifier que l'utilisateur a accès à cette tribu
        user = request.user
        if not user.is_superuser:
            try:
                if user.profile.role == 'patriarche' and user.profile.tribu_id != tribu_id:
                    return redirect('eglise:dashboard')
            except:
                return redirect('eglise:dashboard')
        
        form = MembreForm(request.POST)
        if form.is_valid():
            membre = form.save(commit=False)
            membre.tribu = tribu
            if not membre.departement:
                membre.departement = None
            membre.save()
            return redirect('eglise:tribu_membres', tribu_id=tribu_id)
        
        membres = Membre.objects.filter(tribu=tribu).order_by('nom', 'prenom')
        context = {
            'tribu': tribu,
            'membres': membres,
            'form': form,
        }
        
        return render(request, self.template_name, context)


class DepartementMembreListView(ProtectedDataAccessMixin, TemplateView):
    """Vue pour lister et gérer les membres d'un département"""
    template_name = 'eglise/departement_membres.html'
    
    def get(self, request, departement_id):
        """Récupère la liste des membres du département"""
        try:
            departement = Departement.objects.get(id=departement_id)
        except Departement.DoesNotExist:
            return redirect('eglise:dashboard')
        
        # Vérifier que l'utilisateur a accès à ce département
        user = request.user
        if not user.is_superuser:
            try:
                if user.profile.role == 'responsable' and user.profile.departement_id != departement_id:
                    return redirect('eglise:dashboard')
            except:
                return redirect('eglise:dashboard')
        
        membres = Membre.objects.filter(departement=departement).order_by('nom', 'prenom')
        
        context = {
            'departement': departement,
            'membres': membres,
            'form': MembreForm(),
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, departement_id):
        """Ajoute un nouveau membre au département"""
        try:
            departement = Departement.objects.get(id=departement_id)
        except Departement.DoesNotExist:
            return redirect('eglise:dashboard')
        
        # Vérifier que l'utilisateur a accès à ce département
        user = request.user
        if not user.is_superuser:
            try:
                if user.profile.role == 'responsable' and user.profile.departement_id != departement_id:
                    return redirect('eglise:dashboard')
            except:
                return redirect('eglise:dashboard')
        
        form = MembreForm(request.POST)
        if form.is_valid():
            membre = form.save(commit=False)
            membre.departement = departement
            if not membre.tribu:
                membre.tribu = None
            membre.save()
            return redirect('eglise:departement_membres', departement_id=departement_id)
        
        membres = Membre.objects.filter(departement=departement).order_by('nom', 'prenom')
        context = {
            'departement': departement,
            'membres': membres,
            'form': form,
        }
        
        return render(request, self.template_name, context)


class CultePresenceListView(ProtectedDataAccessMixin, TemplateView):
    """Vue pour gérer la présence à un culte"""
    template_name = 'eglise/culte_presence.html'
    
    def get(self, request, culte_id):
        """Récupère la liste de présence du culte"""
        try:
            culte = Culte.objects.get(id=culte_id)
        except Culte.DoesNotExist:
            return redirect('eglise:dashboard')
        
        # Récupérer les présences du culte
        presences = Presence.objects.filter(culte=culte).select_related('membre').order_by('membre__nom', 'membre__prenom')
        
        # Récupérer tous les membres qui ne sont pas encore dans ce culte
        membres_non_enregistres = Membre.objects.exclude(
            presence__culte=culte
        ).filter(statut='actif')
        
        # Filtrer les membres selon le rôle de l'utilisateur
        user_profile = request.user.profile if hasattr(request.user, 'profile') else None
        if user_profile:
            if user_profile.est_patriarche() and user_profile.tribu:
                # Patriarche: voir uniquement les membres de sa tribu
                membres_non_enregistres = membres_non_enregistres.filter(tribu=user_profile.tribu)
            elif user_profile.est_responsable() and user_profile.departement:
                # Responsable: voir uniquement les membres de son département
                membres_non_enregistres = membres_non_enregistres.filter(departement=user_profile.departement)
            # Pasteur: voit tous les membres (pas de filtrage supplémentaire)
        
        membres_non_enregistres = membres_non_enregistres.order_by('nom', 'prenom')
        
        context = {
            'culte': culte,
            'presences': presences,
            'membres_non_enregistres': membres_non_enregistres,
            'form': PresenceMembreSelectionForm(),
            'user_role': user_profile.get_role_display() if user_profile else 'N/A',
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, culte_id):
        """Ajoute des membres à la liste de présence du culte"""
        try:
            culte = Culte.objects.get(id=culte_id)
        except Culte.DoesNotExist:
            return redirect('eglise:dashboard')
        
        form = PresenceMembreSelectionForm(request.POST)
        if form.is_valid():
            membres = form.cleaned_data['membres']
            
            # Filtrer les membres selon le rôle de l'utilisateur (sécurité)
            user_profile = request.user.profile if hasattr(request.user, 'profile') else None
            if user_profile:
                if user_profile.est_patriarche() and user_profile.tribu:
                    # Patriarche: peut uniquement ajouter les membres de sa tribu
                    membres = membres.filter(tribu=user_profile.tribu)
                elif user_profile.est_responsable() and user_profile.departement:
                    # Responsable: peut uniquement ajouter les membres de son département
                    membres = membres.filter(departement=user_profile.departement)
            
            for membre in membres:
                # Créer la présence si elle n'existe pas déjà
                Presence.objects.get_or_create(
                    membre=membre,
                    culte=culte,
                    defaults={'present': True}
                )
            
            # Mettre à jour le nombre de participants
            culte.mettre_a_jour_nombre_participants()
        
        return redirect('eglise:culte_presence', culte_id=culte_id)


class PresenceToggleView(LoginRequiredMixin, View):
    """Vue pour basculer le statut de présence d'un membre"""
    
    def post(self, request, presence_id):
        """Bascule la présence d'un membre"""
        try:
            presence = Presence.objects.get(id=presence_id)
        except Presence.DoesNotExist:
            return redirect('eglise:dashboard')
        
        # Basculer la présence
        presence.present = not presence.present
        presence.save()
        
        # Mettre à jour le nombre de participants
        presence.culte.mettre_a_jour_nombre_participants()
        
        return redirect('eglise:culte_presence', culte_id=presence.culte.id)


class MembresTotalListView(ProtectedDataAccessMixin, ListView):
    """Liste de tous les membres"""
    model = Membre
    template_name = 'eglise/membre_list.html'
    context_object_name = 'membres'
    paginate_by = 20

    def get_queryset(self):
        queryset = Membre.objects.all()
        # Appliquer le filtrage selon le rôle de l'utilisateur
        queryset = self.get_filtered_queryset(queryset)
        return queryset.order_by('nom', 'prenom')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        context['tribus'] = self.get_filtered_tribus()
        context['departements'] = self.get_filtered_departements()
        context['page_title'] = 'Tous les Membres'
        
        # Ajouter les données pour responsables et patriarches
        try:
            user_profile = self.request.user.profile
            if user_profile.est_responsable() or user_profile.est_patriarche():
                context['show_presence_graphs'] = True
                context.update(self._add_presence_data(context['object_list']))
        except:
            pass
        
        return context
    
    def _add_presence_data(self, membres):
        """Ajoute les données de présence pour les graphes"""
        presence_labels = []
        presence_values = []
        taux_labels = []
        taux_values = []
        
        for membre in membres:
            # Ajouter le compteur de présences
            presences_count = Presence.objects.filter(membre=membre, present=True).count()
            membre.presences_count = presences_count
            
            presence_labels.append(membre.nom_complet())
            presence_values.append(presences_count)
            
            taux_labels.append(membre.nom_complet())
            taux_values.append(membre.taux_participation())
        
        return {
            'presence_data': json.dumps({
                'labels': presence_labels,
                'values': presence_values
            }),
            'taux_data': json.dumps({
                'labels': taux_labels,
                'values': taux_values
            })
        }


class MembresActifsListView(ProtectedDataAccessMixin, ListView):
    """Liste des membres actifs"""
    model = Membre
    template_name = 'eglise/membre_list.html'
    context_object_name = 'membres'
    paginate_by = 20

    def get_queryset(self):
        queryset = Membre.objects.filter(statut='actif')
        # Appliquer le filtrage selon le rôle de l'utilisateur
        queryset = self.get_filtered_queryset(queryset)
        return queryset.order_by('nom', 'prenom')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        context['tribus'] = self.get_filtered_tribus()
        context['departements'] = self.get_filtered_departements()
        context['page_title'] = 'Membres Actifs'
        
        # Ajouter les données pour responsables et patriarches
        try:
            user_profile = self.request.user.profile
            if user_profile.est_responsable() or user_profile.est_patriarche():
                context['show_presence_graphs'] = True
                context.update(self._add_presence_data(context['object_list']))
        except:
            pass
        
        return context
    
    def _add_presence_data(self, membres):
        """Ajoute les données de présence pour les graphes"""
        presence_labels = []
        presence_values = []
        taux_labels = []
        taux_values = []
        
        for membre in membres:
            # Ajouter le compteur de présences
            presences_count = Presence.objects.filter(membre=membre, present=True).count()
            membre.presences_count = presences_count
            
            presence_labels.append(membre.nom_complet())
            presence_values.append(presences_count)
            
            taux_labels.append(membre.nom_complet())
            taux_values.append(membre.taux_participation())
        
        return {
            'presence_data': json.dumps({
                'labels': presence_labels,
                'values': presence_values
            }),
            'taux_data': json.dumps({
                'labels': taux_labels,
                'values': taux_values
            })
        }


class MembresNouveauxListView(ProtectedDataAccessMixin, ListView):
    """Liste des nouveaux membres"""
    model = Membre
    template_name = 'eglise/membre_list.html'
    context_object_name = 'membres'
    paginate_by = 20

    def get_queryset(self):
        queryset = Membre.objects.filter(statut='nouveau')
        # Appliquer le filtrage selon le rôle de l'utilisateur
        queryset = self.get_filtered_queryset(queryset)
        return queryset.order_by('nom', 'prenom')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        context['tribus'] = self.get_filtered_tribus()
        context['departements'] = self.get_filtered_departements()
        context['page_title'] = 'Nouveaux Membres'
        
        # Ajouter les données pour responsables et patriarches
        try:
            user_profile = self.request.user.profile
            if user_profile.est_responsable() or user_profile.est_patriarche():
                context['show_presence_graphs'] = True
                context.update(self._add_presence_data(context['object_list']))
        except:
            pass
        
        return context
    
    def _add_presence_data(self, membres):
        """Ajoute les données de présence pour les graphes"""
        presence_labels = []
        presence_values = []
        taux_labels = []
        taux_values = []
        
        for membre in membres:
            # Ajouter le compteur de présences
            presences_count = Presence.objects.filter(membre=membre, present=True).count()
            membre.presences_count = presences_count
            
            presence_labels.append(membre.nom_complet())
            presence_values.append(presences_count)
            
            taux_labels.append(membre.nom_complet())
            taux_values.append(membre.taux_participation())
        
        return {
            'presence_data': json.dumps({
                'labels': presence_labels,
                'values': presence_values
            }),
            'taux_data': json.dumps({
                'labels': taux_labels,
                'values': taux_values
            })
        }


class MbresSortiListView(ProtectedDataAccessMixin, ListView):
    """Liste des membres sortis"""
    model = Membre
    template_name = 'eglise/membre_list.html'
    context_object_name = 'membres'
    paginate_by = 20

    def get_queryset(self):
        queryset = Membre.objects.filter(statut='sorti')
        # Appliquer le filtrage selon le rôle de l'utilisateur
        queryset = self.get_filtered_queryset(queryset)
        return queryset.order_by('nom', 'prenom')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        context['tribus'] = self.get_filtered_tribus()
        context['departements'] = self.get_filtered_departements()
        context['page_title'] = 'Membres Sortis'
        
        # Ajouter les données pour responsables et patriarches
        try:
            user_profile = self.request.user.profile
            if user_profile.est_responsable() or user_profile.est_patriarche():
                context['show_presence_graphs'] = True
                context.update(self._add_presence_data(context['object_list']))
        except:
            pass
        
        return context
    
    def _add_presence_data(self, membres):
        """Ajoute les données de présence pour les graphes"""
        presence_labels = []
        presence_values = []
        taux_labels = []
        taux_values = []
        
        for membre in membres:
            # Ajouter le compteur de présences
            presences_count = Presence.objects.filter(membre=membre, present=True).count()
            membre.presences_count = presences_count
            
            presence_labels.append(membre.nom_complet())
            presence_values.append(presences_count)
            
            taux_labels.append(membre.nom_complet())
            taux_values.append(membre.taux_participation())
        
        return {
            'presence_data': json.dumps({
                'labels': presence_labels,
                'values': presence_values
            }),
            'taux_data': json.dumps({
                'labels': taux_labels,
                'values': taux_values
            })
        }


# API Endpoints pour modifier et supprimer les membres

class MembreUpdateAPIView(LoginRequiredMixin, View):
    """API pour mettre à jour un membre"""
    
    def post(self, request):
        """Modifie les informations d'un membre"""
        import json
        
        try:
            membre_id = request.POST.get('membre_id')
            membre = Membre.objects.get(id=membre_id)
            
            # Vérifier que l'utilisateur a accès à ce membre
            if not request.user.is_superuser:
                user = request.user
                if hasattr(user, 'profile'):
                    profile = user.profile
                    if profile.est_patriarche() and membre.tribu_id != profile.tribu_id:
                        return JsonResponse({'success': False, 'message': 'Accès refusé'}, status=403)
                    if profile.est_responsable() and membre.departement_id != profile.departement_id:
                        return JsonResponse({'success': False, 'message': 'Accès refusé'}, status=403)
            
            # Mettre à jour les champs
            membre.nom = request.POST.get('nom', membre.nom)
            membre.prenom = request.POST.get('prenom', membre.prenom)
            membre.email = request.POST.get('email', membre.email)
            membre.telephone = request.POST.get('telephone', membre.telephone)
            membre.statut = request.POST.get('statut', membre.statut)
            membre.save()
            
            return JsonResponse({'success': True, 'message': 'Membre modifié avec succès'})
        except Membre.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Membre non trouvé'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)


class MembreDeleteAPIView(LoginRequiredMixin, View):
    """API pour supprimer un membre"""
    
    def delete(self, request, membre_id):
        """Supprime un membre"""
        try:
            membre = Membre.objects.get(id=membre_id)
            
            # Vérifier que l'utilisateur a accès à ce membre
            if not request.user.is_superuser:
                user = request.user
                if hasattr(user, 'profile'):
                    profile = user.profile
                    if profile.est_patriarche() and membre.tribu_id != profile.tribu_id:
                        return JsonResponse({'success': False, 'message': 'Accès refusé'}, status=403)
                    if profile.est_responsable() and membre.departement_id != profile.departement_id:
                        return JsonResponse({'success': False, 'message': 'Accès refusé'}, status=403)
            
            nom_complet = membre.nom_complet()
            membre.delete()
            
            return JsonResponse({'success': True, 'message': f'{nom_complet} a été supprimé'})
        except Membre.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Membre non trouvé'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        context['tribus'] = self.get_filtered_tribus()
        context['departements'] = self.get_filtered_departements()
        context['page_title'] = 'Membres Sortis'
        
        # Ajouter les données pour responsables et patriarches
        user_profile = self.request.user.profile
        if user_profile.est_responsable() or user_profile.est_patriarche():
            context['show_presence_graphs'] = True
            context.update(self._add_presence_data(context['object_list']))
        
        return context
    
    def _add_presence_data(self, membres):
        """Ajoute les données de présence pour les graphes"""
        presence_labels = []
        presence_values = []
        taux_labels = []
        taux_values = []
        
        for membre in membres:
            # Ajouter le compteur de présences
            presences_count = Presence.objects.filter(membre=membre, present=True).count()
            membre.presences_count = presences_count
            
            presence_labels.append(membre.nom_complet())
            presence_values.append(presences_count)
            
            taux_labels.append(membre.nom_complet())
            taux_values.append(membre.taux_participation())
        
        return {
            'presence_data': json.dumps({
                'labels': presence_labels,
                'values': presence_values
            }),
            'taux_data': json.dumps({
                'labels': taux_labels,
                'values': taux_values
            })
        }
