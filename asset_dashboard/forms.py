from django.forms import ModelForm, CharField, TextInput, Textarea, Select, CheckboxInput
from .models import Project, Section, ProjectScore, ProjectCategory, SenateDistrict, HouseDistrict, CommissionerDistrict, Zone
from django.forms import inlineformset_factory

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'section_owner', 'category', 'phase_completion']
        widgets = {
            'name': TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


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
        super().__init__(*args, **kwargs)

        model = self.Meta.model

        for field_name, field in self.fields.items():
            model_field = model._meta.get_field(field_name)
            min_validator, max_validator = model_field.validators

            field.widget.attrs['min'] = min_validator.limit_value
            field.widget.attrs['max'] = max_validator.limit_value
            field.widget.attrs['class'] = 'form-control'


class ProjectCategoryForm(ModelForm):
    class Meta:
        model = ProjectCategory
        fields = [
            'category',
            'subcategory'
        ]


SenateDistrictFormset = inlineformset_factory(Project, 
                                                SenateDistrict,
                                                fields=('name',), 
                                                extra=1, 
                                                widgets={'name': TextInput(attrs={'class': 'form-control'})})

HouseDistrictFormset = inlineformset_factory(Project, 
                                                HouseDistrict, 
                                                fields=('name',), 
                                                extra=1, 
                                                widgets={'name': TextInput(attrs={'class': 'form-control'})})

CommissionerDistrictFormset = inlineformset_factory(Project,
                                                    CommissionerDistrict,
                                                    fields=('name',),
                                                    extra=1,
                                                    widgets={'name': TextInput(attrs={'class': 'form-control'})})

ZoneFormset = inlineformset_factory(Project,
                                    Zone,
                                    fields=('name',),
                                    extra=1,
                                    widgets={'name': TextInput(attrs={'class': 'form-control'})})
