from django.core import validators
from django.core.exceptions import ValidationError

import requests


CONSECUTIVE_SPACE_ERROR_MESSAGE = "You can't use consecutive spaces in the place name."


def consecutive_spaces_checker(value: str) -> str or ValidationError:
    consecutive_space_count = 0

    for char in value:
        if char == ' ':
            consecutive_space_count += 1
            if consecutive_space_count > 1:
                return True  # There are consecutive spaces in the value
        consecutive_space_count = 0

    return False  # There are no consecutive spaces


def alphanumeric_and_spaces_values_validator(value: str) ->str or ValidationError:

    INVALID_CHARACTERS_ERROR_MESSAGE = 'You can use only letters, spaces and numbers.'

    consecutive_space_count = 0

    if consecutive_spaces_checker(value):
        raise ValidationError(CONSECUTIVE_SPACE_ERROR_MESSAGE)

    for char in value:
        if not (char.isalnum() or char == ' '):
            raise ValidationError(INVALID_CHARACTERS_ERROR_MESSAGE)

    return value


def only_letters_and_spaces_values_validator(value: str) -> str or ValidationError:

    INVALID_CHARACTERS_ERROR_MESSAGE = 'You can use only letters and spaces.'

    if consecutive_spaces_checker(value):
        raise ValidationError(CONSECUTIVE_SPACE_ERROR_MESSAGE)

    if not all([char.isalpha() or char==' ' for char in value]):
        raise ValidationError(INVALID_CHARACTERS_ERROR_MESSAGE)


def alphanumeric_and_dashes_validator(value: str) -> str or ValidationError:
    INVALID_CHARACTERS_ERROR_MESSAGE = 'You can use only letters, numbers and dashes "- or _".'
    INVALID_ALL_DASHES_ERROR_MESSAGE = 'You cannot use only dashes'

    if not all([char.isalnum() or char in '-_' for char in value]):
        raise ValidationError(INVALID_CHARACTERS_ERROR_MESSAGE)

    if all([not char.isalpha() for char in value]):
        raise ValidationError(INVALID_ALL_DASHES_ERROR_MESSAGE)

    return value


def check_country_name_validator(country_name: str) -> str or ValidationError:
    INVALID_COUNTRY_NAME_ERROR_MESSAGE = 'Please enter a valid Country name.'

    response = requests.get(f'https://restcountries.com/v3.1/name/{country_name}?fullText=true')

    if response.status_code == 200:
        return country_name

    raise ValidationError(INVALID_COUNTRY_NAME_ERROR_MESSAGE)
