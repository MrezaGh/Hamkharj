from django import forms
from django.forms import ValidationError

from users.models import CustomUser
from .models import Friendship


class AddFriendForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        self.friendship = None
        self.request = kwargs.pop("request")

        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        try:
            user = self.request.user
            new_friend = CustomUser.objects.all().filter(email=self.cleaned_data["email"]).get()
            friendship = Friendship(user_id=user, friend_id=new_friend)
            self.friendship = friendship
            return self.cleaned_data
        except:
            raise ValidationError("Enter a valid user email.")

    def save(self, **kwargs):
        self.friendship.save()
