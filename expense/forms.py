import re

from django import forms

from expense.models import Expense, Record
from group.models import Group


user_share_pattern = re.compile(r'^user_(?P<user_id>\d+)_share$')


class ExpenseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        gid = kwargs.pop("gid", None)
        group = Group.objects.get(pk=gid)
        group_users = group.users.values_list('id', 'email')
        super().__init__(*args, **kwargs)
        self.fields["creator"].choices = group_users
        for user_id, user_email in group_users:
            field_name = f"user_{user_id}_share"
            self.fields[field_name] = forms.DecimalField(
                max_digits=9,
                decimal_places=1,
                label=f'share of user {user_email}'
            )
            self.initial[field_name] = 0

    def save(self, **kwargs):
        expense = super(ExpenseForm, self).save(**kwargs)
        for key in filter(user_share_pattern.match,  self.cleaned_data):
            user_id = int(user_share_pattern.match(key)['user_id'])
            percentage = self.cleaned_data[key]
            if user_id != self.cleaned_data["creator"].id:
                Record.objects.create(
                    expense=expense, user_id=user_id, percent_of_share=percentage,
                )
        return expense

    class Meta:
        model = Expense
        fields = ["title", "amount", "category", "description", "expense_attachment", "creator"]
