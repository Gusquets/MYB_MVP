from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import PasswordChangeForm

urlpatterns = [
    path('login/', views.login, name = 'login'),
    path('logout/', auth_views.logout, name = 'logout', kwargs = {'next_page': '/'}),
    path('profile/', views.Profile.as_view(), name = 'profile'),
    path('profile/update/', auth_views.password_change, name = 'user_update', kwargs={'template_name': 'accounts/profile_update.html','password_change_form': PasswordChangeForm,'post_change_redirect': 'profile'}),

    path('signup/', views.UserCreate.as_view(), name = 'user_create'),
    path('signup/choice/', views.UserCreateChoice.as_view(), name = 'user_create_choice'),
    path('signup/artist/', views.ArtistCreate.as_view(), name = 'artist_create'),
    path('signup/complete/', views.UserCreateComplete.as_view(), name='user_create_complete'),

    path('password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(), name = 'password_reset_done'),
    path('password/reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('pathword/reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name = 'password_reset_complete'),
    path('email/find/', views.FindEmail.as_view(), name='find_email'),
    path('email/find/result/', views.FindEmail.as_view(), name = 'find_email_result'),

    path('artist/list/', views.ArtistList.as_view(), name = 'artist_list'),
    path('artist/list/movie/', views.ArtistList.as_view(), name = 'artist_list_movie'),
    path('artist/list/basket/', views.ArtistList.as_view(), name = 'artist_list_basket'),
    path('artist/detail/<int:pk>/', views.ArtistDetail.as_view(), name = 'artist_detail'),
    path('artist/update/<int:pk>/', views.ArtistUpdate.as_view(), name = 'artist_update'),
]