from django.db import models

class CSService(models.Model):
    from_email = models.EmailField('문의자 E-mail')
    title = models.CharField('제목', max_length = 100)
    description = models.TextField('내용')

    class Meta:
        verbose_name = '고객 문의'
        verbose_name_plural = '고객 문의'