from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ExpenseForm


@login_required
def expense_create_view(request):
    form = ExpenseForm(request.POST or None, user=request.user)
    if form.is_valid():
        form.save()
        return redirect("panel")
    context = {"form": form}
    return render(request, "pages/create_expense.html", context)
