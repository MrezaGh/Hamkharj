from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import ExpenseCreateView, summary, CategoryCreateView

urlpatterns = [
    path("create-expense/<int:group_id>", login_required(ExpenseCreateView.as_view()), name="create_expense"),
    path("create-expense-category/<int:group_id>", login_required(CategoryCreateView.as_view()), name="create_category"),
    path("summary/", summary, name="summary-of-expenses"),

]
