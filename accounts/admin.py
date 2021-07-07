from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User
# Register your models here.

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['id','username','date_joined']
    fieldsets = (
        (None, {'fields': ('username','email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'state', 'city', 'zipcode', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'zipcode'),
        }),
    )
