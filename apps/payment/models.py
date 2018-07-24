from django.db import models
from django.contrib.auth import get_user_model

from apps.accounts.models import Artist

User = get_user_model()


class Sponsor(models.Model):
    user = models.ForeignKey(User, verbose_name = '후원자', on_delete = models.CASCADE)
    artist = models.ForeignKey(Artist, verbose_name = '아티스트', on_delete = models.CASCADE)
    amount = models.PositiveIntegerField('결제 금액')
    regist_dt = models.DateTimeField(auto_now_add=True)