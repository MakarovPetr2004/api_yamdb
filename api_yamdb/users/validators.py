import re

from rest_framework.exceptions import ValidationError

from constants import USERNAME_PATTERN


def regex_validator(value):
    if value.lower() == 'me':
        raise ValidationError("Username 'me' is not allowed.")

    invalid_chars = ''.join(set(re.sub(USERNAME_PATTERN, '', value)))
    if invalid_chars:
        error_message = (f"Username contains invalid characters:"
                         f" {invalid_chars}")
        raise ValidationError(error_message)


class UsernameValidationMixin:
    def validate_username(self, value):
        regex_validator(value)
        return value
