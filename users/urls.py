from django.urls import path

from .views import AccountSettings, UserRecentActivities

urlpatterns = [
    path("", AccountSettings.as_view(), name="account-settings"),
    path("recent-activities", UserRecentActivities.as_view(), name="recent-activities"),
]
