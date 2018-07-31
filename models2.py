# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountEmailaddress(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    verified = models.BooleanField()
    primary = models.BooleanField()
    user = models.ForeignKey('AccountsUser', models.DO_NOTHING)
    email = models.CharField(unique=True, max_length=254)

    class Meta:
        managed = False
        db_table = 'account_emailaddress'


class AccountEmailconfirmation(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    created = models.DateTimeField()
    sent = models.DateTimeField(blank=True, null=True)
    key = models.CharField(unique=True, max_length=64)
    email_address = models.ForeignKey(AccountEmailaddress, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_emailconfirmation'


class AccountsArtist(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=50)
    description = models.TextField()
    is_verify = models.BooleanField()
    social_fb = models.CharField(max_length=200, blank=True, null=True)
    social_insta = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    regist_dt = models.DateTimeField()
    movie_1 = models.CharField(max_length=200, blank=True, null=True)
    movie_2 = models.CharField(max_length=200, blank=True, null=True)
    image = models.CharField(max_length=100)
    rate_avg = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    movie_3 = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accounts_artist'


class AccountsArtistimage(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    image = models.CharField(max_length=100)
    artist = models.ForeignKey(AccountsArtist, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_artistimage'


class AccountsArtistimages(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    artist = models.ForeignKey(AccountsArtist, models.DO_NOTHING)
    image = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'accounts_artistimages'


class AccountsArtistmovie(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    movie = models.CharField(max_length=100)
    artist = models.ForeignKey(AccountsArtist, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_artistmovie'


class AccountsUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    email = models.CharField(unique=True, max_length=254)
    nickname = models.CharField(unique=True, max_length=50)
    regist_dt = models.DateTimeField()
    is_agreed_1 = models.BooleanField()
    is_agreed_2 = models.BooleanField()
    usertype = models.IntegerField()
    artist = models.ForeignKey(AccountsArtist, models.DO_NOTHING, blank=True, null=True)
    phone_number = models.CharField(unique=True, max_length=11)

    class Meta:
        managed = False
        db_table = 'accounts_user'


class AccountsUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)
    group = models.ForeignKey('AuthGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_user_groups'
        unique_together = (('user', 'group'),)


class AccountsUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class ConcertConcert(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    date = models.DateField()
    time = models.TimeField()
    location_1 = models.CharField(max_length=50)
    location_2 = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    probability = models.PositiveIntegerField()
    artist = models.ForeignKey(AccountsArtist, models.DO_NOTHING)
    location_else = models.CharField(max_length=50)
    recommend_yn = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'concert_concert'


class ConcertConcertsonglist(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=50)
    concert = models.ForeignKey(ConcertConcert, models.DO_NOTHING)
    info = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'concert_concertsonglist'


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=50)
    domain = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'django_site'


class PaymentSponsor(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    amount = models.PositiveIntegerField()
    regist_dt = models.DateTimeField()
    artist = models.ForeignKey(AccountsArtist, models.DO_NOTHING)
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING, blank=True, null=True)
    imp_uid = models.CharField(max_length=100)
    merchant_uid = models.CharField(max_length=32)
    status = models.CharField(max_length=9)
    meta = models.TextField()
    message = models.TextField(blank=True, null=True)
    user_name = models.CharField(max_length=50)
    pay_type = models.CharField(max_length=20)
    rate = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'payment_sponsor'


class PreferenceAnswer(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    description = models.TextField()
    review = models.ForeignKey('PreferenceReview', models.DO_NOTHING)
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'preference_answer'


class PreferenceBasket(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    artist = models.ForeignKey(AccountsArtist, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)
    concert = models.ForeignKey(ConcertConcert, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'preference_basket'


class PreferenceLike(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    regist_dt = models.DateTimeField()
    review = models.ForeignKey('PreferenceReview', models.DO_NOTHING)
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'preference_like'


class PreferenceReview(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    rate = models.IntegerField()
    description = models.TextField()
    is_pay = models.BooleanField()
    regist_dt = models.DateTimeField()
    artist = models.ForeignKey(AccountsArtist, models.DO_NOTHING)
    like_count = models.PositiveIntegerField()
    amount = models.PositiveIntegerField(blank=True, null=True)
    user_name = models.CharField(max_length=50)
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'preference_review'


class SocialaccountSocialaccount(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    provider = models.CharField(max_length=30)
    uid = models.CharField(max_length=191)
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)
    extra_data = models.TextField()

    class Meta:
        managed = False
        db_table = 'socialaccount_socialaccount'
        unique_together = (('provider', 'uid'),)


class SocialaccountSocialapp(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    provider = models.CharField(max_length=30)
    name = models.CharField(max_length=40)
    client_id = models.CharField(max_length=191)
    key = models.CharField(max_length=191)
    secret = models.CharField(max_length=191)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialapp'


class SocialaccountSocialappSites(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    socialapp = models.ForeignKey(SocialaccountSocialapp, models.DO_NOTHING)
    site = models.ForeignKey(DjangoSite, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialapp_sites'
        unique_together = (('socialapp', 'site'),)


class SocialaccountSocialtoken(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    token = models.TextField()
    token_secret = models.TextField()
    expires_at = models.DateTimeField(blank=True, null=True)
    account = models.ForeignKey(SocialaccountSocialaccount, models.DO_NOTHING)
    app = models.ForeignKey(SocialaccountSocialapp, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialtoken'
        unique_together = (('app', 'account'),)


class WebsiteCsservice(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    from_email = models.CharField(max_length=254)
    title = models.CharField(max_length=100)
    description = models.TextField()
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'website_csservice'


class WebsiteTerms(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    description = models.TextField()
    category = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'website_terms'
