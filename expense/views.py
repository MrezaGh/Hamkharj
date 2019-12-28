from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ExpenseForm
from .models import Expense, Record


@login_required
def expense_create_view(request, **kwargs):
    form = ExpenseForm(request.POST or None, user=request.user, g_id=kwargs.pop('group_id'))
    if form.is_valid():
        form.save()
        return redirect("panel")
    context = {"form": form}
    return render(request, "pages/create_expense.html", context)


def summary(request):
    paid_expenses = Expense.objects.filter(creator=request.user)
    in_debt_users = {}
    for paid_expense in paid_expenses:
        # paid_expenses = Expense()
        records_of_paid_expenses = Record.objects.filter(expense=paid_expense)
        if len(records_of_paid_expenses):
            in_debt_users[paid_expense.title] = [(paid_expense.amount,record.user, record.percent_of_share * paid_expense.amount/100) for record in records_of_paid_expenses]

    return render(request, 'pages/summary_of_expenses.html', context={'expenses': in_debt_users, 'creator':request.user})
