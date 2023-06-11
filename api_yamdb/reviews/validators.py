from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def validate_max_min(value):
    if value < 1 or value > 10:
        raise ValidationError(
            _("%(value)s не находиться в пределах от 1 до 10 включительно."),
            params={"value": value},
        )


def validate_year(value):
    now = timezone.now().year
    if value > now:
        raise ValidationError(
            f'{value} не может быть больше {now}'
        )
