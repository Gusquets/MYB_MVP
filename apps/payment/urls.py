from django.urls import path
from . import views

app_name = 'payment'
urlpatterns = [
    path('sponsor/<int:artist_id>/', views.SponsorCreate.as_view(), name = 'sponsor_create'),
]