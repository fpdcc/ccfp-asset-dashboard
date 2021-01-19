from django.forms import ModelForm, CharField, TextInput, Textarea
from .models import Project, Section, ProjectScore, ProjectCategory

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'section_owner', 'category']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control w-50'}),
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
        # widgets = {
        #     'category': Select(attrs={'class': 'form-control'}),
        #     'subcategory': Select(attrs={'class': 'form-control'})
        # }

    def __init__(self, *args, **kwargs):
        super(ProjectCategoryForm, self).__init__(*args, **kwargs)
        # self.fields['category'].queryset = self.initial['category']
        # self.fields['subcategory'].queryset = self.initial['subcategory']
        category_choices = ProjectCategory.objects.values_list('id', 'category')
        subcategory_choices = ProjectCategory.objects.values_list('id', 'subcategory')
        category_widget = ChoiceField(widget=Select(choices=ProjectCategory.objects.values_list('id', 'category')), initial={'category': self.initial['category']})
        subcategory_widget = ChoiceField(widget=Select(choices=ProjectCategory.objects.values_list('id', 'subcategory')), initial={'subcategory': self.initial['subcategory']})
        self.fields['category'].widget = category_widget #Select(choices=ProjectCategory.objects.values_list('id', 'category')) #, initial={'category': self.initial['category']})
        self.fields['subcategory'].widget = subcategory_widget #Select(choices=ProjectCategory.objects.values_list('id', 'subcategory')) #, initial={'subcategory': self.initial['subcategory']})
