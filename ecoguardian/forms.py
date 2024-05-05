
from django import forms
from .models import IncidentCategory, IncidentReport
from django.forms import ModelForm

class IncidentReportForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea)
    location = forms.CharField(required=False)
    date = forms.DateField(widget=forms.SelectDateWidget)
    incident_categories = forms.MultipleChoiceField(
        choices=IncidentCategory.CATEGORY_CHOICES,
        widget=forms.SelectMultiple,
        required=False,
        label='Incident category'
    )
    evidence = forms.FileField(required=False)


# class AdminDescriptionForm(forms.Form):
#     admin_description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter incident description'}))

class AdminDescriptionForm(ModelForm):
    class Meta:
        model = IncidentReport
        fields = ['admin_description', 'status']
