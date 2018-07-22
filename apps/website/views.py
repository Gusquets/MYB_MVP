from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from .models import CSService
from .forms import CSServiceForm

class HomeView(TemplateView):
    template_name = 'website/main.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CSServiceCreateView(SuccessMessageMixin , CreateView):
    model = CSService
    template_name = 'website/cs_create.html'
    form_class = CSServiceForm
    success_url = reverse_lazy('website:home')
    success_message = '문의가 성공적으로 접수되었습니다.'

    name = 'cs_create'