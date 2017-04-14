# namepoll/views.py
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import SuggestionForm
from .models import Suggestion, Selector, SelectionGroup

import json
import datetime

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

@login_required(login_url="login/")
def analytics(request):
    user_current = Selector.objects.get(account=request.user)
    user_current_selection_group = SelectionGroup.objects.get(selector__account=user_current.account)
    user_partner = user_current_selection_group.selector_set.exclude(account=request.user).get()

    #Count data

    #Current User
    stat_user_current_suggestions = {
            'girl': Suggestion.objects.filter(selector=user_current).filter(gender=Suggestion.GIRL).count(),
            'boy': Suggestion.objects.filter(selector=user_current).filter(gender=Suggestion.BOY).count(),
            'yes': Suggestion.objects.filter(selector=user_current).filter(suggestion_type=Suggestion.YES).count(),
            'maybe': Suggestion.objects.filter(selector=user_current).filter(suggestion_type=Suggestion.MAYBE).count(),
            'no': Suggestion.objects.filter(selector=user_current).filter(suggestion_type=Suggestion.NO).count(),
            'total': Suggestion.objects.filter(selector=user_current).count(),
        }

    #Partner
    stat_user_partner_suggestions = {
            'girl': Suggestion.objects.filter(selector=user_partner).filter(gender=Suggestion.GIRL).count(),
            'boy': Suggestion.objects.filter(selector=user_partner).filter(gender=Suggestion.BOY).count(),
            'yes': Suggestion.objects.filter(selector=user_partner).filter(suggestion_type=Suggestion.YES).count(),
            'maybe': Suggestion.objects.filter(selector=user_partner).filter(suggestion_type=Suggestion.MAYBE).count(),
            'no': Suggestion.objects.filter(selector=user_partner).filter(suggestion_type=Suggestion.NO).count(),
            'total': Suggestion.objects.filter(selector=user_partner).count(),
        }
    
    #Totals
    stat_suggestions_total = Suggestion.objects.filter(selector=user_current).count() + Suggestion.objects.filter(selector=user_partner).count()

    #Comparison Data

    date_from = datetime.datetime.now() #- datetime.timedelta(days=1)
    #Retrieve suggestions of current user
    suggestions = Suggestion.objects.filter(selector=user_current, last_checked__lte=date_from)
    matches_yesyes = list()
    matches_yesmaybe = list()
    matches_yesno = list()
    matches_maybeyes = list()
    matches_maybemaybe = list()
    matches_maybeno = list()
    matches_noyes = list()
    matches_nomaybe = list()
    matches_nono = list()
    matches_nomatch = 0;
    for suggestion in suggestions:
        #For current user YES
        if suggestion.suggestion_type==Suggestion.YES:
            match_yesyes = Suggestion.objects.filter(selector=user_partner,name=suggestion.name,gender=suggestion.gender,suggestion_type=Suggestion.YES).first()
            if match_yesyes:
                matches_yesyes.append(match_yesyes)
            else:
                match_yesmaybe = Suggestion.objects.filter(selector=user_partner,name=suggestion.name,gender=suggestion.gender,suggestion_type=Suggestion.MAYBE).first()
                if match_yesmaybe:
                    matches_yesmaybe.append(match_yesmaybe)
                else:
                    match_yesno = Suggestion.objects.filter(selector=user_partner,name=suggestion.name,gender=suggestion.gender,suggestion_type=Suggestion.NO).first()
                    if match_yesno:
                        matches_yesno.append(match_yesno)
                    else:
                        matches_nomatch = matches_nomatch + 1
        #For current user MAYBE
        elif suggestion.suggestion_type==Suggestion.MAYBE:
            match_maybeyes = Suggestion.objects.filter(selector=user_partner,name=suggestion.name,gender=suggestion.gender,suggestion_type=Suggestion.YES).first()
            if match_maybeyes:
                matches_maybeyes.append(match_maybeyes)
            else:
                match_maybemaybe = Suggestion.objects.filter(selector=user_partner,name=suggestion.name,gender=suggestion.gender,suggestion_type=Suggestion.MAYBE).first()
                if match_maybemaybe:
                    matches_maybemaybe.append(match_maybemaybe)
                else:
                    match_maybeno = Suggestion.objects.filter(selector=user_partner,name=suggestion.name,gender=suggestion.gender,suggestion_type=Suggestion.NO).first()
                    if match_maybeno:
                        matches_maybeno.append(match_maybeno)
                    else:
                        matches_nomatch = matches_nomatch + 1
        #For current user NO
        elif suggestion.suggestion_type==Suggestion.NO:
            match_noyes = Suggestion.objects.filter(selector=user_partner,name=suggestion.name,gender=suggestion.gender,suggestion_type=Suggestion.YES).first()
            if match_noyes:
                matches_noyes.append(match_noyes)
            else:
                match_nomaybe = Suggestion.objects.filter(selector=user_partner,name=suggestion.name,gender=suggestion.gender,suggestion_type=Suggestion.MAYBE).first()
                if match_nomaybe:
                    matches_nomaybe.append(match_nomaybe)
                else:
                    match_nono = Suggestion.objects.filter(selector=user_partner,name=suggestion.name,gender=suggestion.gender,suggestion_type=Suggestion.NO).first()
                    if match_nono:
                        matches_nono.append(match_nono)
                    else:
                        matches_nomatch = matches_nomatch + 1
        else:
            matches_nomatch = matches_nomatch + 1
            
    matches = {
        'matches_yesyes': matches_yesyes,
        'matches_yesmaybe': matches_yesmaybe,
        'matches_yesno': matches_yesno,
        'matches_maybeyes': matches_maybeyes,
        'matches_maybemaybe': matches_maybemaybe,
        'matches_maybeno': matches_maybeno,
        'matches_noyes': matches_noyes,
        'matches_nomaybe': matches_nomaybe,
        'matches_nono': matches_nono,
        }

    matches_count = {
        'matches_yesyes': len(matches_yesyes),
        'matches_yesmaybe': len(matches_yesmaybe),
        'matches_yesno': len(matches_yesno),
        'matches_maybeyes': len(matches_maybeyes),
        'matches_maybemaybe': len(matches_maybemaybe),
        'matches_maybeno': len(matches_maybeno),
        'matches_noyes': len(matches_noyes),
        'matches_nomaybe': len(matches_nomaybe),
        'matches_nono': len(matches_nono),
        'matches_nomatch': matches_nomatch,
        }

    parameters = {
            'user_current': user_current,
            'user_current_selection_group': user_current_selection_group,
            'suggestions': suggestions,
            'matches': matches,
            'matches_count': matches_count,
            'user_partner': user_partner,
            'stat_user_current_suggestions': stat_user_current_suggestions,
            'stat_user_partner_suggestions': stat_user_partner_suggestions,
            'stat_suggestions_total': stat_suggestions_total,
        }
    
    return render(request, 'analytics.html', parameters)
