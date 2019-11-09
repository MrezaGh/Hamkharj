from django import forms

from expense.models import Expense, Record
from users.models import CustomUser


class ExpenseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = CustomUser.objects.all()
        self.users = dict()
        self.fields["title"] = forms.CharField(max_length=200)
        self.fields["description"] = forms.CharField(max_length=400)
        self.fields["amount"] = forms.DeimalField(max_digits=9, decimal_places=0)

        for i, user in enumerate(users):
            field_name = "user_%s_share" % (user.email,)
            self.fields[field_name] = forms.DecimalField(max_digits=9, decimal_places=1)
            self.users[field_name] = user
            self.initial[field_name] = 0
        print(self.fields)

    def clean(self):
        temps = set()
        i = 0
        tmp_name = "user_%s_share" % (i,)
        field_name = "user_%s_share" % (self.users[tmp_name])
        users = list()
        percentages = list()
        while self.cleaned_data.get(field_name):
            temp = self.cleaned_data[field_name]
            users.append(self.users[field_name])
            percentages.append(temp)
            if temp in temps:
                self.add_error(field_name, "Duplicate")
            else:
                temps.add(temp)
            i += 1
            tmp_name = "user_%s_share" % (i,)
            field_name = "user_%s_share" % (self.users[tmp_name])
        self.cleaned_data["users-expenses"] = {
            "users": users,
            "percentages": percentages,
        }

    def save(self, **kwargs):
        expense = self.instance
        expense.title = self.cleaned_data["title"]
        expense.description = self.cleaned_data["description"]
        expense.amount = self.cleaned_data["amount"]

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
