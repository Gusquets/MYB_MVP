from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.login, name = 'login', kwargs = {'template_name': 'accounts/login.html'}),
    path('logout/', auth_views.logout, name = 'logout', kwargs = {'next_page': '/'}),
    path('signup/', views.UserCreate.as_view(), name = 'user_create'),
    path('profile/', views.profile, name = 'profile'),
    path('profile/update/', views.UserUpdate.as_view(), name = 'user_update'),
]