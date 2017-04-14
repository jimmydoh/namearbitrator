# nampoll/forms.py
from django import forms

from .models import Suggestion

class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ['name', 'suggestion_type', 'gender']
        widgets = {
            'name': forms.TextInput(
                attrs={'id': 'id_name', 'class': 'form-control form-control-lg', 'required': True, 'placeholder': 'Enter suggestion...'}
                ),
            'suggestion_type': forms.RadioSelect(
                attrs={'id': 'id_suggestion_type',}
                ),
            'gender': forms.RadioSelect(
                attrs={'id': 'id_gender',}
                ),
            }
    
