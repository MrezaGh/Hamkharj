from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import ExpenseForm
from .models import Expense, Record


class ExpenseCreateView(CreateView):
    template_name = 'pages/create_expense.html'
    form_class = ExpenseForm
    success_url = reverse_lazy('panel')

    def get_form_kwargs(self):
        kwargs = super(ExpenseCreateView, self).get_form_kwargs()
        kwargs.update(gid=self.kwargs['group_id'])
        return kwargs

    def get_context_data(self, **kwargs):
        return {**super(ExpenseCreateView, self).get_context_data(**kwargs), **{'group_id': self.kwargs['group_id']}}


def summary(request):
    paid_expenses = Expense.objects.filter(creator=request.user)
    in_debt_users = {}
    for paid_expense in paid_expenses:
        # paid_expenses = Expense()
        records_of_paid_expenses = Record.objects.filter(expense=paid_expense)
        if len(records_of_paid_expenses):
            in_debt_users[paid_expense.title] = [(
                paid_expense.amount,
                paid_expense.expense_attachment.url if paid_expense.expense_attachment else '',
                record.user,
                record.percent_of_share * paid_expense.amount / 100
            ) for record in records_of_paid_expenses]

    return render(request, 'pages/summary_of_expenses.html',
                  context={'expenses': in_debt_users, 'creator': request.user})
