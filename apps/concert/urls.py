from django.urls import path
from . import views

app_name = 'concert'
urlpatterns = [
    path('list/', views.ConcertList.as_view(), name = 'concert_list'),
    path('list/movie/', views.ConcertList.as_view(), name = 'concert_list_movie'),
    path('list/basket/', views.ConcertList.as_view(), name = 'concert_list_basket'),
    path('detail/<int:pk>/', views.ConcertDetail.as_view(), name = 'concert_detail'),
    path('create/', views.ConcertCreate.as_view(), name = 'concert_create'),
]