from django.db.models import F, Value
from django.db.models.functions import Concat
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from group.models import Group
from .forms import ExpenseCreateForm, ExpenseUpdateForm, ExpenseCategoryForm
from .models import Expense


class ExpenseCreateView(CreateView):
    template_name = 'pages/create_expense.html'
    form_class = ExpenseCreateForm
    success_url = reverse_lazy('panel')

    def get_form_kwargs(self):
        kwargs = super(ExpenseCreateView, self).get_form_kwargs()
        kwargs.update(gid=self.kwargs['group_id'])
        return kwargs

    def get_context_data(self, **kwargs):
        return {**super(ExpenseCreateView, self).get_context_data(**kwargs), **{'group_id': self.kwargs['group_id']}}


class ExpenseUpdateView(UpdateView):
    template_name = 'pages/update_expense.html'
    queryset = Expense.objects.all()
    pk_url_kwarg = 'expense_id'
    form_class = ExpenseUpdateForm
    success_url = reverse_lazy('summary-of-expenses')

    def get_queryset(self):
        return self.queryset.filter(creator=self.request.user)


class ExpenseSummaryView(ListView):
    template_name = 'pages/summary_of_expenses.html'
    queryset = Expense.objects.all()

    def get_queryset(self):
        return self.queryset.filter(creator=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(ExpenseSummaryView, self).get_context_data(*args, **kwargs)
        context.update(
            creator=self.request.user,
            expense_list=(
                (
                    expense,
                    expense.records.annotate(
                        name=Concat(F('user__first_name'), Value(' '), F('user__last_name')),
                        debt_share=F('percent_of_share') * F('expense__amount') / 100,
                    ).values(
                        'name',
                        'debt_share',
                    )
                )
                for expense in context['expense_list']
            )
        )
        return context


class CategoryCreateView(CreateView):
    template_name = 'pages/create_category.html'
    form_class = ExpenseCategoryForm

    def get_success_url(self):
        return f'/expenses/create-expense/{self.kwargs["group_id"]}'

    def form_valid(self, form):
        group = Group.objects.filter(users=self.request.user.id, id=self.kwargs['group_id']).first()
        if not group:
            form.add_error(None, 'You do not have permission to add expense categories to this group.')
            return self.form_invalid(form)
        form.instance.group = group
        return super(CategoryCreateView, self).form_valid(form)
