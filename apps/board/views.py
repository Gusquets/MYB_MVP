from django.shortcuts import render
from .models import *
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, get_list_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import *

# Create your views here.

def postview(request):
    post = get_list_or_404(ConcertPost.objects.order_by('-created_at'))
    paginator = Paginator(post, 15)

    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    ctx = {
        'posts' : post,
        'page' : paginator,
        'contacts' : contacts,
    }

    return render(request, 'concert_post/post_list.html', ctx)

def detail(request, post_pk):
    post = get_object_or_404(ConcertPost, pk=post_pk)
    comment = Comment.objects.filter(post=post_pk)
    form = CommentForm(initial={'author' : request.session.get('author',None)})
    ctx = {
        'pk' : post.pk,
        'author' : post.author,
        'title' : post.title,
        'content' : post.content,
        'created_at' : post.created_at,
        'comment' : comment,
        'form' : form,
    }
    return render(request, 'concert_post/post_detail.html', ctx)

def create(request):
    if request.method == 'GET':
        form = PostForm(initial={'author': request.session.get('author', None)})

    elif request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            obj = form.save()
            request.session['author'] = form.cleaned_data['author']
            return redirect(obj)

    ctx = {
        'form' : form,
    }
    return render(request, 'concert_post/create.html', ctx)

def comment_create(request, post_pk):
    post = get_object_or_404(ConcertPost, pk=post_pk)
    if request.method == 'GET':
        form = CommentForm

    elif request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.post = post
            obj.save()
            return redirect(obj)

    ctx = {
        'form' : form,
    }

    return render(request, 'concert_post/comment_create.html', ctx)
