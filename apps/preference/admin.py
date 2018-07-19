from django.contrib import admin
from .models import Basket, Review, Answer

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['user', 'artist', 'concert']
    list_display_links = ['user', 'artist', 'concert']
    list_filter = ['artist', 'concert']
    search_fields = ['artist', 'concert']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'artist', 'rate', 'is_pay', 'like']

