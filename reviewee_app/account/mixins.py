from django.contrib.auth.mixins import AccessMixin
from django.urls import reverse_lazy


class BusinessOwnerRequiredMixin(AccessMixin):

    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        # Try-except in case someone tries to access the url and is not logged in, so it doesn't crash
        try:
            is_business_owner = request.user.profile.is_owner()

            if not is_business_owner:
                return self.handle_no_permission()

            return super().dispatch(request, *args, **kwargs)

        except Exception:
            return self.handle_no_permission()
