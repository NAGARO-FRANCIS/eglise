"""
Personnalisation du site admin Django
"""
from django.contrib import admin

# Personnaliser le titre et l'en-tête du site admin
admin.site.site_header = "🏛️ Gestion d'Église - Administration"
admin.site.site_title = "Admin Église"
admin.site.index_title = "Bienvenue dans l'administration de l'Église"
