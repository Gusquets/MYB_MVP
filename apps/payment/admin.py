from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Sponsor


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'artist', 'amount', 'status_html', 'paid_at', 'receipt_link']
    list_display_links = ['id', 'user', 'artist']
    search_fields = ['artist']
    list_filter = ['amount', 'status']
    actions = ['do_update', 'do_cancel']

    def do_update(self, request, queryset):
        total = queryset.count()
        if total > 0:
            for order in queryset:
                order.update()
            self.message_user(request, '{}건의 후원 정보를 갱신했습니다.'.format(total))
        else:
            self.message_user(request, '갱신할 후원정보가 없습니다.')
    do_update.short_description = '선택된 후원들의 정보 갱신하기'

    def do_cancel(self, request, queryset):
        queryset = queryset.filter(status='paid')
        total = queryset.count()
        if total > 0:
            for order in queryset:
                order.cancel()
            self.message_user(request, '{}건의 후원을 취소했습니다.'.format(total))
        else:
            self.message_user(request, '취소할 후원이 없습니다.')
    do_cancel.short_description = '선택된 후원에 대해 결제취소요청하기'

    def status_html(self, sponsor):
        if sponsor.status == 'ready':
            html = mark_safe('<span style="color: green;">{}</span>'.format('미결제'))
        elif sponsor.status == 'paid':
            html = mark_safe('<span style="color: red;">{}</span>'.format('결제완료'))
        elif sponsor.status == 'cancelled':
            html = mark_safe('<span style="color: blue;">{}</span>'.format('결제취소'))
        else:
            html = mark_safe('<span>{}</span>'.format('결제실패'))

        return html
