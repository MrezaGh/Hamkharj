from django.urls import path

from .views import AccountSettings

urlpatterns = [
    path("", AccountSettings.as_view(), name="account-settings"),
]
