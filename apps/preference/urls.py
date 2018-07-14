from django.urls import path
from . import views

app_name = 'preference'
urlpatterns = [
    path('basket/create/<int:id>/', views.basket_create, name = 'basket_create'),
]