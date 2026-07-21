from django.contrib import admin
from django.utils.html import format_html, mark_safe
from .models import Tribu, Departement, Membre, Culte, Presence, Statistique, UserProfile, RapportMensuel, RapportHebdomadaire


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'get_role_display', 'get_tribu_or_departement', 'date_creation']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    list_filter = ['role', 'date_creation']
    readonly_fields = ['date_creation']
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user', 'role')
        }),
        ('Affectation', {
            'fields': ('tribu', 'departement')
        }),
        ('Photo', {
            'fields': ('photo',)
        }),
        ('Métadonnées', {
            'fields': ('date_creation',),
            'classes': ('collapse',)
        }),
    )
    
    def get_username(self, obj):
        """Affiche le nom complet et le nom d'utilisateur"""
        return f"{obj.user.get_full_name() or obj.user.username}"
    get_username.short_description = "Utilisateur"
    
    def get_role_display(self, obj):
        """Affiche le rôle avec une couleur"""
        couleurs = {
            'pasteur': '#4CAF50',
            'patriarche': '#2196F3',
            'responsable': '#FF9800',
        }
        couleur = couleurs.get(obj.role, '#000000')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            couleur,
            obj.get_role_display()
        )
    get_role_display.short_description = "Rôle"
    
    def get_tribu_or_departement(self, obj):
        """Affiche la tribu ou le département assigné"""
        if obj.role == 'patriarche' and obj.tribu:
            return f"Tribu: {obj.tribu.nom}"
        elif obj.role == 'responsable' and obj.departement:
            return f"Département: {obj.departement.nom}"
        return "—"
    get_tribu_or_departement.short_description = "Affectation"


@admin.register(Tribu)
class TribuAdmin(admin.ModelAdmin):
    list_display = ['nom', 'get_patriarche', 'nombre_membres', 'date_creation']
    search_fields = ['nom', 'description']
    ordering = ['nom']
    readonly_fields = ['date_creation']

    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'description')
        }),
        ('Métadonnées', {
            'fields': ('date_creation',),
            'classes': ('collapse',)
        }),
    )
    
    def get_patriarche(self, obj):
        """Affiche le patriarche de la tribu"""
        patriarche = obj.patriarches.first()
        if patriarche:
            return f"{patriarche.user.get_full_name() or patriarche.user.username}"
        return "—"
    get_patriarche.short_description = "Patriarche"


@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    list_display = ['nom', 'get_responsable', 'nombre_membres', 'date_creation']
    search_fields = ['nom', 'description']
    list_filter = ['date_creation']
    ordering = ['nom']
    readonly_fields = ['date_creation']

    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'description')
        }),
        ('Métadonnées', {
            'fields': ('date_creation',),
            'classes': ('collapse',)
        }),
    )
    
    def get_responsable(self, obj):
        """Affiche le responsable du département"""
        responsable = obj.responsables.first()
        if responsable:
            return f"{responsable.user.get_full_name() or responsable.user.username}"
        return "—"
    get_responsable.short_description = "Responsable"


@admin.register(Membre)
class MembreAdmin(admin.ModelAdmin):
    list_display = ['nom_complet', 'email', 'tribu', 'departement', 'statut_badge', 'taux_participation']
    search_fields = ['nom', 'prenom', 'email', 'telephone']
    list_filter = ['statut', 'genre', 'tribu', 'departement', 'date_adhesion']
    readonly_fields = ['date_creation', 'date_modification', 'taux_participation']
    ordering = ['nom', 'prenom']

    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'email', 'telephone', 'adresse', 'genre', 'date_naissance')
        }),
        ('Informations d\'église', {
            'fields': ('tribu', 'departement', 'statut', 'date_adhesion', 'date_depart')
        }),
        ('Notes et suivi', {
            'fields': ('notes',)
        }),
        ('Statistiques', {
            'fields': ('taux_participation',),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )

    def statut_badge(self, obj):
        """Affiche le statut avec une couleur"""
        couleurs = {
            'nouveau': '#FF9800',
            'actif': '#4CAF50',
            'sorti': '#F44336',
            'inactif': '#9E9E9E',
        }
        couleur = couleurs.get(obj.statut, '#000000')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            couleur,
            obj.get_statut_display()
        )
    statut_badge.short_description = 'Statut'


