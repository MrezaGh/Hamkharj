from django.urls import path

from .views import HomePageView, AboutPageView, expense_create_view

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("create-expense/", expense_create_view, name="create_expense"),
]
