from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView

from expense.models import Expense


class PanelView(LoginRequiredMixin, TemplateView):
    template_name = "pages/home.html"

    def get(self, request, **kwargs):
        user = request.user
        expenses = Expense.objects.filter(Q(creator=user.pk))
        return render(request, "pages/home.html", {"expenses": list(expenses)})