@admin.register(Culte)
class CulteAdmin(admin.ModelAdmin):
    list_display = ['date', 'type_culte', 'theme', 'predicateur', 'nombre_participants']
    search_fields = ['theme', 'predicateur', 'notes']
    list_filter = ['type_culte', 'date']
    readonly_fields = ['date_creation', 'nombre_participants']
    ordering = ['-date']

    fieldsets = (
        ('Informations du culte', {
            'fields': ('date', 'type_culte', 'theme', 'predicateur')
        }),
        ('Participants', {
            'fields': ('nombre_participants',)
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Métadonnées', {
            'fields': ('date_creation',),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.mettre_a_jour_nombre_participants()


class PresenceInline(admin.TabularInline):
    model = Presence
    extra = 0
    readonly_fields = ['date_enregistrement']
    fields = ['membre', 'present', 'date_enregistrement']


@admin.register(Presence)
class PresenceAdmin(admin.ModelAdmin):
    list_display = ['membre', 'culte', 'present_badge', 'date_enregistrement']
    search_fields = ['membre__nom', 'membre__prenom']
    list_filter = ['present', 'culte__date', 'culte__type_culte']
    readonly_fields = ['date_enregistrement']
    ordering = ['-culte__date']

    fieldsets = (
        ('Informations', {
            'fields': ('membre', 'culte', 'present')
        }),
        ('Métadonnées', {
            'fields': ('date_enregistrement',),
            'classes': ('collapse',)
        }),
    )

    def present_badge(self, obj):
        """Affiche le statut de présence avec une couleur"""
        if obj.present:
            return mark_safe(
                '<span style="background-color: #4CAF50; color: white; padding: 3px 10px; border-radius: 3px;">Présent</span>'
            )
        else:
            return mark_safe(
                '<span style="background-color: #F44336; color: white; padding: 3px 10px; border-radius: 3px;">Absent</span>'
            )
    present_badge.short_description = 'Statut'


@admin.register(Statistique)
class StatistiqueAdmin(admin.ModelAdmin):
    list_display = ['date', 'nombre_total_membres', 'nombre_membres_actifs', 'nombre_membres_nouveau', 'taux_participation_moyen']
    list_filter = ['date']
    readonly_fields = ['date', 'nombre_total_membres', 'nombre_membres_actifs', 'nombre_membres_nouveau', 'nombre_membres_sorti', 'taux_participation_moyen']
    ordering = ['-date']

    fieldsets = (
        ('Statistiques générales', {
            'fields': ('date', 'nombre_total_membres', 'nombre_membres_actifs')
        }),
        ('Statistiques détaillées', {
            'fields': ('nombre_membres_nouveau', 'nombre_membres_sorti', 'taux_participation_moyen')
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(RapportHebdomadaire)
class RapportHebdomadaireAdmin(admin.ModelAdmin):
    list_display = ['date_debut', 'date_fin', 'type_rapport', 'tribu', 'total_participants', 'total_nouveaux']
    list_filter = ['type_rapport', 'date_debut', 'tribu']
    ordering = ['-date_fin', 'type_rapport']
    readonly_fields = ['date_creation']


@admin.register(RapportMensuel)
class RapportMensuelAdmin(admin.ModelAdmin):
    list_display = ['periode_str', 'nombre_total_membres', 'taux_participation_moyen', 'statut_badge', 'auteur']
    search_fields = ['notes', 'observations']
    list_filter = ['annee', 'mois', 'statut', 'date_creation']
    readonly_fields = ['date_creation', 'date_modification', 'date_validation', 'periode_str']
    ordering = ['-annee', '-mois']
    
    fieldsets = (
        ('Période du rapport', {
            'fields': ('mois', 'annee', 'periode_str')
        }),
        ('Données générales', {
            'fields': ('nombre_total_membres', 'nombre_membres_actifs', 'nombre_membres_nouveau', 'nombre_membres_inactif', 'nombre_membres_sorti')
        }),
        ('Données par structure', {
            'fields': ('nombre_tribus', 'nombre_departements', 'membres_par_tribu', 'membres_par_departement'),
            'classes': ('collapse',)
        }),
        ('Statistiques d\'assistance', {
            'fields': ('nombre_cultes', 'nombre_total_presences', 'nombre_total_absences', 'taux_participation_moyen', 'cultes_par_type')
        }),
        ('Annotations', {
            'fields': ('notes', 'observations')
        }),
        ('Gestion du rapport', {
            'fields': ('statut', 'auteur', 'date_creation', 'date_modification', 'date_validation'),
            'classes': ('collapse',)
        }),
    )
    
    def statut_badge(self, obj):
        """Affiche le statut avec une couleur"""
        couleurs = {
            'brouillon': '#FFC107',
            'valide': '#4CAF50',
            'archive': '#9E9E9E',
        }
        couleur = couleurs.get(obj.statut, '#000000')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            couleur,
            obj.get_statut_display()
        )
    statut_badge.short_description = 'Statut'
    
    def periode_str(self, obj):
        """Retourne la période en format lisible"""
        mois_names = {
            1: 'Janvier', 2: 'Février', 3: 'Mars', 4: 'Avril',
            5: 'Mai', 6: 'Juin', 7: 'Juillet', 8: 'Août',
            9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Décembre'
        }
        return f"{mois_names.get(obj.mois, 'N/A')} {obj.annee}"
    periode_str.short_description = 'Période'


# Personnalisation du site admin Django
admin.site.site_header = "🏛️ Gestion d'Église - Administration"
admin.site.site_title = "Admin Église"
admin.site.index_title = "Bienvenue dans l'administration de l'Église"
