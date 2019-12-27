from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView

from expense.models import Expense, Record
from group.models import Group
from friend.models import Friendship


class PanelView(LoginRequiredMixin, TemplateView):
    template_name = "pages/home.html"

    def get(self, request, **kwargs):
        user = request.user

        creator_expenses = Expense.objects.filter(Q(creator=user.pk))
        balance = dict()
        for expense in creator_expenses:
            amount = expense.amount
            records = Record.objects.filter(expense=expense)
            for record in records:
                record_user = record.user
                shared_amount = record.percent_of_share * amount / 100
                if record_user in balance.keys():
                    balance[record_user] += shared_amount
                else:
                    balance[record_user] = shared_amount

        user_records = Record.objects.filter(user=user)
        for record in user_records:
            expense = record.expense
            if expense.creator in balance.keys():
                balance[expense.creator] -= (
                        expense.amount * record.percent_of_share / 100
                )
            else:
                balance[expense.creator] = (
                        -expense.amount * record.percent_of_share / 100
                )
        balance["Overall Balance"] = sum(list(balance.values()))

        created_groups = Group.objects.filter(creator=user.pk).all()
        added_groups = Group.objects.exclude(creator=user.pk).filter(users=user.pk).all()
        groups = [(elem.pk, elem.title, elem.description, elem.creator) for elem in created_groups]
        groups += [(elem.pk, elem.title, elem.description, elem.creator) for elem in added_groups]

        friendships = Friendship.objects.all().filter(user_id=user)
        friends = [friendship.friend_id for friendship in friendships]

        return render(
            request,
            "pages/home.html",
            {
                "balance": zip(list(balance.keys()), list(balance.values())),
                "groups": groups,
                "friends": friends
            },
        )
