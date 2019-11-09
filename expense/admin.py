from django.contrib import admin

from .models import Expense, Record

admin.site.register(Expense)
admin.site.register(Record)
