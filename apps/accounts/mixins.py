from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.template.loader import render_to_string
from django.urls import reverse


class LoginRequiredMixin(AccessMixin):
    message_login_required = '로그인이 필요한 기능입니다.'

    def get_login_url(self):
        user = self.request.user
        if not user.is_authenticated:
            login_url = super().get_login_url()
            message = render_to_string('account/messages/login_required.html', context={
                'login_url': login_url,
                'message_login_required': self.message_login_required
            })
            messages.warning(self.request, message, extra_tags='html')
            return self.request.META.get('HTTP_REFERER', '/')
        else:
            return reverse('user_verify')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_verified:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()
