# jadauth/views.py
from django.shortcuts import render
from django.contrib.auth import views as auth_views

def login(request, *args, **kwargs):
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
    return auth_views.login(request, *args, **kwargs)

def logout(request, *args, **kwargs):
    return auth_views.logout(request, *args, **kwargs)


