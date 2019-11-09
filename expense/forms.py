from django import forms

from expense.models import Expense, Record
from users.models import CustomUser


class ExpenseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.creator = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        users = CustomUser.objects.all()
        self.users = list()
        self.fields["title"] = forms.CharField(max_length=200)
        self.fields["description"] = forms.CharField(max_length=400)
        self.fields["amount"] = forms.DecimalField(max_digits=9, decimal_places=0)

        for i, user in enumerate(users):
            field_name = "user_%s_share" % (user.email,)
            self.fields[field_name] = forms.DecimalField(max_digits=9, decimal_places=1)
            self.users.append(user)
            self.initial[field_name] = 0

    def clean(self):
        i = 0
        field_name = "user_%s_share" % (self.users[i].email,)
        percentages = list()
        while self.cleaned_data.get(field_name):
            temp = self.cleaned_data[field_name]
            percentages.append(temp)
            i += 1
            if i < len(self.users):
                field_name = "user_%s_share" % (self.users[i].email,)
            else:
                break
        self.cleaned_data["users-expenses"] = {
            "users": self.users,
            "percentages": percentages,
        }

    def save(self, **kwargs):
        expense = self.instance
        expense.title = self.cleaned_data["title"]
        expense.description = self.cleaned_data["description"]
        expense.amount = self.cleaned_data["amount"]
        expense.creator = self.cleaned_data["creator"]
        expense.save()
        for user, percentage in zip(
            self.cleaned_data["users-expenses"]["users"],
            self.cleaned_data["users-expenses"]["percentages"],
        ):
            Record.objects.create(
                expense=expense, user=user, percent_of_share=percentage,
            )

    class Meta:
        model = Expense
        fields = ["title", "creator", "amount", "description"]
