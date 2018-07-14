from django.urls import path
from . import views

app_name = 'preference'
urlpatterns = [
    path('basket/create/concert/<int:id>/', views.basket_create_concert, name = 'basket_create_concert'),
    path('basket/create/artist/<int:id>/', views.basket_create_artist, name = 'basket_create_artist'),
]