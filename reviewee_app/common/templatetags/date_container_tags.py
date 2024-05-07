from django.template import Library
from datetime import datetime, timedelta
from reviewee_app.booking.helpers import find_bookings_count_for_place
from reviewee_app.place.models import Hotel, Restaurant

register = Library()


@register.inclusion_tag('partials/generate_container_dates.html')
def generate_container_dates(get_parameters: str, place: Hotel or Restaurant):
    # remove the &for_date from the get params and discard the last bit
    get_parameters = get_parameters.split('&for_date=')
    selected_date = get_parameters[-1] if len(get_parameters) > 1 else None
    get_parameters = ''.join(get_parameters[0:-1]) if len(get_parameters) > 1 else ''.join(get_parameters)

    dates_and_count_dict = {
        (datetime.now().date() + timedelta(days=day)).strftime('%Y-%m-%d')
        :   find_bookings_count_for_place(place=place, date=(datetime.now().date() + timedelta(days=day)))
        for day in range(-3, 8)
    }

    return {
        'get_parameters': get_parameters,
        'selected_date': selected_date,
        'dates_and_count_dict': dates_and_count_dict,
    }
