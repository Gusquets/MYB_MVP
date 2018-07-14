from django import forms
from .models import Concert

class ConcertCreateForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = '__all__'