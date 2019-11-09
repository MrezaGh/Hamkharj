from django.urls import path

from .views import expense_create_view

urlpatterns = [
    path("create-expense/", expense_create_view, name="create_expense"),
]
