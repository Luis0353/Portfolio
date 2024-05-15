from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    repository = models.URLField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.title