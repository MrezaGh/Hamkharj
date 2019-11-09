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


# class ExpenseCreate(CreateView):
#     model = Expense
#     fields = ["title", "user", "amount", "description"]
#     template_name = "pages/create_expense.html"
#     success_url = reverse_lazy("panel")
#
#     def form_valid(self, form):
#         form.instance.creator = self.request.user
#         return super(ExpenseCreate, self).form_valid(form)
