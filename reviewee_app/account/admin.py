from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, CustomUserProfile, CustomUserBusinessProfile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ['pk', 'email', 'is_staff', 'is_active']
    list_filter = ['email', 'is_staff', 'is_active']
    list_per_page = 20
    ordering = ['-pk']

    # When you are changing the pass of the User
    fieldsets = (
        (
            'General', {
                'fields': (
                    'email',
                    'password',
                ),
            }
        ),
        (
            'Permissions', {
                'fields':
                    (
                        'is_staff',
                        'is_active',
                        'groups',
                        'user_permissions'
                     )
            }
        ),
    )

    # When you are creating a new user
    add_fieldsets = (
        (
            None, {
                'classes': ('wide', ),
                'fields':
                    (
                        'email',
                        'password1',
                        'password2',
                        'is_staff',
                        'is_active',
                        'groups',
                        'user_permissions',
                )
            },
        ),
    )

    search_fields = ['email']


@admin.register(CustomUserProfile)
class CustomUserProfileAdmin(admin.ModelAdmin):

    list_display = ['pk', 'user', 'owner', 'username', 'edited_at']
    ordering = ['-pk']


@admin.register(CustomUserBusinessProfile)
class CustomUserBusinessProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'business_name', 'country', 'city', 'postcode', 'address_line',  'created_at', 'edited_at',]
    ordering = ['-pk']
