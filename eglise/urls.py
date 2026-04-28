from django.urls import path
from . import views

app_name = 'eglise'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('membres/', views.MembreListView.as_view(), name='membre_list'),
    path('statistiques/', views.StatistiquesView.as_view(), name='statistiques'),
    path('analyse/', views.AnalyseView.as_view(), name='analyse'),
]
