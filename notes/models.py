from django.db import models
from user.models import User


# Create your models here.

class Notes(models.Model):
    """
    This model class create the notes with title and description
    """
    title = models.CharField(max_length=250)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
