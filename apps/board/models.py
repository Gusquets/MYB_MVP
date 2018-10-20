from django.db import models
from django.utils import timezone
from django.urls import reverse_lazy
from django.conf import settings

# Create your models here.

class ConcertPost(models.Model):
    login_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = '회원이름', on_delete=models.CASCADE, blank=True, null=True, related_name="login_user")
    author = models.CharField('작성자', max_length=50)
    title = models.CharField('제목', max_length=100)
    content = models.TextField('내용')
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, auto_now=True)

    def __str__(self):
        return f'Title: {self.title}, Author: {self.author}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.modified = timezone.now()
        return super(ConcertPost, self).save(*args, **kwargs)


    def get_absolute_url(self):
        url = reverse_lazy('concert_post:concert_post_list')
        return url

    def return_comment(self):
        comments = Comment.objects.filter(post=self.pk)
        return comments

class Comment(models.Model):
    login_user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name = '회원이름', on_delete=models.CASCADE, blank=True, null=True, related_name='comment_login_user')
    post = models.ForeignKey(ConcertPost, on_delete=models.CASCADE)
    author = models.CharField('작성자', max_length=50)
    content = models.CharField('내용', max_length= 200)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)

    def get_absolute_url(self):
        post = self.post
        url = reverse_lazy('concert_post:concert_post_detail', kwargs={'post_pk': post.pk})
        return url

