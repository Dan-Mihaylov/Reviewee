from django import forms

from reviewee_app.booking.models import RestaurantBooking, HotelBooking


class RestaurantBookingForm(forms.ModelForm):

    class Meta:
        model = RestaurantBooking
        fields = '__all__'

