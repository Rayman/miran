from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='backend/index.html'), name='index'),
    path('login', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('fight', views.FightList.as_view(), name='fight'),
    path('fight/<int:pk>', views.Fight.as_view(), name='fight'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('inventory', views.Inventory.as_view(), name='inventory'),
    path('levelup', views.LevelUp.as_view(), name='levelup'),
    path('levelup/success', views.LevelUp.as_view(), name='levelupview', kwargs={'success': True}),
]
