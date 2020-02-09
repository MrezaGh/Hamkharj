import re

from django import forms
from django.contrib.gis import forms as g_forms
from django.contrib.gis.geos.point import Point
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
        # self.fields["location"] = g_forms.PointField()

        self.fields['latitude'] = forms.DecimalField(
            min_value=-90,
            max_value=90,
            required=False,
        )
        self.fields['longitude'] = forms.DecimalField(
            min_value=-180,
            max_value=180,
            required=False,
        )

    def get_users(self):
        return self.group.users.values_list('id', 'email')

    def save(self, **kwargs):
        expense = super(ExpenseCreateForm, self).save(**kwargs)
        if self.cleaned_data['latitude'] != '' and self.cleaned_data['longitude'] != '':
            expense.location = Point(float(self.cleaned_data['longitude']), float(self.cleaned_data['latitude']))
            expense.save(**kwargs)
        return expense

    class Meta:
        model = Expense
        fields = ["title", "amount", "category", "description", "expense_attachment", "creator"]


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
