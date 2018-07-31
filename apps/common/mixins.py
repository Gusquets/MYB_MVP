from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.template.loader import render_to_string
from django.urls import reverse
from django.shortcuts import redirect


class LoginRequiredMixin(AccessMixin):
    message_login_required = '로그인이 필요한 기능입니다.'

    def get_login_url(self):
        user = self.request.user
        if not user.is_authenticated:
            login_url = super().get_login_url()
            message = render_to_string('common/messages/login_required.html', context={
                'login_url': login_url,
                'message_login_required': self.message_login_required
            })
            messages.warning(self.request, message, extra_tags='html')
            return self.request.META.get('HTTP_REFERER', '/')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.usertype == 2 and not request.user.artist:
            return redirect('artist_needed')
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()


class ArtistRequiredMixin(AccessMixin):
    message_artist_required = '아티스트 회원만 접근이 가능합니다.'

    def get_login_url(self):
        user = self.request.user
        if not user.is_authenticated or not user.usertype == 2:
            login_url = super().get_login_url()
            message = render_to_string('common/messages/artist_required.html', context={
                'login_url': login_url,
                'message_artist_required': self.message_artist_required,
            })
            messages.warning(self.request, message, extra_tags = 'html')
            return self.request.META.get('HTTP_REFERER', '/')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.usertype == 2 and not request.user.artist:
            return redirect('artist_needed')
        if request.user.is_authenticated and request.user.is_authenticated and request.user.usertype == 2:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()

class AbnormalUserMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.usertype == 2 and not request.user.artist:
            return redirect('artist_needed')
        return super().dispatch(request, *args, **kwargs)