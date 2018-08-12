import json
from django.http import HttpResponse
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
from django.views.decorators.csrf import csrf_exempt

from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers

from .forms import UserCreateForm, ArtistCreateForm, UserUpdateForm, SetPasswordForm, PasswordChangeForm
from .models import Artist, ArtistImages, ArtistImagesTemp
from apps.common.mixins import LoginRequiredMixin, ArtistRequiredMixin, AbnormalUserMixin
from apps.preference.models import Basket, Review
from apps.payment.models import Sponsor

User = get_user_model()


class Profile(LoginRequiredMixin, TemplateView):

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        if self.request.user.usertype == 2:
            return ['accounts/profile_artist.html']
        else:
            return ['accounts/profile.html']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basket_concert'] = Basket.objects.filter(user = self.request.user, artist__isnull = True).order_by('-id')[:2]
        context['basket_artist'] = Basket.objects.filter(user = self.request.user, concert__isnull = True).order_by('-id')[:2]
        context['review_list'] = Review.objects.filter(user = self.request.user).order_by('-id')[:3]
        context['reviewed_list'] = Review.objects.filter(artist = self.request.user.artist).order_by('-id')[:3]
        context['reviewed_count'] = len(Review.objects.filter(artist = self.request.user.artist).order_by('-id'))
        context['sponsor_list'] = Sponsor.objects.filter(user = self.request.user, status = 'paid').order_by('-regist_dt')[:3]
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

class UserCreate(AbnormalUserMixin,CreateView):
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

class UserCreateChoice(AbnormalUserMixin, TemplateView):
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
        if artist.movie_1:
            if not artist.movie_1.find('embed') > 0:
                index = artist.movie_1.find('.be')
                movie_id = artist.movie_1[index+4:]
                artist.movie_1 = "https://www.youtube.com/embed/" + movie_id
        if artist.movie_2:
            if not artist.movie_2.find('embed') > 0:
                index = artist.movie_2.find('.be')
                movie_id = artist.movie_2[index+4:]
                artist.movie_2 = "https://www.youtube.com/embed/" + movie_id
        if artist.movie_3:
            if not artist.movie_3.find('embed') > 0:
                index = artist.movie_3.find('.be')
                movie_id = artist.movie_3[index+4:]
                artist.movie_3 = "https://www.youtube.com/embed/" + movie_id

        self.request.user.artist = artist
        while True:
            images = ArtistImagesTemp.objects.filter(user = self.request.user)
            if images:
                break;
        artist.image = ArtistImagesTemp.objects.filter(user = self.request.user).first().image
        for f in images:
            ArtistImages.objects.create(artist = artist, image = f.image)
        
        artist.save()
        
        self.request.user.save()
        return response

@csrf_exempt
def artist_image_temp(request):
    user = User.objects.get(id = request.POST.get('user_id'))
    ArtistImagesTemp.objects.create(user = user, image = request.FILES.get('image'))

    context = {'message': '사진이 등록되었습니다.'}

    return HttpResponse(json.dumps(context), content_type="application/json")

@csrf_exempt
def artist_image_delete(request):
    image_id = request.POST.get('id')

    ArtistImages.objects.filter(id = image_id).delete()

    context = {'message': '사진이 삭제되었습니다.'}

    return HttpResponse(json.dumps(context), content_type="application/json")

class UserCreateComplete(AbnormalUserMixin, TemplateView):
    template_name = 'registration/user_create_complete.html'


class PasswordResetView(BasePasswordResetView):
    html_email_template_name = 'registration/password_reset_email.html'


class PasswordResetConfirmView(BasePasswordResetConfirmView):
    form_class = SetPasswordForm



class ArtistList(AbnormalUserMixin, ListView):
    model = Artist
    template_name = 'accounts/artist_list.html'
    paginate_by = 10

    name = 'artist_list'

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        sort = self.request.GET.get('sorted', '')

        if self.request.path == '/accounts/artist/list/basket/':
            if self.request.user.is_authenticated:
                obj_list = Basket.objects.all().filter(user = self.request.user, concert__isnull = True)
                if q:
                    obj_list = obj_list.filter(artist__name__icontains=q)
                if sort == 'time':
                    obj_list = obj_list.order_by('-id')
                elif sort == 'rate':
                    obj_list = obj_list.order_by('-artist__rate_avg')
            else:
                obj_list = None
        else:
            obj_list = self.model.objects.all()
            if q:
                obj_list = obj_list.filter(name__icontains=q)

            if sort == 'time':
                obj_list = obj_list.order_by('-id')
            elif sort == 'rate':
                obj_list = obj_list.order_by('-rate_avg')

        return obj_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q','')
        context['sorted'] = self.request.GET.get('sorted', '')
        return context


class ArtistDetail(AbnormalUserMixin, DetailView):
    template_name = 'accounts/artist_detail.html'
    model = Artist

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['concert_count'] = len(self.object.concert_set.all())
        context['images'] = self.object.artistimages_set.all()
        context['concert_list'] = self.object.concert_set.all()[:2]
        context['review_list'] = self.object.review_set.all().order_by('-id')[:3]
        context['view'] = self.request.GET.get('view', '')
        return context


class ArtistUpdate(ArtistRequiredMixin, UpdateView):
    template_name = 'accounts/artist_update.html'
    model = Artist
    form_class = ArtistCreateForm
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        i = 1
        for image in self.object.artistimages_set.all():
            context_name = 'url_'+str(i)
            context[context_name] = image
            i += 1
        context['images_count'] = len(self.object.artistimages_set.all())
        context['images_temp_id'] = ArtistImagesTemp.objects.filter(user = self.request.user).order_by('-id').first().id
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        artist = self.object

        images_temp_id = self.request.POST.get('images_temp_id')
        if ArtistImagesTemp.objects.filter(user = self.request.user, id__gt = images_temp_id).exists():
            images = ArtistImagesTemp.objects.filter(user = self.request.user, id__gt = images_temp_id)
            for f in images:
                ArtistImages.objects.create(artist = artist, image = f.image)
                
        images = self.object.artistimages_set.all().order_by('id')

        if len(images) > 5:
            while len(images) > 5:
                images.first().delete()
                images = self.object.artistimages_set.all().order_by('id')

        return response



class FindEmail(TemplateView):
    template_name = 'accounts/find_id.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        phone_number = self.request.GET.get('phone_number','')
        if phone_number:
            context['result_step'] = True   
            if User.objects.all().filter(phone_number = phone_number):
                context['result'] = User.objects.all().get(phone_number = phone_number).email
        return context


class ArtistNeeded(TemplateView):
    template_name = 'accounts/artist_needed.html'


class ArtistLanding(DetailView):
    template_name = 'accounts/artist_landing.html'
    model = Artist

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['concert_count'] = len(self.object.concert_set.all()) 
        return context
    
