from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('account/', include(
        [
            path('<int:pk>/details/', views.ProfileDetailsView.as_view(), name='profile details'),
            path('edit/', views.EditProfileView.as_view(), name='profile edit'),
            path('edit/business/', views.EditBusinessProfileView.as_view(), name='business profile edit'),
            path('delete/', views.ProfileDeleteView.as_view(), name='profile delete'),
        ]
    ))
]
