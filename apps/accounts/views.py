from django.contrib import messages
from django.contrib.auth import get_user_model, login as auth_login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetConfirmView as BasePasswordResetConfirmView, \
    PasswordChangeView as BasePasswordChangeView, PasswordResetView as BasePasswordResetView, login as auth_login2
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, RedirectView, UpdateView, FormView, TemplateView, ListView, DetailView
from django.conf import settings

from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers

from .forms import UserCreateForm, ArtistCreateForm, UserUpdateForm, SetPasswordForm, PasswordChangeForm
from .models import Artist
from apps.common.mixins import LoginRequiredMixin

User = get_user_model()


class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

def login(request):
    providers = []
    for provider in get_providers():
        try:
            provider.social_app = SocialApp.objects.get(provider = provider.id, sites = settings.SITE_ID)
        except SocialApp.DoesNotExist:
            provider.social_app = None
        providers.append(provider)

    return auth_login2(request,
        template_name = 'accounts/login.html',
        extra_context = {'providers' : providers})

class UserCreate(CreateView):
    template_name = 'registration/user_create.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('website:home')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usertype = self.request.GET.get('usertype','')
        if usertype:
            context['usertype'] = usertype
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        user.is_agreed_1 = True
        user.is_agreed_2 = True
        user.save()

        auth_login(self.request, user)
        if self.request.POST.get('usertype') == '2':
            return redirect('artist_create')

        return response

class UserCreateChoice(TemplateView):
    template_name = 'registration/user_create_choice.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class ArtistCreate(CreateView):
    template_name = 'registration/artist_create.html'
    form_class = ArtistCreateForm
    success_url = reverse_lazy('website:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        artist = self.object

        self.request.user.artist = artist
        self.request.user.save()
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


class ArtistList(ListView):
    template_name = 'accounts/artist_list.html'
    paginate_by = 10

    name = 'artist_list'


    def get_queryset(self):
        return Artist.objects.all()


class ArtistDetail(DetailView):
    template_name = 'accounts/artist_detail.html'
    model = Artist


class FindEmail(TemplateView):
    template_name = 'accounts/find_id.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        phone_number = self.request.GET.get('phone_number')
        if User.objects.all().filter(phone_number = phone_number):
            context['result'] = User.objects.all().filter(phone_number = phone_number)
        return context
