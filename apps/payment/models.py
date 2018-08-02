import pytz
from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4
from iamport import Iamport
from django.conf import settings
from jsonfield import JSONField
from datetime import datetime
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.safestring import mark_safe
from django.http import Http404

from apps.accounts.models import Artist

User = get_user_model()

def named_property(name):
    def wrap(fn):
        fn.short_description = name
        return property(fn)
    return wrap

def timestamp_to_datetime(timestamp):
    if timestamp:
        tz = pytz.timezone(settings.TIME_ZONE)
        return datetime.utcfromtimestamp(timestamp).replace(tzinfo=tz)
    return None


class Sponsor(models.Model):
    user = models.ForeignKey(User, verbose_name = '후원자', on_delete = models.CASCADE, blank = True, null = True)
    user_name = models.CharField('후원자 이름' , max_length = 50)
    artist = models.ForeignKey(Artist, verbose_name = '아티스트', on_delete = models.CASCADE)
    amount = models.PositiveIntegerField('결제 금액', choices = ((1000,'1,000 원'),(3000,'3,000 원'),(5000,'5,000 원'),(10000,'10,000 원')), default = 3000)
    rate = models.IntegerField('별점', choices = ((0,'☆☆☆☆☆'),(1,'★☆☆☆☆'),(2,'★★☆☆☆'),(3,'★★★☆☆'),(4,'★★★★☆'),(5,'★★★★★')), default = 5)
    message = models.TextField('함께 전할 메세지', blank = True, null = True)
    pay_type = models.CharField('결제수단', max_length = 20, choices = (('html5_inicis','카드결제'),('kakaopay','카카오페이')), default = 'html5_inicis')
    merchant_uid = models.UUIDField('거래 ID')
    imp_uid = models.CharField('아임포트 거래 ID', max_length = 100, blank = True)
    status = models.CharField('결제 상태', max_length = 9, choices = (
        ('ready', '미결제'),
        ('paid', '결제완료'),
        ('cancelled', '결제취소'),
        ('failed', '결제실패'),
    ), default = 'ready', db_index = True)
    meta = JSONField(blank = True, default = {})
    regist_dt = models.DateTimeField(auto_now_add=True)

    is_ready = property(lambda self: self.status == 'ready')
    is_paid = property(lambda self: self.status == 'paid')
    is_paid_ok = property(lambda self: self.status == 'paid' and self.amount == self.meta.get('amount'))
    is_cancelled = property(lambda self: self.status == 'cancelled')
    is_failed = property(lambda self: self.status == 'failed')

    receipt_url = named_property('영수증')(lambda self: self.meta.get('receipt_url'))
    cancel_reason = named_property('취소이유')(lambda self: self.meta.get('cancel_reason'))
    fail_reason = named_property('실패이유')(lambda self: self.meta.get('fail_reason', ''))

    paid_at = named_property('결제일시')(lambda self: timestamp_to_datetime(self.meta.get('paid_at')))
    failed_at = named_property('실패일시')(lambda self: timestamp_to_datetime(self.meta.get('failed_at')))
    cancelled_at = named_property('취소일시')(lambda self: timestamp_to_datetime(self.meta.get('cancelled_at')))

    @named_property('영수증 링크')
    def receipt_link(self):
        if self.is_paid_ok and self.receipt_url:
            return mark_safe('<a href="{0}" target="_blank">영수증</a>'.format(self.receipt_url))

    class Meta:
        verbose_name = '후원'
        verbose_name_plural = '후원'

    @property
    def api(self):
        return Iamport(settings.IAMPORT_API_KEY, settings.IAMPORT_API_SECRET)
    
    def update(self, commit = True, meta = None):
        if self.imp_uid:
            try:
                self.meta = meta or self.api.find(imp_uid=self.imp_uid)
            except Iamport.HttpError:
                raise Http404('Not found {}'.format(self.imp_uid))
            assert str(self.merchant_uid) == self.meta['merchant_uid']
            self.status = self.meta['status']

            if self.status == 'paid':
                assert self.amount == self.meta['amount']
        if commit:
            self.save()
    
    def cancel(self, reason=None, commit=True):
        try:
            meta = self.api.cancel(reason, imp_uid=self.imp_uid)
            assert str(self.merchant_uid) == self.meta['merchant_uid']
            self.update(commit=commit, meta=meta)
        except Iamport.ResponseError as e:
            self.update(commit=commit)
        if commit:
            self.save()