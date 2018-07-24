import json
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_text
from django.template.loader import render_to_string

from .models import Sponsor

class SponsorForm(forms.ModelForm):
    class Meta:
        model = Sponsor
        fields = [
            'user',
            'artist',
            'user_name',
            'message',
            'amount',
            'pay_type',
            'imp_uid',
            'merchant_uid'
        ]
        widgets = {
            'user': forms.HiddenInput(),
            'artist': forms.HiddenInput(),
            'imp_uid': forms.HiddenInput(),
            'merchant_uid': forms.HiddenInput(),
            'message': forms.Textarea(attrs={'rows': 3})
        }
    
    
    def save(self):
        sponsor = super().save(commit = False)
        sponsor.update()

        return sponsor
