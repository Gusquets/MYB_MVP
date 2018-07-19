from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from .models import Artist, ArtistImages
User = get_user_model()


class UserCreateAdminForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'email', 'nickname', 'usertype', 'is_staff']
    list_display_links = ['id', 'email', 'nickname']
    list_filter = ['usertype', 'is_active', 'artist']
    ordering = ['-id']
    search_fields = ['email', 'nickname']
    add_form = UserCreateAdminForm
    add_form_template = 'admin/change_form.html'
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname', 'usertype', 'password1', 'password2'),
        }),
    )
    fieldsets = [
        ('개인정보', {'fields': [
            'nickname',
            'email',
            'phone_number',
            'is_agreed_1',
            'is_agreed_2',
            'artist',
        ]}),
        ('권한', {'fields': (
            'usertype',
            'is_active',
            'is_staff',
            'is_superuser',
            'password',
        )})
    ]


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_user_number', 'is_verify', 'regist_dt']
    list_display_links = ['id', 'name']
    list_filter = ['is_verify']
    fieldsets = [
        ('아티스트 정보', {'fields': [
            'name',
            'description',
        ]}),
        ('아티스트 소개', {'fields': [
            'image',
            'movie_1',
            'movie_2',
            'movie_3',
            'social_fb',
            'social_insta',
            'social_youtube',
        ]}),
        ('권한', {'fields': (
            'is_verify',
        )})
    ]


    def get_user_number(self, artist):
        return len(artist.user_set.all())

    get_user_number.short_description = '회원수'


@admin.register(ArtistImages)
class ArtistImagesAdmin(admin.ModelAdmin):
    list_display = ['artist']
    list_display_links = ['artist']
    search_fields = ['artist']