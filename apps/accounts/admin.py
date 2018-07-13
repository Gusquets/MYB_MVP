from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from .models import Artist, ArtistImage, ArtistMovie
User = get_user_model()


class UserCreateAdminForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'email', 'nickname', 'usertype', 'is_staff']
    list_display_links = ['id', 'email', 'nickname']
    list_filter = ['usertype', 'is_active']
    ordering = ['-id']
    search_fields = ['email', 'nickname']
    add_form = UserCreateAdminForm
    add_form_template = 'admin/change_form.html'
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname', 'user_type', 'password1', 'password2'),
        }),
    )
    fieldsets = [
        ('개인정보', {'fields': [
            'nickname',
            'email',
            'phone_number',
            'is_agreed_1',
            'is_agreed_2',
            'regist_dt',
            'artist',
        ]}),
        ('권한', {'fields': (
            'user_type',
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

    def get_user_number(self, artist):
        return len(artist.user_set.all())

    get_user_number.short_description = '회원수'


@admin.register(ArtistImage)
class ArtistImageAdmin(admin.ModelAdmin):
    list_display = ['artist', 'get_image']
    list_display_links = ['artist', 'get_image']
    list_filter = ['artist']

    def get_image(self, image):
        if image.image:
            return mark_safe('<img src="{}" style="width: 75px;">'.format(image.image.url))
        return None
    
    get_image.short_description = '아티스트 사진'


@admin.register(ArtistMovie)
class ArtistMovie(admin.ModelAdmin):
    list_display = ['artist', 'get_movie']
    list_display_links = ['artist', 'get_movie']
    list_filter = ['artist']

    def get_movie(self, movie):
        if movie.movie:
            return mark_safe('<video src="{}" style="width: 75px;"></video>'.format(movie.movie.url))