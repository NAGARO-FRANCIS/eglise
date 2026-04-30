from django.urls import path
from . import views

app_name = 'eglise'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('membres/', views.MembreListView.as_view(), name='membre_list'),
    path('membres/total/', views.MembresTotalListView.as_view(), name='membres_total'),
    path('membres/actifs/', views.MembresActifsListView.as_view(), name='membres_actifs'),
    path('membres/nouveaux/', views.MembresNouveauxListView.as_view(), name='membres_nouveaux'),
    path('membres/sortis/', views.MbresSortiListView.as_view(), name='membres_sortis'),
    path('statistiques/', views.StatistiquesView.as_view(), name='statistiques'),
    path('analyse/', views.AnalyseView.as_view(), name='analyse'),
    path('inscription/', views.CategorySelectView.as_view(), name='category-select'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('role-completion/', views.RoleCompletionView.as_view(), name='role-completion'),
    
    # Gestion des membres par tribu et département
    path('tribu/<int:tribu_id>/membres/', views.TribuMembreListView.as_view(), name='tribu_membres'),
    path('departement/<int:departement_id>/membres/', views.DepartementMembreListView.as_view(), name='departement_membres'),
    
    # Gestion de la présence par culte
    path('culte/<int:culte_id>/presence/', views.CultePresenceListView.as_view(), name='culte_presence'),
    path('presence/<int:presence_id>/toggle/', views.PresenceToggleView.as_view(), name='presence_toggle'),
]
