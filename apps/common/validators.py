import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_password(value):
    wrong_length = len(value) < 6 or len(value) > 32
    wrong_type = not bool(re.match('^(?=.*[a-zA-Z])(?=.*[0-9])', value))

    if wrong_length or wrong_type:
        raise ValidationError('6~32자 영문, 숫자를 사용하세요.')


class PhoneNumberValidator(RegexValidator):
    regex = r'^(?:(010\d{4})|(01[1|6|7|8|9]\d{3,4}))(\d{4})*$'
    message = '올바른 형식의 휴대폰번호를 입력하세요.'
    code = 'invalid'


def validate_movie_url(value):
    find_embed = value.find('embed')

    if find_embed == -1:
        raise ValidationError('Embed용 youtube 주소를 입력해 주세요.')

class ProbabilityValidator(RegexValidator):
    regex = r'^(?:(\d{2})|(100))*$'
    message = '0-100의 값을 입력해 주세요'
    code = 'invalid'