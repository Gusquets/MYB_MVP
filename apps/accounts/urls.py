from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login, name = 'login'),
    path('logout/', auth_views.logout, name = 'logout', kwargs = {'next_page': '/'}),
    path('profile/', views.Profile.as_view(), name = 'profile'),
    path('profile/update/', views.UserUpdate.as_view(), name = 'user_update'),

    path('signup/', views.UserCreate.as_view(), name = 'user_create'),
    path('signup/choice/', views.UserCreateChoice.as_view(), name = 'user_create_choice'),
    path('signup/artist/', views.ArtistCreate.as_view(), name = 'artist_create'),
    path('signup/complete/', views.UserCreateComplete.as_view(), name='user_create_complete'),

    path('password/change', views.PasswordChangeView.as_view(), name='password_change'),

    path('password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('email/find/', views.FindEmail.as_view(), name='find_email'),

    path('artist/list/', views.ArtistList.as_view(), name = 'artist_list'),
    path('artist/detail/<int:pk>/', views.ArtistDetail.as_view(), name = 'artist_detail'),
]