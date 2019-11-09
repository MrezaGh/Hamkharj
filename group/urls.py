from django.urls import path

from .views import GroupCreate, AddToGroup

urlpatterns = [
    path("create-group/", GroupCreate.as_view(), name="create_group"),
    path("update-group/", AddToGroup.as_view(), name="update_group"),
]
