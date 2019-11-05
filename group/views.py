from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Group


class GroupCreate(CreateView):
    model = Group
    fields = "__all__"
    fields_order = ["title"]
    template_name = "pages/create_expense.html"
    success_url = reverse_lazy("home")
