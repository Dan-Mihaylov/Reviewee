import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reviewee_app.settings")
django.setup()


# From here down
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import requests


request = requests.get('https://restcountries.com/v3.1/name/greece?fullText=true')
json_response = request.json()
items = json_response.pop(0)
print(items['name']['common'])
# or official

# TODO Add this validator to the Business Model Country
# Validator
def check_country_name(country_name: str) -> str or ValidationError:

    response = requests.get(f'https://restcountries.com/v3.1/name/{country_name}?fullText=true')

    if response.status_code == 200:
        return country_name
    else:
        raise ValidationError('This country name is not valid, please enter a valid country name.')


print(check_country_name('georgia'))