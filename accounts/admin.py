
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.utils.html import format_html

from .models import Profile


def avatar_url(avatar_value):
    if not avatar_value:
        return static('images/avatar-default.svg')
    if avatar_value.startswith('images/'):
        return static(avatar_value)
    return static(f'images/{avatar_value}')


admin.site.unregister(User)


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff', 'avatar_image'
    )

    def avatar_image(self, obj):
        try:
            avatar = obj.profile.avatar
            return format_html(
                '<img src="{}" width="32" height="32" style="object-fit:cover;border-radius:50%;">',
                avatar_url(avatar)
            )
        except Exception:
            pass
        return format_html(
            '<img src="{}" width="32" height="32" style="object-fit:cover;border-radius:50%;opacity:0.65;">',
            avatar_url(None)
        )
    avatar_image.short_description = 'Avatar'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar_image', 'role', 'bio', 'website', 'github')

    def avatar_image(self, obj):
        return format_html(
            '<img src="{}" width="32" height="32" style="object-fit:cover;border-radius:50%;">',
            avatar_url(obj.avatar)
        )
    avatar_image.allow_tags = True
    avatar_image.short_description = 'Avatar'
