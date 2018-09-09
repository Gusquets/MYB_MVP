from django import forms
from .models import Review, Answer


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'rate',
            'description',
        ]

class DeleteForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = []


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = [
            'description',
        ]