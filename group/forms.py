from django import forms
from django.forms import ValidationError

from group.models import Group
from users.models import CustomUser


class CreateGroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        users_email = list()
        users = list()
        self.fields["title"] = forms.CharField(max_length=200)
        for i, user in enumerate(CustomUser.objects.exclude(email=self.user).all()):
            users_email.append(user.email)
            users.append(user)
        self.fields["users"] = forms.MultipleChoiceField(choices=zip(users_email, users), required=False)
        self.fields["description"] = forms.CharField(max_length=500, required=False)

    def save(self, **kwargs):
        group = self.instance
        group.title = self.cleaned_data["title"]
        group.creator = self.user
        group.description = self.cleaned_data["description"]
        group.save()
        for user in self.cleaned_data["users"]:
            group.users.add(CustomUser.objects.filter(email=user).get())

    class Meta:
        model = Group
        fields = ["title", "users", "description"]


class AddToGroupForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        try:
            user = self.request.user
            group = Group.objects.all().filter(creator=user).get()
            new_user = (
                CustomUser.objects.all().filter(email=self.cleaned_data["email"]).get()
            )
            group.users.add(new_user)
            self.group = group
            return self.cleaned_data
        except:
            raise ValidationError("Enter a valid user email.")

    def save(self, **kwargs):
        self.group.save()
