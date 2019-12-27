from django.urls import path
from .views import AddFriendView

urlpatterns = [
    path("add-friend/", AddFriendView.as_view(), name="add_friend"),
    # path("update-group/", AddToGroup.as_view(), name="update_group"),
    # path("update-group/<int:group_id>", AddToGroup.as_view(), name="update_group"),
]