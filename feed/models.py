from django.db import models
from users.models import Profile

class SavedNewsItem(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    source = models.CharField(max_length=200)
    date = models.CharField(max_length=200)

