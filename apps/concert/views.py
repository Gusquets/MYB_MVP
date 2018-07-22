from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q

from apps.common.mixins import LoginRequiredMixin, ArtistRequiredMixin
from apps.preference.models import Basket
from .forms import ConcertCreateForm
from .models import Concert

class ConcertCreate(LoginRequiredMixin, ArtistRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'concert/concert_create.html'
    form_class = ConcertCreateForm
    success_url = reverse_lazy('concert:concert_list')
    success_message = '성공적으로 공연이 등록되었습니다.'

    name = 'concert_create'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['artist'] = self.request.user.artist
        return context


class ConcertList(ListView):
    model = Concert
    template_name = 'concert/concert_list.html'
    paginate_by = 10

    name = 'concert_list'


    def get_queryset(self):
        obj_list = self.model.objects.all()
        q = self.request.GET.get('q', '')
        date = self.request.GET.get('date', '')
        location = self.request.GET.get('location', '')

        if q:
            obj_list = self.model.objects.filter(Q(artist__name__icontains=q)|Q(date__icontains=date)|Q(location_1__icontains=location))

        return obj_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q', '')
        context['q'] = q
        context['date'] = self.request.GET.get('date', '')
        context['location'] = self.request.GET.get('location', '')
        sort = self.request.GET.get('sorted', '')
        context['sorted'] = sort
        if sort == 'time':
            context['concert_list'] = self.get_queryset().order_by('-id')
        elif sort == 'rate':
            context['concert_list'] = self.get_queryset().order_by('-artist__rate_avg')
        else:
            context['concert_list'] = self.get_queryset()
        if self.request.user.is_authenticated:
            if q:
                context['basket_list'] = Basket.objects.all().filter(user = self.request.user, artist__isnull = True).filter(concert__artist__name__icontains=q)
            else:
                context['basket_list'] = Basket.objects.all().filter(user = self.request.user, artist__isnull = True)
        if sort == 'time':
            context['basket_list'] = context['basket_list'].order_by('-id')
        elif sort == 'rate':
            context['basket_list'] = context['basket_list'].order_by('-concert__artist__rate_avg')
        return context


class ConcertDetail(DetailView, UpdateView):
    template_name = 'concert/concert_detail.html'
    model = Concert
    form_class = ConcertCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.artist.artistimages_set.all()
        context['song_list'] = self.object.concertsonglist_set.all()
        context['review_list'] = self.object.artist.review_set.all()[:3]
        context['view'] = self.request.GET.get('view', '')
        return context