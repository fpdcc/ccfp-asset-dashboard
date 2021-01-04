from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from djmoney.models.fields import MoneyField
from django.contrib.gis.db import models


class Section(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section,
                                null=True,
                                on_delete=models.SET_NULL)


class Plan(models.Model):

    name = models.TextField()
    user = models.ForeignKey(Staff,
                             on_delete=models.CASCADE,
                             related_name='plans')

    def total_budget(self):
        ...

    def other_aggregate_measures(self):
        ...


class Project(models.Model):

    name = models.TextField()
    description = models.TextField()
    category = models.ForeignKey('ProjectCategory',
                                 null=True,
                                 on_delete=models.SET_NULL)
    section_owner = models.ForeignKey(Section,
                                      null=True,
                                      on_delete=models.SET_NULL)
    plan = models.ManyToManyField(Plan)

    obligation = models.BooleanField(default=False)
    phase_completion = models.BooleanField(default=False)
    accessibility = models.BooleanField(default=False)
    leverage_resource = models.BooleanField(default=False)

    # Geographic Districts
    @property
    def zones(self):
        'Which CCFP Zones intersect with the assets associated with this project'
        # we'll start by doing a geo-intersect query, but we might want to
        # end up caching that in table that gets updated when the assets
        # that gets associated with a project gets updated
        ...

    @property
    def senate_districts(self):
        ...

    @property
    def house_districts(self):
        ...

    @property
    def commissioner_districts(self):
        ...

    def __str__(self):
        return self.name


class ProjectScore(models.Model):

    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    core_mission_score = models.IntegerField(default=1,
                                             validators=[MinValueValidator(1),
                                                         MaxValueValidator(5)])
    operations_impact_score = models.IntegerField(default=1,
                                                  validators=[MinValueValidator(1),
                                                              MaxValueValidator(5)])
    sustainability_score = models.IntegerField(default=1,
                                               validators=[MinValueValidator(1),
                                                           MaxValueValidator(5)])
    ease_score = models.IntegerField(default=1,
                                     validators=[MinValueValidator(1),
                                                 MaxValueValidator(5)])
    geographic_distance_score = models.IntegerField(default=1,
                                                    validators=[MinValueValidator(1),
                                                                MaxValueValidator(5)])
    social_equity_score = models.IntegerField(default=1,
                                              validators=[MinValueValidator(1),
                                                          MaxValueValidator(5)])

    @property
    def total_score(self):
        '''return the total, weighted score'''
        ...

    def add_score_to_queryset(self):
        '''we'll need to add the total scores to the queryset'''
        ...


class ProjectFinances(models.Model):

    FUNDING_CHOICES = [
        ('unfunded', 'Unfunded'),
        ('partially funded', 'Partially Funded'),
        ('future unfunded', 'Future Unfunded'),
        ('funded', 'Funded')
    ]

    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    year = models.IntegerField()
    bid_quarter = models.TextField()
    funded = models.TextField(choices=FUNDING_CHOICES,
                              null=True,
                              blank=True)
    high_priority = models.BooleanField(default=False)
    rollover = MoneyField(default_currency='USD',
                          default=0.00,
                          max_digits=11)
    bond = MoneyField(default_currency='USD',
                      default=0.00,
                      max_digits=11)
    grant_funds = MoneyField(default_currency='USD',
                             default=0.00,
                             max_digits=11)
    fees = MoneyField(default_currency='USD',
                      default=0.00,
                      max_digits=11)
    budget = MoneyField(default_currency='USD',
                        default=0.00,
                        max_digits=11)


class ProjectFundingYear(models.Model):

    project = models.ForeignKey(Project,
                                null=True,
                                on_delete=models.CASCADE)
    year = models.IntegerField()
    funds = MoneyField(default_currency='USD',
                       default=0.00,
                       max_digits=11)


class Asset(models.Model):

    name = models.TextField()
    location = models.GeometryField()
    project = models.ManyToManyField(Project,
                                     related_name='assets')


class ProjectCategory(models.Model):

    category = models.TextField(null=False)
    subcategory = models.TextField(null=True)

    def __str__(self):
        return self.category


class HouseDistrict(models.Model):
    name = models.TextField()
    shape = models.PolygonField()


class SenateDistrict(models.Model):
    name = models.TextField()
    shape = models.PolygonField()


class CommissionerDistrict(models.Model):

    name = models.TextField()
    shape = models.PolygonField()


class Zone(models.Model):
    name = models.TextField(null=False)
    shape = models.PolygonField()


class ScoreWeights(models.Model):

    core_mission_score = models.FloatField(default=1.0,
                                           validators=[MinValueValidator(0.0),
                                                       MaxValueValidator(1.0)])
    operations_impact_score = models.FloatField(default=1.0,
                                                validators=[MinValueValidator(0.0),
                                                            MaxValueValidator(1.0)])
    sustainability_score = models.FloatField(default=1.0,
                                             validators=[MinValueValidator(0.0),
                                                         MaxValueValidator(1.0)])
    ease_score = models.FloatField(default=1.0,
                                   validators=[MinValueValidator(0.0),
                                               MaxValueValidator(1.0)])
    geographic_distance_score = models.FloatField(default=1.0,
                                                  validators=[MinValueValidator(0.0),
                                                              MaxValueValidator(1.0)])
    social_equity_score = models.FloatField(default=1.0,
                                            validators=[MinValueValidator(0.0),
                                                        MaxValueValidator(1.0)])

    # I'm not sure it makes sense to score these binary variables, but
    # there's ambiguity on what the client wants
    obligation_weight = models.FloatField()
    phase_completion = models.FloatField()
    accessibility = models.FloatField()
    leverage_resource = models.FloatField()


class DummyProject(models.Model):
    """A Project model, based on the columns from ~/raw/simplified.csv"""
    name = models.CharField(max_length=100)
    project_description = models.CharField(max_length=1000)
    budget = models.IntegerField()
    zone = models.CharField(max_length=30)

    def __str__(self):
        """"String for representing the model object"""
        return self.name
