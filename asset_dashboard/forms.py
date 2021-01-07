from django.forms import ModelForm, CharField
from django import forms
from .models import Project, Section, ProjectScore

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'section_owner']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'})
        }


class ProjectScoreForm(ModelForm):
    class Meta:
        model = ProjectScore
        fields = [
            'core_mission_score',
            'operations_impact_score',
            'sustainability_score',
            'ease_score',
            'geographic_distance_score',
            'social_equity_score'
        ]
