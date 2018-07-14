from django.db import models
from django.contrib.auth import get_user_model
from apps.accounts.models import Artist
from apps.concert.models import Concert

User = get_user_model()

class Basket(models.Model):
    user = models.ForeignKey(User, verbose_name = '찜한 회원', on_delete = models.CASCADE)
    artist = models.ForeignKey(Artist, verbose_name = '아티스트', blank = True, null = True, on_delete = models.CASCADE, related_name = 'basket_artist')
    concert = models.ForeignKey(Artist, verbose_name = '공연', blank = True, null = True, on_delete = models.CASCADE, related_name = 'basket_concert')


class Review(models.Model):
    user = models.ForeignKey(User, verbose_name = '사용자', on_delete = models.CASCADE)
    artist = models.ForeignKey(Artist, verbose_name = '아티스트', on_delete = models.CASCADE)
    rate = models.IntegerField('별점', choices = ((1,'★'),(2,'★★'),(3,'★★★'),(4,'★★★★'),(5,'★★★★★')))
    description = models.TextField('리뷰')
    is_pay = models.BooleanField('후원 여부', default = False)
    regist_dt = models.DateTimeField('작성 시각', auto_now_add = True)
    like = models.PositiveIntegerField('좋아요', default = 0)

class Answer(models.Model):
    user = models.ForeignKey(User, verbose_name = '사용자', on_delete = models.CASCADE)
    review = models. ForeignKey(Review, verbose_name = '리뷰', on_delete = models.CASCADE)
    description = models.TextField('답변')