from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import ExpenseCreateView, ExpenseUpdateView, ExpenseSummaryView, CategoryCreateView

urlpatterns = [
    path("create-expense/<int:group_id>", login_required(ExpenseCreateView.as_view()), name="create_expense"),
    path("update-expense/<int:expense_id>", login_required(ExpenseUpdateView.as_view()), name="update_expense"),
    path("create-expense-category/<int:group_id>", login_required(CategoryCreateView.as_view()), name="create_category"),
    path("summary/", ExpenseSummaryView.as_view(), name="summary-of-expenses"),

]
