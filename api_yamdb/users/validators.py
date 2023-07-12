import re

from rest_framework.exceptions import ValidationError

from constants import USERNAME_PATTERN


def regex_validator(value):
    if value.lower() == 'me':
        raise ValidationError("Username 'me' is not allowed.")

    if not re.match(USERNAME_PATTERN, value):
        invalid_chars = re.sub(USERNAME_PATTERN, '', value)
        error_message = (f"Username contains "
                         f"invalid characters: {invalid_chars}")
        raise ValidationError(error_message)


def no_me_validator(value):
    if 'me' == value:
        raise ValidationError('A username cannot equals "me".')


class UsernameValidationMixin:
    def validate_username(self, value):
        regex_validator(value)
        return value
