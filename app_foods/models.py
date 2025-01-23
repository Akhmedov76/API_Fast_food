from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [(
        ('admin', 'Admin'),
        ('user', 'User'),
        ('courier', 'Courier'),
    )]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user',
    )

    @property
    def is_admin(self):
        return self.role == 'admin'
