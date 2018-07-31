from django.views.generic import ListView
from apps.common.mixins import AbnormalUserMixin


class SearchView(AbnormalUserMixin, ListView):
    def get_queryset(self):
        obj_list = self.model.objects.all()
        q = self.request.GET.get('q', '')

        if q:
            obj_list = self.model.objects.filter(name__icontains=q)

        return obj_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q','')
        context['obj_list'] = self.get_queryset()
        return context