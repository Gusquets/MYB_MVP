from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models import Q

from apps.accounts.models import Artist
from apps.concert.models import Concert

from .models import CSService, Terms
from .forms import CSServiceForm

class HomeView(TemplateView):
    template_name = 'website/main.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slider_concert'] = Concert.objects.filter(recommend_yn = True)

        return context


class CSServiceCreateView(SuccessMessageMixin , CreateView):
    model = CSService
    template_name = 'website/cs_create.html'
    form_class = CSServiceForm
    success_url = reverse_lazy('website:home')
    success_message = '문의가 성공적으로 접수되었습니다.'

    name = 'cs_create'


class TermView(TemplateView):
    template_name = 'website/terms.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.path == '/terms/access/':
            category = 1
        elif self.request.path == '/terms/information/':
            category = 2

        context['description'] = Terms.objects.get(category = category).description

        return context


class SearchList(TemplateView):
    template_name = 'website/search_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q', '')
        context['q'] = q
        context['artist_list'] = Artist.objects.all().filter(Q(name__icontains = q) | Q(description__icontains = q))

        context['concert_list'] = Concert.objects.all().filter(Q(date__icontains = q) | Q(time__icontains = q) | Q(description__icontains = q) | Q(location_1__icontains = q) | Q(artist__name__icontains = q))

        return context


