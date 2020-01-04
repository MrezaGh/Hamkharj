from django.views import View
from django.shortcuts import render, redirect


class AccountSettings(View):
    template_name = 'account/settings.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)



