from django import forms
from django.forms import ValidationError

from group.models import Group
from users.models import CustomUser


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
