from django.urls import path
from . import views

app_name = 'website'
urlpatterns = [
    path('', views.HomeView.as_view(), name = 'home'),

    path('customer/center/', views.CSServiceCreateView.as_view(), name = 'cs_create'),
    path('terms/access/', views.TermView.as_view(), name = 'term_access'),
    path('terms/information/', views.TermView.as_view(), name = 'term_information'),

    path('search/', views.SearchList.as_view(), name = 'search_list'),
]