from django.urls import path

from .views import group_create_view, AddToGroup

urlpatterns = [
    path("create-group/", group_create_view, name="create_group"),
    path("update-group/", AddToGroup.as_view(), name="update_group"),
    path("update-group/<int:group_id>", AddToGroup.as_view(), name="update_group"),

]
