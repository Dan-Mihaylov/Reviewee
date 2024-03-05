from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ['email', 'is_staff', 'is_active']
    list_filter = ['email', 'is_staff', 'is_active']

    # When you are changing the pass of the User
    fieldsets = (
        (
            'General', {
                'fields': (
                    'email',
                    'password',
                    'username',
                    'first_name',
                    'last_name',
                    'gender',
                    'owner',
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
                        'username',
                        'password1',
                        'password2',
                        'owner',
                        'first_name',
                        'last_name',
                        'gender',
                        'date_of_birth',
                        'is_staff',
                        'is_active',
                        'groups',
                        'user_permissions',

                )
            },
        ),
    )

    search_fields = ['email']

    ordering = ['email']