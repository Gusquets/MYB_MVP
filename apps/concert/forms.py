from django import forms
from .models import Concert
from apps.common.widgets import NaverMapPointWidget

class ConcertCreateForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = '__all__'
        widgets = {
            'location_2': NaverMapPointWidget(),
            }