from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput

from .models import Project, PhaseFinances, ProjectScore, ProjectCategory, Phase, PhaseFundingYear


class StyledFormMixin(object):
    """
    Generic mixin to consistently style each form field's html <input> element.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProjectForm(StyledFormMixin, ModelForm):
    class Meta:
        model = Project
        fields = ['name',
                  'description',
                  'section_owner',
                  'category',
                  'senate_districts',
                  'house_districts',
                  'commissioner_districts',
                  'zones']
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


class PhaseFinancesForm(StyledFormMixin, ModelForm):
    class Meta:
        model = PhaseFinances
        fields = [
            'budget'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PhaseForm(StyledFormMixin, ModelForm):
    class Meta:
        model = Phase
        fields = [
            'phase_type',
            'estimated_bid_quarter',
            'status'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PhaseFundingYearForm(StyledFormMixin, ModelForm):
    class Meta:
        model = PhaseFundingYear
        fields = [
            'year',
            'funds'
        ]

    # TODO: reconcile with phase-form branch
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # When saving a Phase, this PhaseFundingYearForm
        # is included but isn't required
        self.fields['year'].required = False
        self.fields['funds'].required = False


class LocalAssetForm:
    """
    We don't need all the HTML elements from a standard Django
    form class, so we're implementing a basic class to validate
    the GeoJSON.
    """
    def __init__(self, geojson, *args, **kwargs):
        self.uncleaned_geojson = geojson

    def is_valid(self, *args, **kwargs):
        request_data = self.uncleaned_geojson

        if self.is_valid_feature_collection(request_data):
            return True

    def is_valid_feature_collection(self, data):
        """
        The geojson library doesn't have a validation for
        feature collection, so we implement our own.
        """
        try:
            geojson = data.get('geojson')

            if not geojson:
                raise ValidationError('The GeoJSON is missing a "geom" key.')

            features = geojson.get('features')

            if not features:
                raise ValidationError('The GeoJSON is missing a "features" key')

            for feature in features:
                geometry = feature.get('geometry')

                if not geometry:
                    raise ValidationError('Feature is missing a "geometry" key.')

                if not geometry.get('coordinates'):
                    raise ValidationError('Geometry is missing a "coordinates" key.')

            self.cleaned_geojson = geojson
            return True
        except AttributeError as e:
            """Catch this error when a part of the dict is a string."""
            raise ValidationError(e)
