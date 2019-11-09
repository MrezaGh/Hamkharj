from django.db import models
from django.conf import settings


class Expense(models.Model):

    title = models.CharField(max_length=200)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE, related_name="creator"
    )
    other = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE, related_name="other"
    )
    amount = models.DecimalField(max_digits=9, decimal_places=0)
    description = models.TextField(blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class Record(models.Model):

    expense = models.ForeignKey(
        'Expense', models.CASCADE, related_name='expense'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE, related_name='user'
    )
    percent_of_share = models.DecimalField(max_digits=9, decimal_places=1, default=0)

