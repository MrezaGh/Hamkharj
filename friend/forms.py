from django import forms
from django.forms import ValidationError
from django.urls import reverse
from invitations.utils import get_invitation_model

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


class InviteFriendForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        self.invite_url = None
        self.request = kwargs.pop("request")

        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        try:
            user = self.request.user
            Invitation = get_invitation_model()
            invite = Invitation.create(self.cleaned_data["email"], inviter=self.request.user)
            invite.send_invitation(self.request)
            invite_url = reverse('invitations:accept-invite', args=[invite.key])
            invite_url = self.request.build_absolute_uri(invite_url)
            self.invite_url = invite_url
            return self.cleaned_data
        except:
            import sys
            raise ValidationError(sys.exc_info())

    def save(self, **kwargs):
        pass
