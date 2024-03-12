from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('account/', include(
        [
            path('details/', views.my_account_details, name='personal account details'),
            path('<int:pk>/details/', views.account_details, name='account details'),
            path('edit/', views.EditProfileView.as_view(), name='profile edit'),
            path('edit/business/', views.EditBusinessProfileView.as_view(), name='business profile edit'),
            path('delete/', views.account_delete, name='account delete'),
        ]
    ))
]
