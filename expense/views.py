from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Expense
from .forms import ExpenseForm

class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "pages/home.html"


# class ExpenseCreate(CreateView):
#     model = Expense
#     fields = ["title", "user", "amount", "description"]
#     template_name = "pages/create_expense.html"
#     success_url = reverse_lazy("home")
#
#     def form_valid(self, form):
#         form.instance.creator = self.request.user
#         return super(ExpenseCreate, self).form_valid(form)


def expense_create_view(request):
    form = ExpenseForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = ExpenseForm()
    context = {
        'form': form
    }
    return render(request, "pages/create_expense.html", context)


class AboutPageView(TemplateView):
    template_name = "pages/about.html"
