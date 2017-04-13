# namepoll/urls.py
from django.conf.urls import url
from . import views

# We are adding a URL called /home
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^suggest$', views.suggest, name='suggest'),
    url(r'^submit_suggestion$', views.submit_suggestion),
    url(r'^remove_suggestion$', views.remove_suggestion),
    url(r'^suggestions$', views.suggestions, name='suggestions'),
]
