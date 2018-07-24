from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from apps.accounts.models import Artist

from .forms import SponsorForm


class SponsorCreate(CreateView):
    template_name = 'payment/sponsor_create.html'
    form_class = SponsorForm
    success_url = reverse_lazy('website:home')

    def get_initial(self):
        pk = self.kwargs['artist_id']
        artist = get_object_or_404(Artist, id = pk)
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            user = None
        initial = {'user': self.request.user, 'artist': artist}
        return initial

    




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
        concert.artist = self.request.user.artist

        concert.save()
        response = super().form_valid(form)

        return response