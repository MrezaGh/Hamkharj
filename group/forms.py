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

        group.users.add(self.user)
        for user in self.cleaned_data["users"]:
            group.users.add(CustomUser.objects.filter(email=user).get())

    class Meta:
        model = Group
        fields = ["title", "users", "description"]


class AddToGroupForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        self.group = None
        self.g_id = kwargs.pop("g_id")
        self.request = kwargs.pop("request")

        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        try:
            user = self.request.user
            group = Group.objects.get(pk=self.g_id)
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


class GroupSettingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.g_id = kwargs.pop("g_id")
        self.group = Group.objects.get(pk=self.g_id)
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        self.fields['title'] = forms.CharField(initial=self.group.title, max_length=30, required=False)
        self.fields['description'] = forms.CharField(initial=self.group.description, max_length=200, required=False)

    def save(self, **kwargs):
        for changed in self.changed_data:
            setattr(self.group, changed, self.cleaned_data[changed])
        self.group.save()

    class Meta:
        model = Group
        fields = ['title', 'description']
