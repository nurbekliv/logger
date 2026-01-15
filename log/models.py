from __future__ import annotations

from django.db import models
from django.core.validators import FileExtensionValidator


class DeviceGroup(models.Model):
    name = models.CharField(max_length=120, unique=True, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name or f"Group #{self.pk}"


class Device(models.Model):
    ip = models.GenericIPAddressField(unique=True, null=True, blank=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    group = models.ForeignKey(
        DeviceGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="devices",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.ip or f"Device #{self.pk}"


class Code(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(
        upload_to="codes/",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["zip"])],
    )
    active = models.BooleanField(default=True, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "-created_at"]

    def __str__(self) -> str:
        return self.name or f"Code #{self.pk}"


class Screenshot(models.Model):
    image = models.ImageField(upload_to="screenshots/", null=True, blank=True)
    device = models.ForeignKey(
        Device,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="screenshots",
    )

    ip = models.GenericIPAddressField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Screenshot {self.pk} - {self.ip or 'no-ip'}"
