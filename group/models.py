from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords


class Group(models.Model):
    history = HistoricalRecords()

    title = models.CharField(max_length=200, default="My Group")
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owner"
    )
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="group")
    description = models.TextField(blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
