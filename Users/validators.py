import re
from django.core.exceptions import ValidationError


def validate_phone_number(value):
    number = str(value)
    pattern = re.compile("[0-9]+")
    if "0" not in number[0]:
        raise ValidationError("Phone numbers should start with 0 ")
    if len(number) < 11:
        raise ValidationError("Phone number should not be less than 11")
    elif len(number) > 11:
        raise ValidationError("Phone number should not be greater than 11")

    elif pattern.fullmatch(number) is not None:
        return number
    else:
        raise ValidationError('Remove letters or special characters to continue')