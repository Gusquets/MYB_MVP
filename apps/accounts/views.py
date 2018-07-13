from django.contrib import messages
from django.contrib.auth import get_user_model, login as auth_login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetConfirmView as BasePasswordResetConfirmView, \
    PasswordChangeView as BasePasswordChangeView, PasswordResetView as BasePasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, RedirectView, UpdateView, FormView
from django.conf import settings

from .forms import UserCreateForm, UserUpdateForm, SetPasswordForm, PasswordChangeForm
from .mixins import LoginRequiredMixin

User = get_user_model()


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

class UserCreate(CreateView):
    template_name = 'registration/user_create.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('website:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object

        auth_login(self.request, user)

        return response


class UserUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'registration/user_update.html'
    form_class = UserUpdateForm
    model = User
    success_url = reverse_lazy('profile')
    success_message = '성공적으로 내 정보를 저장했습니다.'

    name = 'user_update'

    def get_object(self, queryset=None):
        return self.request.user


class PasswordResetView(BasePasswordResetView):
    html_email_template_name = 'registration/password_reset_email.html'


class PasswordResetConfirmView(BasePasswordResetConfirmView):
    form_class = SetPasswordForm


class PasswordChangeView(BasePasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('profile')

    name = 'password_change'
