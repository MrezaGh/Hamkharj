from django.urls import path

from .views import GroupCreate

urlpatterns = [
    path("create-group/", GroupCreate.as_view(), name="create_group"),
]
