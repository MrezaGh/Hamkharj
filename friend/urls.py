from django.urls import path
from .views import AddFriendView, InviteFriend

urlpatterns = [
    path("add-friend/", AddFriendView.as_view(), name="add_friend"),
    path("invite/", InviteFriend.as_view(), name="invite_friend")
]