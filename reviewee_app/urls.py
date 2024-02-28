from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reviewee_app.common.urls')),          # Common for index page
    path('', include('reviewee_app.account.urls')),         # Accounts
    path('place/', include('reviewee_app.place.urls')),     # Place and review
    path('booking/', include('reviewee_app.booking.urls')),  # Booking apps
]
