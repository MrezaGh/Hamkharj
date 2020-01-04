from allauth.account.forms import SignupForm
from django import forms

from .models import CustomUser
from allauth.account.models import EmailAddress


class AccountSettingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.user = self.request.user
        super().__init__(*args, **kwargs)

        self.fields["first_name"] = forms.CharField(max_length=200, required=False, initial=self.user.first_name)
        self.fields["last_name"] = forms.CharField(max_length=200, required=False, initial=self.user.last_name)
        self.fields["email"] = forms.CharField(max_length=200, required=False, initial=self.user.email)

    def save(self, **kwargs):
        user = CustomUser.objects.get(pk=self.user.id)
        for changed in self.changed_data:
            if changed == 'email':
                email_rel = EmailAddress.objects.get(user_id=user.id)
                email_rel.email = self.cleaned_data[changed]
                email_rel.save()
            setattr(user, changed, self.cleaned_data[changed])
        user.save()

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email"]


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
