from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import User, Profile

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_active', 'is_superuser')
    list_filter = ('email', 'is_active', 'is_superuser')
    searching_fields = ('email',)
    ordering = ('email',)
    fieldsets = (('Authentication', {'fields': ('email', 'password')}), ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}), ('Group permissions', {'fields': ('groups', 'user_permissions')}), ('Important date', {'fields': ('last_login',)}),)
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')}),)

admin.site.register(Profile)
admin.site.register(User, CustomUserAdmin)


