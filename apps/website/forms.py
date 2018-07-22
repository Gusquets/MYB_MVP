from django import forms
from django.core.mail import EmailMultiAlternatives

from .models import CSService


class CSServiceForm(forms.ModelForm):
    class Meta:
        model = CSService
        fields = '__all__'

    def save(self, commit=True):
        csservice = super().save(commit=True)
        email = EmailMultiAlternatives(subject=self.cleaned_data['title'], body=self.cleaned_data['description'], to=['mybusker@naver.com'], from_email=self.cleaned_data['from_email'])
        email.send()

        return csservice