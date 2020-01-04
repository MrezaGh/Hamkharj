from django.views import View
from django.shortcuts import render, redirect

from .models import CustomUser
from .forms import AccountSettingsForm


class AccountSettings(View):
    template_name = 'account/settings.html'
    form_class = AccountSettingsForm

    def get(self, request, *args, **kwargs):
        CustomUser.objects.get(pk=request.user.id)
        form = self.form_class(request=request)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request=request)
        if form.is_valid():
            form.save()
            return redirect("panel")
        return render(request, self.template_name, {"form": form})



