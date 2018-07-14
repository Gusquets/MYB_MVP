import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from apps.common.mixins import LoginRequiredMixin
from apps.concert.models import Concert
from apps.accounts.models import Artist
from .models import Basket

@login_required
def basket_create_concert(request, id):
    concert = get_object_or_404(Concert, id=id)

    if Basket.objects.filter(user = request.user).filter(concert = concert).exists():
        message = '이미 찜하였습니다.'
    else:
        Basket.objects.create(user = request.user, concert = concert)
        message = '찜하였습니다.'
    
    context = {'message': message,}

    return HttpResponse(json.dumps(context), content_type="application/json")

@login_required
def basket_create_artist(request, id):
    artist = get_object_or_404(Artist, id=id)

    if Basket.objects.filter(user = request.user).filter(artist = artist).exists():
        message = '이미 찜하였습니다.'
    else:
        Basket.objects.create(user = request.user, artist = artist)
        message = '찜하였습니다.'
    
    context = {'message': message,}

    return HttpResponse(json.dumps(context), content_type="application/json")
