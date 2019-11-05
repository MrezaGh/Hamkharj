from django.urls import path

from .views import HomePageView, AboutPageView, ExpenseCreate

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('create-expense/', ExpenseCreate.as_view(), name='create_expense')
]
