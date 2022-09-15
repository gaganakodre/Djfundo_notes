from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


#  Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, username, password, *args, **kwargs):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            *args, **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, *args, **kwargs):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
            *args, **kwargs
        )
        user.is_admin = True
        user.is_verified = True
        user.save(using=self._db)
        return user


# Create your models here.
class User(AbstractBaseUser):
    """
    This model will create the user
    """
    username = models.CharField(max_length=200, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=250)
    is_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
