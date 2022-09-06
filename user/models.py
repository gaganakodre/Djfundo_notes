from django.db import models


# Create your models here.
class User(models.Model):
    REQUIRED_FIELDS = ('email', 'password',)
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=250)

    def __str__(self):
        return self.username
