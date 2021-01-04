from django.forms import ModelForm, Form, CharField
from django import forms
from .models import Project, Section

class ProjectForm(Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    section_owner = forms.ModelChoiceField(queryset=Section.objects.all())
