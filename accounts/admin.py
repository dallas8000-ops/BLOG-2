
from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
admin.site.unregister(User)
@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    list_display = DefaultUserAdmin.list_display + ('avatar_image',)

    def avatar_image(self, obj):
        try:
            avatar = obj.profile.avatar
            if avatar:
                return format_html(
                    '<img src="/static/images/{}" width="32" height="32" style="object-fit:cover;border-radius:50%;">',
                    avatar.split("/")[-1]
                )
        except Exception:
            return ""
        return ""
    avatar_image.short_description = 'Avatar'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar_image')

    def avatar_image(self, obj):
        if obj.avatar:
            return f'<img src="/static/images/{obj.avatar.split("/")[-1]}" width="32" height="32" style="object-fit:cover;border-radius:50%;">'
        return ""
    avatar_image.allow_tags = True
    avatar_image.short_description = 'Avatar'
