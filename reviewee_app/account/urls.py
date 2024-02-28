from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('account/', include(
        [
            path('details/', views.my_account_details, name='personal account details'),
            path('<int:pk>/details/', views.account_details, name='account details'),
            path('edit/', views.account_edit, name='account edit'),
            path('delete/', views.account_delete, name='account delete'),
        ]
    ))
]
