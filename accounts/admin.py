
from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
admin.site.unregister(User)
@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff', 'avatar_image'
    )

    def avatar_image(self, obj):
        try:
            avatar = obj.profile.avatar
            if avatar:
                # Use the filename directly as stored in the profile
                return format_html(
                    '<img src="/static/images/{}" width="32" height="32" style="object-fit:cover;border-radius:50%;">',
                    avatar
                )
        except Exception:
            pass
        # Show a default avatar if missing
        return format_html(
            '<img src="/static/images/default.png" width="32" height="32" style="object-fit:cover;border-radius:50%;opacity:0.5;">'
        )
    avatar_image.short_description = 'Avatar'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar_image', 'role', 'bio', 'website', 'github', 'linkedin')

    def avatar_image(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="/static/images/{}" width="32" height="32" style="object-fit:cover;border-radius:50%;">',
                obj.avatar
            )
        return ""
    avatar_image.allow_tags = True
    avatar_image.short_description = 'Avatar'
