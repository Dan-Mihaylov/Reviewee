from django.contrib.auth.mixins import AccessMixin


class BookingOwnerRequiredMixin(AccessMixin):

    @staticmethod
    def booking_ownership_verified(request, **kwargs):
        return kwargs['slug'] in request.session['owned_bookings']

    def dispatch(self, request, *args, **kwargs):

        if self.booking_ownership_verified(request, **kwargs):
            return super().dispatch(request, *args, **kwargs)

        return self.handle_no_permission()


class BookingConfirmationDataInSessionMixin:

    @staticmethod
    def attach_booking_info_to_session(request, booking):
        if hasattr(booking, 'restaurant'):
            request.session['place_name'] = booking.restaurant.name
        else:
            request.session['place_name'] = booking.hotel.name
        request.session['date'] = str(booking.date)
        request.session['confirmation_code'] = booking.confirmation_code
        request.session['email'] = booking.email

