from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.fields import CharField, BooleanField, DateTimeField

from apps.models import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        MANAGER = 'manager', 'Manager'
        MASTER = 'master', 'Master'

    phone = CharField(max_length=20, unique=True)
    full_name = CharField(max_length=255, blank=True)

    role = CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ADMIN
    )

    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)

    created_at = DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone
