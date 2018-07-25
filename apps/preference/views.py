import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse, reverse_lazy

from apps.common.mixins import LoginRequiredMixin
from apps.concert.models import Concert
from apps.accounts.models import Artist
from apps.payment.models import Sponsor

from .models import Basket, Review, Like, Answer
from .forms import ReviewForm, AnswerForm

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
        context['concert_list'] = self.request.user.basket_set.all().filter(artist__isnull = True)[:6]
        context['artist_list'] = self.request.user.basket_set.all().filter(concert__isnull = True)[:6]
        return context

class MyBasketArtist(LoginRequiredMixin, ListView):
    model = Basket
    template_name = 'preference/basket/my_basket_artist.html'
    paginate_by = 12

    def get_queryset(self):
        return self.request.user.basket_set.all().filter(concert__isnull = True)


class MyBasketConcert(LoginRequiredMixin, ListView):
    model = Basket
    template_name = 'preference/basket/my_basket_concert.html'
    paginate_by = 12

    def get_queryset(self):
        return self.request.user.basket_set.all().filter(artist__isnull = True)


class MyReview(ListView):
    model = Review
    template_name = 'preference/review/my_review.html'
    paginate_by = 10

    name = 'review_list'

    def get_queryset(self):
        if self.request.path == '/preference/my/review/':
            obj_list = Review.objects.filter(user = self.request.user)
        elif self.request.path == '/preference/my/reviewed/':
            obj_list = Review.objects.filter(artist = self.request.user.artist)
        elif self.kwargs['pk']:
            artist = Artist.objects.get(id = self.kwargs['pk'])
            obj_list = Review.objects.filter(artist = artist)
        
        return obj_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.path == '/preference/my/review/':
            context['type'] = 'review'
        elif self.request.path == '/preference/my/reviewed/':
            context['type'] = 'reviewed'
        elif self.kwargs['pk']:
            context['type'] = 'artist'
            context['artist_name'] = Artist.objects.get(id = self.kwargs['pk']).name
        
        return context


class ReviewCreate(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    
    def get_template_names(self):
        if self.request.is_ajax():
            return ['preference/review/_review_create.html']
        return ['preference/review/review_create.html'] 

    def get_success_url(self):
        return reverse('preference:artist_review', kwargs = {'pk': self.object.artist.id})
    
    def form_valid(self, form):
        review = form.save(commit=False)
        artist = Artist.objects.get(id = self.kwargs['artist_id'])
        review.user = self.request.user
        review.user_name = self.request.user.nickname
        review.artist = artist
        review.is_pay = False

        review.save()

        rates_review = Review.objects.all().filter(artist = artist)
        rates_sponsor = Sponsor.objects.all().filter(artist = artist)
        rates_list = []
        for rate  in rates_review:
            rates_list.append(rate.rate)
        for rate in rates_sponsor:
            rates_list.append(rate.rate)
        artist.rate_avg = sum(rates_list) / len(rates_list)
        artist.save()

        response = super().form_valid(form)

        return response


class AnswerCreate(CreateView):
    model = Answer
    form_class = AnswerForm
    
    def get_template_names(self):
        if self.request.is_ajax():
            return ['preference/review/_answer_create.html']
        return ['preference/review/answer_create.html'] 

    def get_success_url(self):
        return reverse_lazy('website:home')
    
    def form_valid(self, form):
        answer = form.save(commit=False)
        review = Review.objects.get(id = self.kwargs['review_id'])
        answer.user = self.request.user
        answer.review = review

        answer.save()

        response = super().form_valid(form)

        return response