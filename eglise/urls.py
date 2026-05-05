from django.urls import path
from . import views
from . import culte_views
from . import views_rapports

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
    
    # Gestion des cultes pour le département STATISTIQUE
    path('cultes/', culte_views.CulteListView.as_view(), name='culte_list'),
    path('cultes/nouveau/', culte_views.CulteCreateView.as_view(), name='culte_create'),
    path('cultes/<int:culte_id>/modifier/', culte_views.CulteUpdateView.as_view(), name='culte_update'),
    path('cultes/<int:culte_id>/supprimer/', culte_views.CulteDeleteView.as_view(), name='culte_delete'),
    path('cultes/statistiques/', culte_views.CulteStatisticsView.as_view(), name='culte_statistics'),
    path('cultes/statistiques-view/', culte_views.CulteStatistiquesViewView.as_view(), name='culte_statistiques_view'),
    path('cultes/participation/ajouter/', culte_views.CulteParticipationAddView.as_view(), name='culte_participation_add'),
    path('cultes/ajouter-participation/', culte_views.AjouterParticipationDimanchemView.as_view(), name='ajouter_participation'),
    
    # API endpoints pour modifier et supprimer les membres
    path('api/membres/update/', views.MembreUpdateAPIView.as_view(), name='api_membre_update'),
    path('api/membres/<int:membre_id>/delete/', views.MembreDeleteAPIView.as_view(), name='api_membre_delete'),
    
    # Rapports mensuels
    path('rapports/', views_rapports.RapportMensuelListView.as_view(), name='rapports_list'),
    path('rapports/<int:pk>/', views_rapports.RapportMensuelDetailView.as_view(), name='rapport_detail'),
    path('mon-rapport-tribu/', views_rapports.RapportTribuView.as_view(), name='rapport_tribu'),
    path('mon-rapport-departement/', views_rapports.RapportDepartementView.as_view(), name='rapport_departement'),
    
    # PWA endpoints
    path('offline/', views.OfflineView.as_view(), name='offline'),
    path('ping/', views.PingView.as_view(), name='ping'),
]
