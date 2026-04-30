#!/usr/bin/env python
# Script to add Culte views to views.py

import re

# Read the views.py file
with open('eglise/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find where MembreDeleteAPIView ends and remove any duplicated code
lines = content.split('\n')
valid_lines = []
in_duplicate = False

for i, line in enumerate(lines):
    # Check if we're in the duplicate/broken code section
    if 'context = super().get_context_data(**kwargs)' in line and i > 500:
        # Skip these duplicate lines
        in_duplicate = True
        continue
    
    if in_duplicate and i > len(lines) - 100:  # Stop skipping near the end
        # Rejoin the non-duplicated content
        valid_lines = lines[:i]
        break
    
    if not in_duplicate:
        valid_lines.append(line)

# Rejoin clean content
clean_content = '\n'.join(valid_lines)

# Add the Culte views code
culte_views_code = '''


# ============= GESTION DES CULTES - DÉPARTEMENT STATISTIQUE =============

class CulteListView(LoginRequiredMixin, TemplateView):
    """Vue pour lister les cultes - accessible uniquement aux responsables du département STATISTIQUE"""
    template_name = 'eglise/culte_list.html'
    
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        cultes = Culte.objects.all().order_by('-date')
        
        for culte in cultes:
            culte.nombre_enregistrements = Presence.objects.filter(culte=culte).count()
        
        context['cultes'] = cultes
        context['form'] = CulteForm()
        context['page_title'] = '📈 Gestion des Cultes - Statistiques'
        
        cultes_last_3_months = Culte.objects.filter(
            date__gte=timezone.now().date() - timedelta(days=90)
        ).order_by('-date')
        
        if cultes_last_3_months.exists():
            moyenne_participants = int(cultes_last_3_months.aggregate(
                avg=Avg('nombre_participants')
            )['avg'] or 0)
        else:
            moyenne_participants = 0
        
        context['stats'] = {
            'total_cultes': Culte.objects.count(),
            'total_cultes_3m': cultes_last_3_months.count(),
            'moyenne_participants': moyenne_participants,
            'total_participants_3m': cultes_last_3_months.count(),
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
            culte.delete()
            return redirect('eglise:culte_list')
        except Culte.DoesNotExist:
            return redirect('eglise:culte_list')


class CulteStatisticsView(LoginRequiredMixin, TemplateView):
    """Vue pour afficher les statistiques détaillées des cultes"""
    template_name = 'eglise/culte_statistics.html'
    
    def dispatch(self, request, *args, **kwargs):
        """Vérifie que l'utilisateur a accès"""
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
        
        three_months_ago = timezone.now().date() - timedelta(days=90)
        cultes = Culte.objects.filter(date__gte=three_months_ago).order_by('date')
        
        evolution_data = []
        for culte in cultes:
            evolution_data.append({
                'date': culte.date.strftime('%d/%m/%Y'),
                'participants': culte.nombre_participants,
                'type': culte.get_type_culte_display(),
                'theme': culte.theme or 'N/A'
            })
        
        context['evolution_data_json'] = json.dumps(evolution_data)
        
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
'''

final_content = clean_content + culte_views_code

# Write the corrected file
with open('eglise/views.py', 'w', encoding='utf-8') as f:
    f.write(final_content)

print('✓ Successfully cleaned and updated eglise/views.py with Culte views')
