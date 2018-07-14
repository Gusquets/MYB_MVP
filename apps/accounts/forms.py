from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm as BaseSetPasswordForm, PasswordChangeForm as BasePasswordChangeForm
from django.utils.safestring import mark_safe

from apps.common.validators import validate_password
from .models import Artist

User = get_user_model()


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput(attrs={'placeholder': '6~32자리의 영문, 숫자를 혼합하여 사용하세요.'}), validators=[validate_password])
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput(attrs={'placeholder': ''}))

    current_site = None

    class Meta:
        model = User
        fields = [
            'email',
            'nickname',
            'phone_number',
            'password1',
            'password2',
            'is_agreed_1',
            'is_agreed_2',
            'usertype',
        ]
        help_texts = {
            'email': 'MYBUSKER의 ID로 사용할 이메일 주소를 입력해주세요.<br>가입하신 이메일 주소는 변경할 수 없습니다.',
            'nickname': '닉네임은 언제든지 변경할 수 있습니다.'
        }
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'example@email.com'}),
            'nickname': forms.TextInput(attrs={'placeholder': 'Nickname'}),
            'usertype': forms.HiddenInput()
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user
class ArtistCreateForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = '__all__'


class UserUpdateForm(forms.ModelForm):
    email_readonly = forms.CharField(label='이메일', widget=forms.TextInput(attrs={'readonly': ''}))

    class Meta:
        model = User
        fields = [
            'email_readonly',
            'phone_number',
            'nickname',
        ]
        labels = {
            'nickname': '닉네임 변경',
        }

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email_readonly'].initial = self.instance.email

    def save(self, commit=True):
        instance = super(UserUpdateForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance


class SetPasswordForm(BaseSetPasswordForm):
    new_password1 = forms.CharField(
        label='새 비밀번호',
        widget=forms.PasswordInput(attrs={'placeholder': '6~32자리의 영문, 숫자를 혼합하여 사용하세요.'}),
        validators=[validate_password],
        strip=False,
    )
    new_password2 = forms.CharField(
        label='새 비밀번호 확인',
        strip=False,
        widget=forms.PasswordInput,
    )


class PasswordChangeForm(BasePasswordChangeForm):
    old_password = forms.CharField(
        label='기존 비밀번호',
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True}),
    )
    new_password1 = forms.CharField(
        label='새 비밀번호',
        widget=forms.PasswordInput(attrs={'placeholder': '6~32자리의 영문, 숫자를 혼합하여 사용하세요.'}),
        strip=False,
        validators=[validate_password],
    )
    new_password2 = forms.CharField(
        label='새 비밀번호 확인',
        strip=False,
        widget=forms.PasswordInput,
    )
