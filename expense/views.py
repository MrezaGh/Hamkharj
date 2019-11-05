from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Expense

class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/home.html'


class ExpenseCreate(CreateView):
    model = Expense
    fields = '__all__'
    fields_order = ['title']
    template_name = 'pages/create_expense.html'
    success_url= reverse_lazy('home')

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'
