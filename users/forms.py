from allauth.account.forms import SignupForm
from django import forms

from .models import CustomUser


class CustomSignUpForm(SignupForm):
    first_name = forms.CharField(
        max_length=20,
        min_length=4,
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "First Name", "class": "form-control"}
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Last Name", "class": "form-control"}
        ),
    )
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(
            attrs={"placeholder": "Email", "class": "form-control"}
        ),
    )
    password1 = forms.CharField(
        label="Password",
        max_length=30,
        min_length=8,
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        ),
    )

    password2 = forms.CharField(
        label="Password",
        max_length=30,
        min_length=8,
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm Password", "class": "form-control"}
        ),
    )

    field_order = ["first_name", "last_name", "email", "password1", "password2"]

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CustomSignUpForm, self).save(request)

        # Add your own processing here.
        # group = Group.objects.create(creator=user)
        # group.save()
        # You must return the original result.
        return user

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )
