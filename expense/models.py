from django.conf import settings
from django.db import models
from django.contrib.gis.db import models as nm

from simple_history.models import HistoricalRecords


class Expense(models.Model):
    history = HistoricalRecords()

    title = models.CharField(max_length=200)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE, related_name="creator"
    )
    amount = models.DecimalField(max_digits=9, decimal_places=0)
    description = models.TextField(blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    expense_attachment = models.ImageField(
        upload_to='expenses/attachments',
        blank=True,
        default='',
        verbose_name='expense attachment'
    )

    category = models.ForeignKey(
        to='expense.ExpenseCategory',
        related_name='expenses',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        verbose_name='category'
    )

    location = nm.PointField(null=True, blank=True, srid=4326)

    def __str__(self):
        return self.title


class Record(models.Model):
    history = HistoricalRecords()

    expense = models.ForeignKey("Expense", models.CASCADE, related_name="records")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE, related_name="user"
    )
    percent_of_share = models.DecimalField(max_digits=9, decimal_places=1, default=0)

    class Meta:
        unique_together = ["expense", "user"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(percent_of_share__lte=100),
                name="percent_of_share_lte_100",
            ),
        ]


class ExpenseCategory(models.Model):
    history = HistoricalRecords()

    title = models.CharField(max_length=50, verbose_name='title')
    group = models.ForeignKey(
        to='group.Group',
        related_name='expense_categories',
        on_delete=models.DO_NOTHING,
        verbose_name='group'
    )

    def __str__(self):
        return self.title
