from django.contrib import admin

from .models import Application, SecurityGroup


@admin.register(SecurityGroup)
class SecurityGroupAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    filter_horizontal = ("users",)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "service", "enabled")
    list_filter = ("enabled",)
    search_fields = ("name", "description", "service")
    filter_horizontal = ("groups",)