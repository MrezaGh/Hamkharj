from django.urls import path

from .views import expense_create_view, summary

urlpatterns = [
    path("create-expense/", expense_create_view, name="create_expense"),
    path("create-expense/<int:group_id>", expense_create_view, name="create_expense"),
    path("summary/", summary, name="summary-of-expenses"),

]
