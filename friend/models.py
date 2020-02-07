from django.conf import settings
from django.db import models

from simple_history.models import HistoricalRecords


class Friendship(models.Model):
    history = HistoricalRecords()

    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="current_user")
    friend_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="friend")
    friendship_start_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} -> Love <- {self.friend_id}"
