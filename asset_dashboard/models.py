from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from djmoney.models.fields import MoneyField
from django.contrib.gis.db import models


class Section(models.Model):
    name = models.TextField()


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section,
                                null=True,
                                on_delete=models.SET_NULL)


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


class ProjectCategory(models.Model):

    category = models.TextField(null=False)
    subcategory = models.TextField(null=True)


class Project(models.Model):
    FUNDING_CHOICES = [
        ('unfunded', 'Unfunded'),
        ('partially funded', 'Partially Funded'),
        ('future unfunded', 'Future Unfunded'),
        ('funded', 'Funded')
    ]

    name = models.TextField()
    description = models.TextField()
    category = models.ForeignKey(ProjectCategory,
                                 null=True,
                                 on_delete=models.SET_NULL)
    section_owner = models.ForeignKey(Section,
                                      null=True,
                                      on_delete=models.SET_NULL)

    # don't love setting these by hand instead of computing
    # them, but CCFP wants to do this by hand for now.
    #
    # if projects are long-lived then this is going to run
    # into a problem when the disctricts change
    #
    # alternative might be to get them to put in a lat long
    # I'll ask Garret about that.
    zone = models.ForeignKey(Zone,
                             null=True,
                             on_delete=models.SET_NULL)
    senate_district = models.ForeignKey(SenateDistrict,
                                        null=True,
                                        on_delete=models.SET_NULL)
    house_district = models.ForeignKey(HouseDistrict,
                                       null=True,
                                       on_delete=models.SET_NULL)
    commissioner_district = models.ForeignKey(CommissionerDistrict,
                                              null=True,
                                              on_delete=models.SET_NULL)
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
    obligation = models.BooleanField(default=False)
    phase_completion = models.BooleanField(default=False)
    accessibility = models.BooleanField(default=False)
    leverage_resource = models.BooleanField(default=False)

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
    year = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    budget = MoneyField(default_currency='USD',
                        default=0.00,
                        max_digits=11)

    def score(self):
        '''return the total, weighted score'''
        ...

    def add_score_to_queryset(self):
        '''we'll need to add the total scores to the queryset'''
        ...


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
    location = models.PointField()
    project = models.ManyToManyField(Project,
                                     related_name='assets')


class CapitalPlan(models.Model):

    name = models.TextField()
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='plans')

    def total_budget(self):
        ...

    def other_aggregate_measures(self):
        ...


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
