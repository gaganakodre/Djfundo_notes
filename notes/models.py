from django.db import models

from lables.models import Labels
from user.models import User


# Create your models here.

class Notes(models.Model):
    """
    This model class create the notes with title and description
    """
    title = models.CharField(max_length=250)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    labels = models.ManyToManyField(Labels, null=True, blank=True)
    collaborator = models.ManyToManyField(User, related_name='collaborator')
    is_pinned = models.BooleanField(default=False)
    is_archive = models.BooleanField(default=False)

    def __str__(self):
        return self.title
