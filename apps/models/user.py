from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.models import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=255, blank=True)

    role = models.CharField(
        max_length=20,
        choices=(
            ('admin', 'Admin'),
            ('manager', 'Manager'),
            ('master', 'Master'),
        ),
        default='admin'
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # admin panel access

    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone