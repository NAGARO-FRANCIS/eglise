from django.urls import path
from . import views

app_name = 'eglise'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('membres/', views.MembreListView.as_view(), name='membre_list'),
    path('statistiques/', views.StatistiquesView.as_view(), name='statistiques'),
    path('analyse/', views.AnalyseView.as_view(), name='analyse'),
    path('inscription/', views.CategorySelectView.as_view(), name='category-select'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('role-completion/', views.RoleCompletionView.as_view(), name='role-completion'),
]
