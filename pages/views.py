from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


@login_required
class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'
