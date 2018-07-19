from django.contrib import admin
from .models import Basket, Review, Answer, Like

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['user', 'artist', 'concert']
    list_display_links = ['user', 'artist', 'concert']
    list_filter = ['artist', 'concert']
    search_fields = ['artist', 'concert']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'artist', 'rate', 'is_pay']
    list_display_links = ['user', 'artist']
    list_filter = ['rate', 'is_pay']
    search_fields = ['artist']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'review']
    search_fields = ['user']




