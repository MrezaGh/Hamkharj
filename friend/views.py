from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from .forms import AddFriendForm, InviteFriendForm
from .models import Friendship
from users.models import CustomUser


@method_decorator(login_required, 'dispatch')
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


class InviteFriend(View):
    form_class = InviteFriendForm
    template_name = "pages/invite_friend.html"

    def get(self, request):
        form = self.form_class(request=request)
        return render(request, self.template_name, {"form": form})

    def post(self, request, **kwargs):
        form = self.form_class(request.POST, request=request)
        if form.is_valid():
            form.save()
            print(form)
            return render(request, 'pages/invite_link.html', {"invite_link": form.invite_url, 'friend_mail': form.data['email']})

        return render(request, self.template_name, {"form": form})
