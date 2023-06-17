import re

from rest_framework.exceptions import ValidationError

from constants import USERNAME_PATTERN


def regex_validator(value):
    if not re.match(USERNAME_PATTERN, value):
        raise ValidationError(
            'Username must match the pattern ' + USERNAME_PATTERN
        )


def no_me_validator(value):
    if 'me' == value:
        raise ValidationError('A username cannot equals "me".')


class UsernameValidationMixin:
    def validate_username(self, value):
        regex_validator(value)
        no_me_validator(value)
        return value
