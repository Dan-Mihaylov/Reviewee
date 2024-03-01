from django.core import validators
from django.core.exceptions import ValidationError


CONSECUTIVE_SPACE_ERROR_MESSAGE = "You can't use consecutive spaces in the place name."


def consecutive_spaces_checker(value: str) -> str:
    consecutive_space_count = 0

    for char in value:
        if char == ' ':
            consecutive_space_count += 1
            if consecutive_space_count > 1:
                return True  # There are consecutive spaces in the value
        consecutive_space_count = 0

    return False  # There are no consecutive spaces


def alphanumeric_and_spaces_values_validator(value: str) ->str:

    INVALID_CHARACTERS_ERROR_MESSAGE = 'You can use only letters, spaces and numbers.'

    consecutive_space_count = 0

    if consecutive_spaces_checker(value):
        raise ValidationError(CONSECUTIVE_SPACE_ERROR_MESSAGE)

    for char in value:
        if not (char.isalnum() or char == ' '):
            raise ValidationError(INVALID_CHARACTERS_ERROR_MESSAGE)

    return value


def only_letters_and_spaces_values_validator(value: str) -> str:

    INVALID_CHARACTERS_ERROR_MESSAGE = 'You can use only letters and spaces.'

    if consecutive_spaces_checker(value):
        raise ValidationError(CONSECUTIVE_SPACE_ERROR_MESSAGE)

    if not all([char.isalpha() or char==' ' for char in value]):
        raise ValidationError(INVALID_CHARACTERS_ERROR_MESSAGE)

