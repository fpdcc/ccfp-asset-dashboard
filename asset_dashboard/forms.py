from django.forms import ModelForm, CharField, TextInput, Textarea
from .models import Project, Section, ProjectScore
from django.core.validators import MaxValueValidator, MinValueValidator

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'section_owner']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'})
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

    def __init__(self, *args, **kwargs):
        super(ProjectScoreForm, self).__init__(*args, **kwargs)

        min_value = 1
        max_value = 5
        
        for field_name, field in self.fields.items():
            field.widget.attrs['min'] = min_value
            field.widget.attrs['max'] = max_value
            # field.validators.append(MaxValueValidator(max_value))
            # field.validators.append(MinValueValidator(min_value))
