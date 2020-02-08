from django.views import View
from django.views.generic import DetailView
from django.shortcuts import render, redirect
from invitations.utils import get_invitation_model

from expense.models import Expense, ExpenseCategory, Record
from friend.models import Friendship
from group.models import Group
from .models import CustomUser
from .forms import AccountSettingsForm


class AccountSettings(View):
    template_name = 'account/settings.html'
    form_class = AccountSettingsForm

    def get(self, request, *args, **kwargs):
        CustomUser.objects.get(pk=request.user.id)
        form = self.form_class(request=request)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request=request)
        if form.is_valid():
            form.save()
            return redirect("panel")
        return render(request, self.template_name, {"form": form})


class UserRecentActivities(DetailView):
    template_name = 'pages/user_recent_activities.html'
    registered_history_models = (
        ('Expenses', Expense, ('title', 'amount', 'description', 'expense_attachment', 'category', )),
        ('Categories', ExpenseCategory, ('title', 'group')),
        ('Friends', Friendship, ()),
        ('Groups', Group, ('title', 'description')),
        ('Invitations', get_invitation_model(), ()),
    )

    def get_object(self, queryset=None):\
        return self.request.user

    def get_user_history(self, model):
        user = self.get_object()
        history = model.history.filter(history_user_id=user.id).order_by('id', 'history_date')
        return list(history)

    def get_context_data(self, **kwargs):
        context = super(UserRecentActivities, self).get_context_data(**kwargs)

        activities = dict()
        for key, model, history_fields in self.registered_history_models:
            user_history = self.get_user_history(model)
            objects_map = {obj.id: obj for obj in model.objects.filter(id__in=[rec.id for rec in user_history])}
            history = list()
            last_record_obj_id = None
            for idx, record in enumerate(user_history):
                if record.id != last_record_obj_id:
                    history.append({'created': True, 'object': objects_map[record.id], 'datetime': record.history_date})
                    last_record_obj_id = record.id
                else:
                    modified_fields = list()
                    for field in history_fields:
                        old_val = getattr(user_history[idx - 1], field)
                        new_val = getattr(record, field)
                        if new_val != old_val:
                            modified_fields.append((field, old_val, new_val))
                    if key == 'Expenses':
                        expense = objects_map[record.id]

                        def get_expense_records_history(_expense, **filters):
                            return {rec.id: rec for rec in Record.history.filter(expense=_expense, **filters)}
                        old_expense_records_history = get_expense_records_history(
                            expense,
                            history_date__lt=record.history_date
                        )
                        new_expense_records_history = get_expense_records_history(
                            expense,
                            history_date__gte=record.history_date
                        )

                        for record_id in set(old_expense_records_history) & set(new_expense_records_history):
                            old_record = old_expense_records_history[record_id]
                            new_record = new_expense_records_history[record_id]
                            old_share, new_share = old_record.percent_of_share, new_record.percent_of_share
                            if old_share != new_share:
                                user = new_record.user
                                user_name = f'{user.first_name or ""} {user.last_name or ""}' or user.username
                                modified_fields.append((
                                    f'share of {user_name}',
                                    f'{old_share}%',
                                    f'{new_share}%'
                                ))
                    if modified_fields:
                        history.append({
                            'created': False,
                            'object': objects_map[record.id],
                            'modified_fields': modified_fields,
                            'datetime': record.history_date
                        })

            activities.update({key: list(reversed(history))})
        context.update(activities=activities)
        return context
