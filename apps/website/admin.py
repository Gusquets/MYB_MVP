from django.contrib import admin
from .models import CSService, Terms


@admin.register(CSService)
class CSServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'from_email', 'title']
    list_display_links = ['title']
    search_fields = ['title', 'from_email']


@admin.register(Terms)
class TermsAdmin(admin.ModelAdmin):
    list_display = ['catogory']