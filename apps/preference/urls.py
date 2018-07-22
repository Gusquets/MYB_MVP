from django.urls import path
from . import views

app_name = 'preference'
urlpatterns = [
    path('basket/create/concert/<int:id>/', views.basket_create_concert, name = 'basket_create_concert'),
    path('basket/create/artist/<int:id>/', views.basket_create_artist, name = 'basket_create_artist'),

    path('like/<int:pk>/', views.like_create, name = 'like_create'),

    path('my/basket/', views.MyBasket.as_view(), name = 'my_basket'),
    path('my/review/', views.MyReview.as_view(), name = 'my_review'),
    path('my/reviewed/', views.MyReview.as_view(), name = 'my_reviewed'),
    path('artist/review/<int:pk>', views.MyReview.as_view(), name='artist_review'),

    path('review/create/<int:artist_id>/', views.ReviewCreate.as_view(), name = 'review_create'),
]