from django.urls import path

from .views import group_create_view, AddToGroup, GroupSettings, DeleteUser

urlpatterns = [
    path("create-group/", group_create_view, name="create_group"),
    path("update-group/", AddToGroup.as_view(), name="update_group"),
    path("update-group/<int:group_id>", AddToGroup.as_view(), name="update_group"),
    path("group-settings/<int:group_id>", GroupSettings.as_view(), name="group_settings"),
    path("<int:group_id>/delete-user/<str:user_email>", DeleteUser.as_view(), name="delete_user"),
]
