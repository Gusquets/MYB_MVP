from django.urls import path
from. import views

app_name = 'concert_post'
urlpatterns = [
    path('', views.postview, name="concert_post_list"),
    path('create/', views.create, name="concert_post_create"),
    path('<int:post_pk>/detail/', views.detail, name='concert_post_detail'),
    path('<int:post_pk>/comment_post/create/', views.comment_create, name="comment_create"),
]