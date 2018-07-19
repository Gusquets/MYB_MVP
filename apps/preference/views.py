import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from apps.common.mixins import LoginRequiredMixin
from apps.concert.models import Concert
from apps.accounts.models import Artist
from .models import Basket, Review, Like

@login_required
def like_create(request, pk):
    review = get_object_or_404(Review, id=pk)

    if Like.objects.filter(user = request.user).filter(review = review).exists():
        Like.objects.filter(user = request.user).filter(review = review).delete()
        review.like_count = Like.objects.filter(user = request.user).filter(review = review).count()
        review.save()
        message = '좋아요 취소.'
    else:
        Like.objects.create(user = request.user, review = review)
        review.like_count = Like.objects.filter(user = request.user).filter(review = review).count()
        review.save()
        message = '좋아요.'
    
    context = {'message': message,}

    return HttpResponse(json.dumps(context), content_type="application/json")


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


class MyBasket(TemplateView):
    template_name = 'preference/basket/my_basket.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['concert_list'] = self.request.user.basket_set.all().filter(artist__isnull = True)
        context['artist_list'] = self.request.user.basket_set.all().filter(concert__isnull = True)
        return context


class MyReview(TemplateView):
    template_name = 'preference/review/my_review.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_list'] = Review.objects.filter(user = self.request.user)
        return context