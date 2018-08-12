from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import SetPasswordForm as BaseSetPasswordForm, PasswordChangeForm as BasePasswordChangeForm
from django.utils.safestring import mark_safe
from allauth.socialaccount.forms import SignupForm as AllauthSignupForm
from allauth.socialaccount.adapter import get_adapter

from apps.common.validators import validate_password, PhoneNumberValidator
from .models import Artist

User = get_user_model()


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput(attrs={'placeholder': '비밀번호 입력(8자리 이상, 숫자 + 영문)'}), validators=[validate_password])
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput(attrs={'placeholder': '비밀번호 확인'}))

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
            'email': forms.EmailInput(attrs={'placeholder': '이메일'}),
            'nickname': forms.TextInput(attrs={'placeholder': '마이버스커에서 사용할 닉네임'}),
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
        fields = [
            'name',
            'description',
            'movie_1',
            'movie_2',
            'movie_3',
            'social_fb',
            'social_insta',
            'social_youtube',
        ]
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 3,
            }),
        }


class SocialSignupForm(AllauthSignupForm):
    nickname = forms.CharField(label = '닉네임', required=True, widget = forms.TextInput(attrs={'autocomplete': 'off'}))
    email = forms.EmailField(label = 'E-mail', required=True, widget = forms.EmailInput())
    phone_number = forms.CharField(label = '휴대폰 번호', max_length=11, required=True, validators=[PhoneNumberValidator()])

    def save(self, request):
        adapter = get_adapter(request)
        user = adapter.save_user(request, self.sociallogin, form=self, commit=False)
        user.phone_number = self.cleaned_data['phone_number']
        user.nickname = self.cleaned_data['nickname']
        user.is_agreed_1 = True
        user.is_agreed_2 = True

        user.save()
        self.custom_signup(request, user)
        return user

    def clean_nickname(self):
        value = self.cleaned_data['nickname']
        if value:
            value = self.validate_unique_nickname(value)
        return value

    def clean_phone_number(self):
        value = self.cleaned_data['phone_number']
        if value:
            value = self.validate_unique_phone_number(value)
        return value

    def validate_unique_nickname(self, value):
        try:
            return get_adapter().validate_unique_nickname(value)
        except forms.ValidationError:
            raise forms.ValidationError(
                get_adapter().error_messages['nickname_taken'])

    def validate_unique_phone_number(self, value):
        try:
            return get_adapter().validate_unique_phone_number(value)
        except forms.ValidationError:
            raise forms.ValidationError(
                get_adapter().error_messages['phone_number_taken'])
    


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
        required=False,
        validators=[validate_password],
    )
    new_password2 = forms.CharField(
        label='새 비밀번호 확인',
        strip=False,
        required=False,
        widget=forms.PasswordInput,
    )
    email = forms.EmailField(required=False, widget = forms.TextInput(attrs={'readonly': ''}))
    nickname = forms.CharField(required=False)
    phone_number = forms.CharField(required=False, max_length = 11, validators=[PhoneNumberValidator()])

    def clean_new_password2(self):
        password = self.cleaned_data.get('old_password')
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
            else:
                password_validation.validate_password(password2, self.user)
                return password2

        return password

    def save(self, commit=True):
        if self.cleaned_data.get('new_password1'):
            password = self.cleaned_data["new_password1"]
        else:
            password = self.cleaned_data['old_password']
        nickname = self.cleaned_data['nickname']
        phone_number = self.cleaned_data['phone_number']

        if nickname:
            self.user.nickname = nickname
        if phone_number:
            self.user.phone_number = phone_number
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
