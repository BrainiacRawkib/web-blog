from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'facebook', 'twitter', 'linkedin']
    list_display_links = ['id', 'user']
    raw_id_fields = ['user']
