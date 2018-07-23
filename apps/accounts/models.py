from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.common.validators import PhoneNumberValidator, validate_movie_url

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


def artist_image_upload_to(instance, filename):
    return '/'.join([instance.name, 'title_images/', filename])

class Artist(models.Model):
    name = models.CharField('아티스트명', max_length = 50, unique=True)
    description = models.TextField('아티스트 소개')
    is_verify = models.BooleanField('아티스트 인증여부', default = False)
    image = models.ImageField('사진', upload_to = artist_image_upload_to)
    movie_1 = models.URLField('Youtube 영상 1', blank = True, null = True, validators = [validate_movie_url])
    movie_2 = models.URLField('Youtube 영상 2', blank = True, null = True, validators = [validate_movie_url])
    movie_3 = models.URLField('Youtube 영상 3', blank = True, null = True, validators = [validate_movie_url])
    social_fb = models.URLField('소셜_페이스북', blank = True, null = True)
    social_insta = models.URLField('소셜_인스타그램', blank = True, null = True)
    social_youtube = models.URLField('소셜_유튜브', blank = True, null = True)
    rate_avg = models.DecimalField('평점', max_digits=2, decimal_places=1, default = 0)
    regist_dt = models.DateTimeField('등록시간',auto_now_add = True)

    class Meta:
        verbose_name = '아티스트'
        verbose_name_plural = '아티스트'

    def __str__(self):
        return self.name

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name
        

class User(AbstractUser):
    username = None
    first_name = None
    last_name = None

    email = models.EmailField('이메일', unique=True)
    nickname = models.CharField('닉네임', max_length=50, unique = True)
    phone_number = models.CharField('휴대폰 번호', max_length = 11, validators=[PhoneNumberValidator()], unique = True)
    regist_dt = models.DateTimeField('등록시간', auto_now_add=True)
    is_agreed_1 = models.BooleanField('이용약관 동의여부', default = False)
    is_agreed_2 = models.BooleanField('개인정보 처리방침 동의여부', default = False)
    usertype = models.IntegerField('유저 타입', choices = ((1,'일반 회원'),(2,'아티스트 회원')), default = 1)
    artist = models.ForeignKey(Artist, verbose_name = '아티스트 이름', on_delete = models.CASCADE, blank = True, null =True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = '회원'
        verbose_name_plural = '회원'

    def __str__(self):
        return self.nickname

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.nickname
    
    def get_user_type(self):
        return self.usertype


def artist_image_upload_to_2(instance, filename):
    return '/'.join([instance.artist.name, 'images/', filename])

class ArtistImages(models.Model):
    artist = models.ForeignKey(Artist, verbose_name = '아티스트', on_delete = models.CASCADE)
    image = models.ImageField('사진 1', upload_to=artist_image_upload_to_2)

    class Meta:
        verbose_name = '아티스트 사진'
        verbose_name_plural = '아티스트 사진'
