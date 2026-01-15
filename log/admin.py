from django.contrib import admin
from .models import DeviceGroup, Device, Code, Screenshot


@admin.register(DeviceGroup)
class DeviceGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at", "updated_at")
    search_fields = ("name",)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("id", "ip", "active", "group", "created_at", "updated_at")
    list_filter = ("active", "group")
    search_fields = ("ip",)


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "active", "created_at", "updated_at")
    list_filter = ("active",)
    search_fields = ("name",)


@admin.register(Screenshot)
class ScreenshotAdmin(admin.ModelAdmin):
    list_display = ("id", "ip", "device", "created_at", "updated_at")
    list_filter = ("device", "created_at")
    search_fields = ("ip", "device__ip")
