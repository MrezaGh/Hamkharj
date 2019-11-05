from django.db import models
from django.conf import settings

class Expense(models.Model):

    title = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    amount = models.DecimalField(name="Amount", max_digits=9, decimal_places=0)
    description = models.TextField(blank=True)
    
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)






