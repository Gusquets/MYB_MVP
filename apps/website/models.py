from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class CSService(models.Model):
    from_email = models.EmailField('문의자 E-mail')
    title = models.CharField('제목', max_length = 100)
    description = models.TextField('내용')

    class Meta:
        verbose_name = '고객 문의'
        verbose_name_plural = '고객 문의'


class Terms(models.Model):
    catogory = models.IntegerField('종류', choices=((1,'이용약관'),(2,'개인정보처리방침')))
    description = RichTextUploadingField('내용')

    class Meta:
        verbose_name = '약관'
        verbose_name_plural = '약관'