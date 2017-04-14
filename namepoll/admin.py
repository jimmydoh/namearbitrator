from django.contrib import admin

from .models import SelectionGroup, Selector, Suggestion

from django.contrib.auth.models import User

class SelectionGroupAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields':['name']}),
    ]
    list_display = ('__str__',)

class SelectorAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields':['account','selection_groups']}),
    ]
    list_display = ('__str__',Selector.suggestions,Selector.suggestions_yes,Selector.suggestions_maybe,Selector.suggestions_no)

class SuggestionAdmin(admin.ModelAdmin):
    readonly_fields = ['created','last_checked']
    fieldsets = [
        (None,  {'fields':['suggestion_type','gender','name','selector']}),
        ('Extra Info',{'fields':['created','last_checked'], 'classes':['collapse']}),
    ]
    list_display = ('__str__','suggestion_type','gender','selector',)

admin.site.register(SelectionGroup, SelectionGroupAdmin)
admin.site.register(Selector, SelectorAdmin)
admin.site.register(Suggestion, SuggestionAdmin)
