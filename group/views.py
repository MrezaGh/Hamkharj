from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView
from expense.models import Expense
from .models import Group
from users.models import CustomUser
from friend.models import Friendship
from .forms import AddToGroupForm, CreateGroupForm, GroupSettingsForm


@login_required
def group_create_view(request):
    form = CreateGroupForm(request.POST or None, user=request.user)
    if form.is_valid():
        form.save()
        return redirect("panel")
    context = {"form": form}
    return render(request, "pages/create_group.html", context)


class AddToGroup(View):
    form_class = AddToGroupForm
    template_name = "pages/add_to_group.html"

    def get(self, request, *args, **kwargs):
        self.user = request.user
        g_id = kwargs.pop('group_id')
        form = self.form_class(request=request, g_id=g_id)
        return render(request, self.template_name,
                      {"form": form, "group_id": g_id, "members": self.members(g_id), "users": self.friends})

    def post(self, request, **kwargs):
        self.user = request.user
        g_id = kwargs.pop('group_id')
        form = self.form_class(request.POST, request=request, g_id=g_id)
        if form.is_valid():
            form.save()
            return redirect("panel")
        return render(request, self.template_name,
                      {"form": form, "group_id": g_id, "members": self.members(g_id), "users": self.friends})

    def members(self, g_id):
        members = Group.objects.get(pk=g_id).users.all()
        members_email = [user.email for user in members]
        self.users = CustomUser.objects.exclude(email__in=members_email).all()
        self.friends = [friendship.friend_id for friendship in Friendship.objects.filter(user_id=self.user) if
                        friendship.friend_id.email not in members_email]
        return members_email


class GroupSettings(View):
    template_name = "pages/group_update.html"
    form_class = GroupSettingsForm

    def get(self, request, *args, **kwargs):
        g_id = kwargs.pop('group_id')
        form = self.form_class(request=request, g_id=g_id)
        return render(request, self.template_name, {"form": form, "members": self.members(g_id), "id": g_id})

    def post(self, request, **kwargs):
        g_id = kwargs.pop('group_id')
        form = self.form_class(request.POST, request=request, g_id=g_id)
        if form.is_valid():
            form.save()
            return redirect("panel")
        return render(request, self.template_name, {"form": form, "members": self.members(g_id), "users": self.users})

    def members(self, g_id):
        members = Group.objects.get(pk=g_id).users.all()
        members_email = [user.email for user in members]
        self.users = CustomUser.objects.exclude(email__in=members_email).all()
        return members_email


class DeleteUser(View):
    def get(self, request, *args, **kwargs):
        g_id = kwargs.pop('group_id')
        group = Group.objects.get(pk=g_id)
        user_email = kwargs.pop('user_email')

        group.users.remove(CustomUser.objects.get(email=user_email))
        group.save()

        return redirect("group_settings", group_id=g_id)


class AddUser(View):
    def get(self, request, *args, **kwargs):
        g_id = kwargs.pop('group_id')
        group = Group.objects.get(pk=g_id)
        user_email = kwargs.pop('user_email')

        group.users.add(CustomUser.objects.get(email=user_email))

        group.save()

        return redirect("group_settings", group_id=g_id)
