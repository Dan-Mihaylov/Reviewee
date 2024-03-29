from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reviewee_app.common.urls')),              # Common for index page
    path('', include('reviewee_app.account.urls')),             # Accounts
    path('place/', include('reviewee_app.place.urls')),         # Place and review
    path('booking/', include('reviewee_app.booking.urls')),     # Booking apps
    path('review/', include('reviewee_app.review.urls')),       # Review app
    path('favourite/', include('reviewee_app.favourite.urls')), # Add and remove to/from favourite
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
