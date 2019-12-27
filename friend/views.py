from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from .forms import AddFriendForm
from .models import Friendship
from users.models import CustomUser


class AddFriendView(View):
    form_class = AddFriendForm
    template_name = "pages/add_friend.html"

    def get(self, request):
        form = self.form_class(request=request)
        friends = [friendship.friend_id for friendship in Friendship.objects.filter(user_id=request.user)]
        available_users = CustomUser.objects.exclude(email__in=friends)

        return render(request, self.template_name, {"form": form, "available_users": available_users})

    def post(self, request, **kwargs):
        form = self.form_class(request.POST, request=request)
        if form.is_valid():
            form.save()
            return redirect("panel")

        friends = [friendship.friend_id for friendship in Friendship.objects.filter(user_id=request.user)]
        available_users = CustomUser.objects.exclude(email__in=friends)

        return render(request, self.template_name, {"form": form, "available_users": available_users})
