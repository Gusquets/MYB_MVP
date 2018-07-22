from django.urls import path
from . import views

app_name = 'website'
urlpatterns = [
    path('', views.HomeView.as_view(), name = 'home'),

    path('customer/center/', views.CSServiceCreateView.as_view(), name = 'cs_create'),
]