from django import forms
from .models import Concert
from apps.common.widgets import NaverMapPointWidget, NaverMapPointWidget2, CalendarWidget

class ConcertCreateForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = [
            'date',
            'start_time',
            'end_time',
            'location_1',
            'location_2',
            'location_else',
            'description',
            'rain_cancel',
            'site_reserved',
        ]
        widgets = {
            'date': CalendarWidget(),
            'location_2': NaverMapPointWidget(attrs={'width': '100%'}),
            'location_else': forms.TextInput(attrs={'readonly': True}),
            'rain_cancel': forms.RadioSelect(),
            'site_reserved': forms.RadioSelect(),
            }


class ConcertCreateForm2(forms.ModelForm):
    class Meta:
        model = Concert
        fields = [
            'date',
            'start_time',
            'end_time',
            'location_1',
            'location_2',
            'location_else',
            'description',
            'rain_cancel',
            'site_reserved',
        ]
        widgets = {
            'date': CalendarWidget(),
            'location_2': NaverMapPointWidget2(attrs={'width': '100%'}),
            'location_else': forms.TextInput(attrs={'readonly': True}),
            'rain_cancel': forms.RadioSelect(),
            'site_reserved': forms.RadioSelect(),
            }