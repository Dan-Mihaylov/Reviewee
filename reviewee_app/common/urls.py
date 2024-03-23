from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('browse/', views.BrowsePageView.as_view(), name='browse'),
]
