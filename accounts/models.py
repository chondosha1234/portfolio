from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    username = models.TextField(max_length=64, unique=True, primary_key=True)

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username
