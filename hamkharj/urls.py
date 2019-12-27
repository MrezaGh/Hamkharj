from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.shortcuts import redirect


# fixme should be deleted
def landing(request):
    return redirect("panel")


urlpatterns = [
    # fixme should be deleted
    path("", landing, name="landing"),
    path("admin/", admin.site.urls),
    path("users/", include("django.contrib.auth.urls")),
    path("accounts/", include("allauth.urls")),
    path("", include("expense.urls")),
    path("group/", include("group.urls")),
    path("friend/", include("friend.urls")),
    path("panel/", include("panel.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls)),] + urlpatterns
