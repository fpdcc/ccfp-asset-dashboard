from django.forms import ModelForm, TextInput
from .models import Project, ProjectScore, ProjectCategory, SenateDistrict, HouseDistrict, CommissionerDistrict, Zone
from django.forms import inlineformset_factory


class StyledFormMixin(object):
    """
    Generic mixin to consistently style each form field's html <input> element.
    """

    def __init__(self, *args, **kwargs):
        super(StyledFormMixin, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProjectForm(StyledFormMixin, ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'section_owner', 'category', 'phase_completion']
        widgets = {
            'name': TextInput(),
        }


class ProjectScoreForm(StyledFormMixin, ModelForm):
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


class ProjectCategoryForm(StyledFormMixin, ModelForm):
    class Meta:
        model = ProjectCategory
        fields = [
            'category',
            'subcategory'
        ]


class SenateDistrictForm(StyledFormMixin, ModelForm):
    class Meta:
        model = SenateDistrict
        fields = ('name',)
        widgets = {
            'name': TextInput()
        }


class HouseDistrictForm(StyledFormMixin, ModelForm):
    class Meta:
        model = HouseDistrict
        fields = ('name',)
        widgets = {
            'name': TextInput()
        }


class CommissionerDistrictForm(StyledFormMixin, ModelForm):
    class Meta:
        model = CommissionerDistrict
        fields = ('name',)
        widgets = {
            'name': TextInput()
        }


class ZoneForm(StyledFormMixin, ModelForm):
    class Meta:
        model = Zone
        fields = ('name',)
        widgets = {
            'name': TextInput()
        }


SenateDistrictFormset = inlineformset_factory(Project, SenateDistrict, form=SenateDistrictForm)


HouseDistrictFormset = inlineformset_factory(Project, HouseDistrict, form=HouseDistrictForm)


CommissionerDistrictFormset = inlineformset_factory(Project, CommissionerDistrict, form=CommissionerDistrictForm)


ZoneFormset = inlineformset_factory(Project, Zone, form=ZoneForm)
