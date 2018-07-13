from django.urls import path
from django.conrtib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.login, name = 'login', kwargs = {'template_name': 'accounts/login.html'}),
    path('logout/', auth_views.logout, name = 'logout', kwargs = {'next_page': '/'}),
    path('signup/', views.UserCreate.as_view(), name = 'signup'),
    path('profile/', views.profile, name = 'profile'),
]