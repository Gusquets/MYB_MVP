from django.urls import path
from . import views

app_name = 'concert'
urlpatterns = [
    path('list/', views.ConcertList.as_view(), name = 'concert_list'),
    path('detail/<int:pk>/', views.ConcertDetail.as_view(), name = 'concert_detail'),
    path('create/', views.ConcertCreate.as_view(), name = 'concert_create'),
]