from django import forms
from .models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = ConcertPost
        fields = ['author', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'content']