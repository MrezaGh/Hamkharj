from django.db import models
from django.contrib.auth.models import User


class Expense(models.Model):

    user = models.ForeignKey(User, models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    amount = models.DecimalField(name="Amount", max_digits=9)
    description = models.TextField(blank=True)
    title = models.CharField(max_length=200)





