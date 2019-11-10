from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView

from .forms import AddToGroupForm
from .models import Group


class GroupCreate(CreateView):
    model = Group
    fields = "__all__"
    fields_order = ["title"]
    template_name = "pages/create_expense.html"
    success_url = reverse_lazy("panel")


class AddToGroup(View):
    form_class = AddToGroupForm
    template_name = "pages/add_to_group.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(request=request)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST, request=request)
        if form.is_valid():
            form.save()
            return redirect("panel")
        return render(request, self.template_name, {"form": form})
