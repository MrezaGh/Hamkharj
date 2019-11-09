from django.shortcuts import render

from .forms import ExpenseForm


def expense_create_view(request):
    form = ExpenseForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = ExpenseForm()
    context = {"form": form}
    return render(request, "pages/create_expense.html", context)


# class ExpenseCreate(CreateView):
#     model = Expense
#     fields = ["title", "user", "amount", "description"]
#     template_name = "pages/create_expense.html"
#     success_url = reverse_lazy("home")
#
#     def form_valid(self, form):
#         form.instance.creator = self.request.user
#         return super(ExpenseCreate, self).form_valid(form)
