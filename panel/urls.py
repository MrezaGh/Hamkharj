from django.urls import path

from .views import PanelView

urlpatterns = [
    path("", PanelView.as_view(), name="panel"),
]
