from django.urls import path
from . import views

app_name = 'payment'
urlpatterns = [
    path('sponsor/<int:artist_id>/', views.sponsor_create, name = 'sponsor_create'),
    path('sponsor/pay/complete/', views.PayComplete.as_view(), name = 'pay_complete'),
]