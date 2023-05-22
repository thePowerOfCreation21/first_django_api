"""
Database models
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""

        """raising ValueError if email is empty"""
        if not email:
            raise ValueError('user must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creating and returning a new superuser."""
        return self.create_user(
            email=email,
            password=password,
            is_superuser=True,
            is_staff=True
        )


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    """Fields"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    """Configurations"""
    objects = UserManager()
    USERNAME_FIELD = 'email'
