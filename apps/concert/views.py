from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from apps.common.mixins import LoginRequiredMixin, ArtistRequiredMixin

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
    template_name = 'concert/concert_list.html'
    paginate_by = 10

    name = 'concert_list'


    def get_queryset(self):
        return Concert.objects.all()


class ConcertDetail(DetailView):
    template_name = 'concert/concert_detail.html'
    model = Concert