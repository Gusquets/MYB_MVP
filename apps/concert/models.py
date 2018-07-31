from django.db import models
from apps.accounts.models import Artist
from django.core.validators import MaxValueValidator


class Concert(models.Model):
    date = models.DateField('공연 날짜')
    start_time = models.TimeField('공연 시작 시간')
    end_time = models.TimeField('공연 종료 시간')
    location_1 = models.CharField('공연 장소 1', max_length = 50, choices = (('신촌','신촌'),('홍대','홍대'),('강남','강남'),('이태원','이태원'),('건대','건대'),('한강','한강'),('그외','그외')))
    location_2 = models.CharField('공연 장소 2', max_length = 100)
    location_else = models.CharField('공연장소 그외', max_length = 50, default = '해당없음')
    artist = models.ForeignKey(Artist, verbose_name = '아티스트', on_delete = models.CASCADE)
    description = models.TextField('공연 설명', blank = True, null = True)
    probability = models.PositiveIntegerField('공연 확률', validators = [MaxValueValidator(100)], default = 100)
    rain_cancel = models.BooleanField('우천시 취소여부', choices = ((True,'네'),(False,'아니오')), default = False)
    site_reserved = models.BooleanField('장소 예약여부', choices = ((True,'네'),(False,'아니오')), default = False)
    recommend_yn = models.BooleanField('추천 여부', default = False)

    class Meta:
        verbose_name = '공연 정보'
        verbose_name_plural = '공연 정보'

    def __str__(self):
        return str(self.artist) + '/' + str(self.date)

class ConcertSongList(models.Model):
    concert = models.ForeignKey(Concert, verbose_name = '공연', on_delete = models.CASCADE)
    name = models.CharField('곡 제목', max_length = 50)
    info = models.CharField('곡 정보' , max_length = 50)

    class Meta:
        verbose_name ='공연 곡'
        verbose_name_plural = '공연 곡'

    def __str__(self):
        return self.name