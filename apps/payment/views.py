from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.conf import settings
from uuid import uuid4

from apps.accounts.models import Artist

from .forms import SponsorForm
from .models import Sponsor


def sponsor_create(request, artist_id):
    artist = get_object_or_404(Artist, id = artist_id)
    merchant_uid = uuid4
    if request.user.is_authenticated:
        user = request.user
        user_name = user.nickname
        email = user.email
        initial = {
            'user': user,
            'user_name': user_name,
            'artist': artist,
            'merchant_uid': merchant_uid,
        }
        is_user = 'true'
    else:
        user = None
        email = 'anonymous@example.com'
        initial = {
            'user': user,
            'artist': artist,
            'merchant_uid': merchant_uid,
        }
        is_user = 'false'
    
    if request.method == 'POST':
        form = SponsorForm(request.POST, initial = initial)
        if form.is_valid():
            form.save()
            return redirect('payment:pay_complete')
    else:
        form = SponsorForm(initial = initial)


    return render(request, 'payment/payment_page.html', {
        'form': form,
        'is_user': is_user,
        'artist': artist,
        'email': email,
        'iamport_shop_id': settings.IAMPORT_SHOP_ID,
        'merchant_uid': merchant_uid,
    })


class PayComplete(TemplateView):
    template_name = 'payment/payment_complete.html'


def sponsor_pay(request, artist_id, merchant_uid):
    if request.user.is_authenticated:
        user_name = request.user.nickname
        email = request.user.email
        user = request.user
    else:
        user_name = 'Anonymous'
        email = 'anonymous@example.com'
        user = None

    sponsor = get_object_or_404(Sponsor, user = user, merchant_uid = merchant_uid, status = 'ready')
    artist = Artist.objects.get(id = artist_id)

    if request.method == 'POST':
        form = SponsorForm(request.POST, instance = sponsor)
        if form.is_valid():
            form.save()
            return redirect('website:home')
        else:
            return redirect('profile')
    else:
        form = SponsorForm(instance = sponsor)
    
    return render(request, 'payment/payment_page.html', {
        'form': form,
        'artist': artist,
        'user_name': user_name,
        'email': email,
        'iamport_shop_id': settings.IAMPORT_SHOP_ID,
        'merchant_uid': sponsor.merchant_uid,
    })

