from django import forms
from .models import Concert
from apps.common.widgets import NaverMapPointWidget

class ConcertCreateForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = [
            'date',
            'time',
            'location_1',
            'location_2',
            'location_else',
            'description',
            'probability',
        ]
        widgets = {
            'location_2': NaverMapPointWidget(attrs={'width': '100%'}),
            'location_else': forms.TextInput(attrs={'readonly': True}),
            }