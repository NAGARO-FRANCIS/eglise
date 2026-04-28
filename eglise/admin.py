from django.contrib import admin
from django.utils.html import format_html
from .models import Tribu, Departement, Membre, Culte, Presence, Statistique


@admin.register(Tribu)
class TribuAdmin(admin.ModelAdmin):
    list_display = ['nom', 'nombre_membres', 'date_creation']
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


@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    list_display = ['nom', 'responsable', 'nombre_membres', 'date_creation']
    search_fields = ['nom', 'responsable', 'description']
    list_filter = ['date_creation']
    ordering = ['nom']
    readonly_fields = ['date_creation']

    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'description', 'responsable')
        }),
        ('Métadonnées', {
            'fields': ('date_creation',),
            'classes': ('collapse',)
        }),
    )


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
            return format_html(
                '<span style="background-color: #4CAF50; color: white; padding: 3px 10px; border-radius: 3px;">Présent</span>'
            )
        else:
            return format_html(
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


# Personnalisation du site admin Django
admin.site.site_header = "🏛️ Gestion d'Église - Administration"
admin.site.site_title = "Admin Église"
admin.site.index_title = "Bienvenue dans l'administration de l'Église"
