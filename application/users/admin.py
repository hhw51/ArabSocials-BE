from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    # Fields to display in the admin list view
    list_display = ('id', 'username', 'email', 'name', 'phone', 'location', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')  # Add filters for user status
    search_fields = ('username', 'email', 'name', 'phone')  # Enable search for these fields
    ordering = ('id',)  # Default ordering
    readonly_fields = ('date_joined', 'last_login')  # Make these fields read-only

    # Fields to display in the admin detail/edit view
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('name', 'email', 'phone', 'location', 'marital_status', 'interests', 'profession', 'social_links')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields to display when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

# Register the User model with the custom admin
admin.site.register(User, UserAdmin)
