from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter, get_adapter as get_account_adapter
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django import forms

User = get_user_model()

class AccountAdapter(DefaultAccountAdapter):
    error_messages = {
        'username_blacklisted':
            _('Username can not be used. Please use other username.'),
        'username_taken':
        AbstractUser._meta.get_field('username').error_messages['unique'],
        'too_many_login_attempts':
            _('Too many failed login attempts. Try again later.'),
        'email_taken':
            _("A user is already registered with this e-mail address."),
        'nickname_taken':
            _("해당 닉네임이 이미 사용중입니다."),
        'phone_number_taken':
            _("해당 휴대폰번호는 이미 등록된 번호입니다."),
    }

    def validate_unique_nickname(self, nickname):
        if User.objects.get(nickname = nickname).exists():
            raise forms.ValidationError(self.error_messages['nickname_taken'])
        return nickname
    
    def validate_unique_phone_number(self, phone_number):
        if User.objects.get(phone_number = phone_number).exists():
            raise forms.ValidationError(self.error_messages['phone_number_taken'])
        return phone_number
    

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    error_messages = {
        'email_taken':
            _("An account already exists with this e-mail address."
            " Please sign in to that account first, then connect"
            " your %s account."),
        'nickname_taken':
            _("해당 닉네임은 이미 사용중입니다."),
        'phone_number_taken':
            _("해당 휴대폰 번호는 이미 사용중입니다."),
    }

    def validate_unique_nickname(self, nickname):
        if User.objects.filter(nickname = nickname).exists():
            raise forms.ValidationError(self.error_messages['nickname_taken'])
        return nickname
    
    def validate_unique_phone_number(self, phone_number):
        if User.objects.filter(phone_number = phone_number).exists():
            raise forms.ValidationError(self.error_messages['phone_number_taken'])
        return phone_number

    def save_user(self, request, sociallogin, form=None, commit=True):
        u = sociallogin.user
        u.set_unusable_password()
        if form:
            get_account_adapter().save_user(request, u, form, commit)
        else:
            get_account_adapter().populate_username(request, u, commit)
        sociallogin.save(request)
        return u