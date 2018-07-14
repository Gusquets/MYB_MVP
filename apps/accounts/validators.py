import re

from django.core.exceptions import ValidationError


def validate_password(value):
    wrong_length = len(value) < 6 or len(value) > 32
    wrong_type = not bool(re.match('^(?=.*[a-zA-Z])(?=.*[0-9])', value))

    if wrong_length or wrong_type:
        raise ValidationError('6~32자 영문, 숫자를 사용하세요.')
