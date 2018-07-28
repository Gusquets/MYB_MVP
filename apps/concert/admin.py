from django.contrib import admin
from .models import Concert, ConcertSongList

@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'location_1', 'artist', 'probability', 'recommend_yn']
    list_display_links = ['id', 'date', 'artist']
    list_filter = ['date', 'location_1', 'recommend_yn']
    search_fields = ['location_1', 'artist__name']


@admin.register(ConcertSongList)
class ConcertSongListAdmin(admin.ModelAdmin):
    list_display = ['id', 'concert', 'name']
    list_display_links = ['concert', 'name']
    list_filter= ['concert']
    search_fields = ['concert']