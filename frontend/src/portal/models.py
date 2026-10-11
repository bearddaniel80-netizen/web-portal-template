from django.contrib.auth.models import User
from django.db import models


class SecurityGroup(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    users = models.ManyToManyField(
        User,
        related_name="security_groups",
        blank=True,
    )

    def __str__(self):
        return self.name


class Application(models.Model):
    id = models.SlugField(
        primary_key=True,
    )

    name = models.CharField(
        max_length=100,
    )

    description = models.TextField(
        blank=True,
    )

    service = models.CharField(
        max_length=100,
        unique=True,
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
    )

    enabled = models.BooleanField(
        default=True,
    )

    groups = models.ManyToManyField(
        SecurityGroup,
        related_name="applications",
        blank=True,
    )

    def __str__(self):
        return self.name
