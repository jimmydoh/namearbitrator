# namepoll/views.py
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import SuggestionForm
from .models import Suggestion, Selector

import json

@login_required(login_url="login/")
def home(request):
    form = SuggestionForm()
    return render(request, 'suggest.html',{'form': form})

@login_required(login_url="login/")
def suggest(request):
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            #Save data

            return render(request, 'suggest.html',{'form': form})

    else:
        form = SuggestionForm()

    return render(request, 'suggest.html',{'form': form})

@login_required(login_url="login/")
def submit_suggestion(request):
    if request.method == 'POST':
        suggestion_name = request.POST.get('name')
        suggestion_suggestion_type = request.POST.get('suggestion_type')
        suggestion_gender = request.POST.get('gender')
        response_data = {}

        #Check the data
        if Suggestion.objects.filter(selector=Selector.objects.get(account=request.user)).filter(gender=suggestion_gender).filter(name__iexact=suggestion_name).count() > 0:
            #Name already exists
            response_data['result'] = 'Failure'
            response_data['html_message'] = '<div class="alert alert-danger">You have already entered <strong>' + suggestion_name + '</strong> in the past</div>'
        else:
            suggestion = Suggestion(name=suggestion_name, suggestion_type=suggestion_suggestion_type, gender=suggestion_gender, selector=Selector.objects.get(account=request.user))
            suggestion.save()

            response_data['result'] = 'Success'
            response_data['html_message'] = '<div class="alert alert-success"><strong>' + suggestion.name + '</strong> has been added as a <strong>' + suggestion.get_suggestion_type_display() + '</strong></div>'
            response_data['pk'] = suggestion.pk
            response_data['name'] = suggestion.name
            response_data['suggestion_type'] = suggestion.get_suggestion_type_display()
            response_data['gender'] = suggestion.get_gender_display()
            response_data['selector'] = suggestion.selector.account.username

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

@login_required(login_url="login/")
def remove_suggestion(request):
    if request.method == 'POST':
        suggestion_name = request.POST.get('name')
        suggestion_pk = request.POST.get('pk')
        response_data = {}

        #Check the data
        if Suggestion.objects.filter(selector=Selector.objects.get(account=request.user)).filter(pk=suggestion_pk).count() > 0:
            #Object exists and belongs to user
            Suggestion.objects.get(pk=suggestion_pk).delete()

            response_data['result'] = 'Success'
            response_data['html_message'] = '<div class="alert alert-success"><strong>' + suggestion_name + '</strong> has been deleted</div>'
            response_data['pk'] = suggestion_pk
            response_data['name'] = suggestion_name
            
        else:
            response_data['result'] = 'Failure'
            response_data['html_message'] = '<div class="alert alert-danger">Unable to delete the object</div>'
            

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

@login_required(login_url="login/")
def suggestions(request):
    # Retrieve existing suggestion set
    girl_set = Suggestion.objects.filter(selector=Selector.objects.get(account=request.user)).filter(gender=Suggestion.GIRL)
    boy_set = Suggestion.objects.filter(selector=Selector.objects.get(account=request.user)).filter(gender=Suggestion.BOY)

    parameters = {
            'girl_set': girl_set,
            'boy_set': boy_set,
        }
    
    return render(request, 'suggestions.html', parameters)
