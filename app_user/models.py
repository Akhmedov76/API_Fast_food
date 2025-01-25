from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRoleChoice(models.TextChoices):
    """
    UserRoleChoice is a class that contains choices for the user role.
    """
    ADMIN = "admin", "Admin"
    USER = "user", "User"
    WAITER = "waiter", "Waiter"


class UserStatusChoice(models.TextChoices):
    """
    UserStatusChoice is a class that contains choices for the user status.
    """
    ACTIVE = "active", "Active"
    DELETE = "delete", "Delete"
    INACTIVE = "inactive", "Inactive"



class UserModel(AbstractUser):
    """
    UserModel is a custom user model that extends the AbstractUser model provided by Django.
    It has additional fields such as role, status.
    The role field is a CharField with choices to specify the user's role in the system.
    The status field is a CharField to specify the user's status in the system.
    """

    role = models.CharField(
        default=UserRoleChoice.USER,
        max_length=15,
        choices=UserRoleChoice.choices)
    status = models.CharField(
        default=UserStatusChoice.ACTIVE,
        max_length=15,
        choices=UserStatusChoice.choices)
