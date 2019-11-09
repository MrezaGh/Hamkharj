from django.conf import settings
from django.db import models


class Group(models.Model):
    title = models.CharField(max_length=200, default='My Group')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owner")
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="group")
    description = models.TextField(blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
