from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q

from apps.common.mixins import LoginRequiredMixin, ArtistRequiredMixin, AbnormalUserMixin
from apps.preference.models import Basket
from apps.accounts.models import Artist
from .forms import ConcertCreateForm, ConcertCreateForm2
from .models import Concert

class ConcertCreate(LoginRequiredMixin, ArtistRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'concert/concert_create.html'
    form_class = ConcertCreateForm
    success_url = reverse_lazy('concert:concert_create_complete')
    success_message = '성공적으로 공연이 등록되었습니다.'

    name = 'concert_create'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['artist'] = self.request.user.artist
        return context
    
    def form_valid(self, form):
        concert = form.save(commit=False)
        if not concert.location_1 == '그외':
            concert.location_else = '해당없음'
        concert.artist = self.request.user.artist

        concert.save()
        response = super().form_valid(form)

        return response


class ConcertCreateComplete(AbnormalUserMixin, TemplateView):
    template_name = 'concert/concert_create_complete.html'


class ConcertList(AbnormalUserMixin, ListView):
    model = Concert
    template_name = 'concert/concert_list.html'
    paginate_by = 10

    name = 'concert_list'

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        sort = self.request.GET.get('sorted', '')

        if self.request.path == '/concert/list/basket/':
            if self.request.user.is_authenticated:
                obj_list = Basket.objects.all().filter(user = self.request.user, artist__isnull = True)
                if q:
                    obj_list = obj_list.filter(Q(concert__artist__name__icontains=q) | Q(concert__location_1__icontains=q))
                if sort == 'time':
                    obj_list = obj_list.order_by('-concert__date')
                elif sort == 'rate':
                    obj_list = obj_list.order_by('-concert__artist__rate_avg')
            else:
                obj_list = None
        elif self.kwargs.get('pk',''):
            artist = Artist.objects.get(id = self.kwargs['pk'])
            obj_list = self.model.objects.filter(artist = artist)
            if q:
                obj_list = obj_list.filter(Q(artist__name__icontains=q) | Q(location_1__icontains=q))
            if sort == 'time':
                obj_list = obj_list.order_by('-date')

        else:
            obj_list = self.model.objects.all()
            if q:
                obj_list = obj_list.filter(Q(artist__name__icontains=q) | Q(location_1__icontains=q))

            if sort == 'time':
                obj_list = obj_list.order_by('-date')
            elif sort == 'rate':
                obj_list = obj_list.order_by('-artist__rate_avg')

        return obj_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['date'] = self.request.GET.get('date', '')
        context['location'] = self.request.GET.get('location', '')
        context['sorted'] = self.request.GET.get('sorted', '')
        context['page'] = self.request.GET.get('page','')
        if self.kwargs.get('pk',''):
            context['list_artist'] = Artist.objects.get(id = self.kwargs['pk'])
        if self.request.path.find('movie') > 0:
            context['movie'] = True
        if self.request.path.find('basket') > 0:
            context['basket'] = True

        return context


class ConcertDetail(AbnormalUserMixin, DetailView, UpdateView):
    template_name = 'concert/concert_detail.html'
    model = Concert
    form_class = ConcertCreateForm2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.artist.artistimages_set.all()
        context['song_list'] = self.object.concertsonglist_set.all()
        context['review_list'] = self.object.artist.review_set.all()[:3]
        context['view'] = self.request.GET.get('view', '')
        return context