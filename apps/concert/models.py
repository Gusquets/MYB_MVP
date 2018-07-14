from django.db import models
from apps.accounts.models import Artist


class Concert(models.Model):
    date = models.DateField('공연 날짜')
    time = models.TimeField('공연 시간')
    location_1 = models.CharField('공연 장소 1', max_length = 50, choices = (('신촌','신촌'),('홍대','홍대'),('강남','강남'),('이태원','이태원'),('건대','건대'),('한강','한강'),('그외','그외')))
    location_2 = models.CharField('공연 장소 2', max_length = 100)
    artist = models.ForeignKey(Artist, verbose_name = '아티스트', on_delete = models.CASCADE)
    description = models.TextField('공연 설명')
    probability = models.IntegerField('공영 확률')

    class Meta:
        verbose_name = '공연 정보'
        verbose_name_plural = '공연 정보'

class ConcertSongList(models.Model):
    concert = models.ForeignKey(Concert, verbose_name = '공연', on_delete = models.CASCADE)
    name = models.CharField('곡 제목', max_length = 50)