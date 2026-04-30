# CULTE MANAGEMENT VIEWS - Add to eglise/views.py

class CulteListView(LoginRequiredMixin, TemplateView):
    """Vue pour lister les cultes - accessible uniquement aux responsables du département STATISTIQUE"""
    template_name = 'eglise/culte_list.html'
    
    def dispatch(self, request, *args, **kwargs):
        """Vérifie que l'utilisateur est responsable du département STATISTIQUE"""
        if not request.user.is_authenticated:
            return redirect('eglise:login')
        
        # Vérifier que l'utilisateur est admin ou responsable statistique
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        
        try:
            profile = request.user.profile
            if profile.role == 'pasteur':
                return super().dispatch(request, *args, **kwargs)
            elif profile.role == 'responsable':
                # Vérifier que c'est le département STATISTIQUE
                if profile.departement and profile.departement.nom == 'STATISTIQUE':
                    return super().dispatch(request, *args, **kwargs)
        except UserProfile.DoesNotExist:
            pass
        
        return redirect('eglise:dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Récupérer tous les cultes triés par date décroissante
        cultes = Culte.objects.all().order_by('-date')
        
        # Ajouter les statistiques pour chaque culte
        for culte in cultes:
            culte.nombre_enregistrements = Presence.objects.filter(culte=culte).count()
        
        context['cultes'] = cultes
        context['form'] = CulteForm()
        context['page_title'] = '📈 Gestion des Cultes - Statistiques'
        
        # Récupérer les statistiques de participation
        cultes_last_3_months = Culte.objects.filter(
            date__gte=timezone.now().date() - timedelta(days=90)
        ).order_by('-date')
        
        # Calcul des moyennes
        if cultes_last_3_months.exists():
            moyenne_participants = int(cultes_last_3_months.aggregate(
                avg=Avg('nombre_participants')
            )['avg'] or 0)
            total_participants_3m = cultes_last_3_months.aggregate(
                total=Count('nombre_participants')
            )['total'] or 0
        else:
            moyenne_participants = 0
            total_participants_3m = 0
        
        context['stats'] = {
            'total_cultes': Culte.objects.count(),
            'total_cultes_3m': cultes_last_3_months.count(),
            'moyenne_participants': moyenne_participants,
            'total_participants_3m': total_participants_3m,
        }
        
        return context


class CulteCreateView(LoginRequiredMixin, View):
    """Vue pour créer un nouveau culte"""
    
    def dispatch(self, request, *args, **kwargs):
        """Vérifie que l'utilisateur est responsable du département STATISTIQUE"""
        if not request.user.is_authenticated:
            return redirect('eglise:login')
        
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        
        try:
            profile = request.user.profile
            if profile.role == 'pasteur':
                return super().dispatch(request, *args, **kwargs)
            elif profile.role == 'responsable':
                if profile.departement and profile.departement.nom == 'STATISTIQUE':
                    return super().dispatch(request, *args, **kwargs)
        except UserProfile.DoesNotExist:
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
            culte = form.save()
            return redirect('eglise:culte_list')
        
        return render(request, 'eglise/culte_form.html', {
            'form': form,
            'page_title': '➕ Ajouter un Culte',
            'action': 'create'
        })


class CulteUpdateView(LoginRequiredMixin, View):
    """Vue pour modifier un culte"""
    
    def dispatch(self, request, *args, **kwargs):
        """Vérifie que l'utilisateur est responsable du département STATISTIQUE"""
        if not request.user.is_authenticated:
            return redirect('eglise:login')
        
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        
        try:
            profile = request.user.profile
            if profile.role == 'pasteur':
                return super().dispatch(request, *args, **kwargs)
            elif profile.role == 'responsable':
                if profile.departement and profile.departement.nom == 'STATISTIQUE':
                    return super().dispatch(request, *args, **kwargs)
        except UserProfile.DoesNotExist:
            pass
        
        return redirect('eglise:dashboard')
    
    def get(self, request, culte_id):
        try:
            culte = Culte.objects.get(id=culte_id)
        except Culte.DoesNotExist:
            return redirect('eglise:culte_list')
        
        form = CulteForm(instance=culte)
        return render(request, 'eglise/culte_form.html', {
            'form': form,
            'culte': culte,
            'page_title': f'✏️ Modifier le Culte du {culte.date}',
            'action': 'update'
        })
    
    def post(self, request, culte_id):
        try:
            culte = Culte.objects.get(id=culte_id)
        except Culte.DoesNotExist:
            return redirect('eglise:culte_list')
        
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


class CulteDeleteView(LoginRequiredMixin, View):
    """Vue pour supprimer un culte"""
    
    def dispatch(self, request, *args, **kwargs):
        """Vérifie que l'utilisateur est responsable du département STATISTIQUE"""
        if not request.user.is_authenticated:
            return redirect('eglise:login')
        
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        
        try:
            profile = request.user.profile
            if profile.role == 'pasteur':
                return super().dispatch(request, *args, **kwargs)
            elif profile.role == 'responsable':
                if profile.departement and profile.departement.nom == 'STATISTIQUE':
                    return super().dispatch(request, *args, **kwargs)
        except UserProfile.DoesNotExist:
            pass
        
        return redirect('eglise:dashboard')
    
    def post(self, request, culte_id):
        try:
            culte = Culte.objects.get(id=culte_id)
            date_culte = culte.date
            culte.delete()
            return redirect('eglise:culte_list')
        except Culte.DoesNotExist:
            return redirect('eglise:culte_list')


class CulteStatisticsView(LoginRequiredMixin, TemplateView):
    """Vue pour afficher les statistiques détaillées des cultes avec graphiques"""
    template_name = 'eglise/culte_statistics.html'
    
    def dispatch(self, request, *args, **kwargs):
        """Vérifie que l'utilisateur est responsable du département STATISTIQUE ou admin/pasteur"""
        if not request.user.is_authenticated:
            return redirect('eglise:login')
        
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        
        try:
            profile = request.user.profile
            if profile.role == 'pasteur':
                return super().dispatch(request, *args, **kwargs)
            elif profile.role == 'responsable':
                if profile.departement and profile.departement.nom == 'STATISTIQUE':
                    return super().dispatch(request, *args, **kwargs)
        except UserProfile.DoesNotExist:
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
        for stat in type_stats:
            type_data.append({
                'type': Culte.TYPE_CULTE_CHOICES[
                    [choice[0] for choice in Culte.TYPE_CULTE_CHOICES].index(stat['type_culte'])
                ][1],
                'count': stat['count'],
                'avg_participants': int(stat['avg_participants'] or 0)
            })
        
        context['type_data_json'] = json.dumps(type_data)
        
        # Statistiques globales
        context['stats'] = {
            'total_cultes': cultes.count(),
            'total_participants': cultes.aggregate(total=Count('nombre_participants'))['total'] or 0,
            'average_participants': int(cultes.aggregate(avg=Avg('nombre_participants'))['avg'] or 0),
            'max_participants': cultes.aggregate(max=Max('nombre_participants'))['max'] or 0,
            'min_participants': cultes.filter(nombre_participants__gt=0).aggregate(min=Min('nombre_participants'))['min'] or 0,
        }
        
        context['page_title'] = '📊 Statistiques Détaillées des Cultes'
        
        return context
