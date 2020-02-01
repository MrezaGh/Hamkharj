import re

from django import forms
from django.contrib.gis import forms as g_forms

from expense.models import Expense, Record, ExpenseCategory
from group.models import Group


user_share_pattern = re.compile(r'^user_(?P<user_id>\d+)_share$')


class ExpenseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = self.get_users()
        for user_id, user_email in users:
            field_name = self.get_user_field_name(user_id)
            self.fields[field_name] = forms.DecimalField(
                max_digits=9,
                decimal_places=1,
                label=f'share of user {user_email}'
            )
            self.initial[field_name] = 0

    @staticmethod
    def get_user_field_name(user_id):
        return f"user_{user_id}_share"

    def get_users(self):
        raise NotImplementedError

    def save(self, **kwargs):
        expense = super(ExpenseForm, self).save(**kwargs)
        for key in filter(user_share_pattern.match,  self.cleaned_data):
            user_id = int(user_share_pattern.match(key)['user_id'])
            percentage = self.cleaned_data[key]
            if user_id != self.cleaned_data.get("creator", self.instance.creator).id:
                Record.objects.update_or_create(
                    expense=expense, user_id=user_id, defaults=dict(percent_of_share=percentage),
                )
        return expense


class ExpenseCreateForm(ExpenseForm):

    def __init__(self, *args, **kwargs):
        gid = kwargs.pop("gid", None)
        self.group = Group.objects.get(pk=gid)
        super(ExpenseCreateForm, self).__init__(*args, **kwargs)
        self.fields["creator"].choices = self.get_users()
        self.fields["location"] = g_forms.PointField()

    def get_users(self):
        return self.group.users.values_list('id', 'email')

    class Meta:
        model = Expense
        fields = ["title", "amount", "category", "description", "expense_attachment", "creator", "location"]


class ExpenseUpdateForm(ExpenseForm):

    def __init__(self, *args, **kwargs):
        super(ExpenseUpdateForm, self).__init__(*args, **kwargs)
        for user_id, _ in self.get_users():
            self.initial[self.get_user_field_name(user_id)] = int(self.instance.records.get(
                user_id=user_id
            ).percent_of_share)

    def get_users(self):
        if not self.instance:
            return []
        return self.instance.records.values_list('user', 'user__email')

    class Meta:
        model = Expense
        fields = ["title", "amount", "category", "description", "expense_attachment"]


class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ('title', )
