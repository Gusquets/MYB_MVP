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
from .models import Artist, ArtistImages
from apps.common.mixins import LoginRequiredMixin
from apps.preference.models import Basket, Review

User = get_user_model()


class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basket_concert'] = Basket.objects.filter(user = self.request.user, artist__isnull = True).order_by('-id')[:2]
        context['basket_artist'] = Basket.objects.filter(user = self.request.user, concert__isnull = True).order_by('-id')[:2]
        context['review_list'] = Review.objects.filter(user = self.request.user).order_by('-id')[:3]
        return context

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
    success_url = reverse_lazy('user_create_complete')
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
    success_url = reverse_lazy('user_create_complete')

    def form_valid(self, form):
        response = super().form_valid(form)
        artist = self.object

        self.request.user.artist = artist

        files = self.request.FILES.getlist('image')
        for f in files:
            ArtistImages.objects.create(artist = artist, image = f)
        
        self.request.user.save()
        return response


class UserCreateComplete(TemplateView):
    template_name = 'registration/user_create_complete.html'


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
    model = Artist
    template_name = 'accounts/artist_list.html'
    paginate_by = 12

    name = 'artist_list'

    def get_queryset(self):
        obj_list = self.model.objects.all()
        q = self.request.GET.get('q', '')

        if q:
            obj_list = self.model.objects.filter(name__icontains=q)

        return obj_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q','')
        sort = self.request.GET.get('sorted', '')
        context['sorted'] = sort
        if sort == 'time':
            context['artist_list'] = self.get_queryset().order_by('-id')
        elif sort == 'rate':
            context['artist_list'] = self.get_queryset().order_by('-rate_avg')
        else:
            context['artist_list'] = self.get_queryset()
        q = self.request.GET.get('q', '')
        if q:
            context['basket_list'] = Basket.objects.all().filter(user = self.request.user, concert__isnull = True).filter(artist__name__icontains=q)
        else:
            context['basket_list'] = Basket.objects.all().filter(user = self.request.user, concert__isnull = True)
        if sort == 'time':
            context['basket_list'] = context['basket_list'].order_by('-id')
        elif sort == 'rate':
            context['basket_list'] = context['basket_list'].order_by('-artist__rate_avg')
        return context


class ArtistDetail(DetailView):
    template_name = 'accounts/artist_detail.html'
    model = Artist

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['concert_count'] = len(self.object.concert_set.all())
        context['images'] = self.object.artistimages_set.all()
        context['concert_list'] = self.object.concert_set.all()[:2]
        context['review_list'] = self.object.review_set.all()[:3]
        return context


class FindEmail(TemplateView):
    template_name = 'accounts/find_id.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        phone_number = self.request.GET.get('phone_number')
        if User.objects.all().filter(phone_number = phone_number):
            context['result'] = User.objects.all().filter(phone_number = phone_number)
        return context
