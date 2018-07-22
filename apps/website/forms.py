from django import forms
from .models import CSService

class CSServiceForm(forms.ModelForm):
    class Meta:
        model = CSService
        fields = '__all__'