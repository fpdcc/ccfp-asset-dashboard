from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from djmoney.models.fields import MoneyField

# https://stackoverflow.com/a/20116327/98080

class HouseDistrict(models.Model):
    
    name = models.CharField()
    shape = model.shape
    
class SenateDistrict(models.Model):
    
    name = models.CharField()
    shape = models.shape
    
class CommissionerDistrict():
    
    name = models.CharField()
    shape = models.shape
    
class ProjectCategory(models.Model):
    
    category = models.CharField(null=False)
    subcategory = models.CharField(null=True)

class Zone(models.Model):    
    name = models.CharField(null=False)
    shape = models.shape
    
class Section(models.Model):
    
    name = models.CharField()

class Project(models.Model):
    FUNDING_CHOICES = [
        ('unfunded', 'Unfunded'),
        ('partially funded', 'Partially Funded'),
        ('future unfunded', 'Future Unfunded'),
        ('funded', 'Funded')
    ]
    section_owner = models.ForeignKey(Section,
                                      on_delete=models.SET_NULL)

    # don't love setting these by hand instead of computing 
    # them, but CCFP wants to do this by hand for now.
    #
    # if projects are long-lived then this is going to run
    # into a problem when the disctricts change
    #
    # alternative might be to get them to put in a lat long
    # I'll ask Garrert about that.
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
    
    name = models.CharField()
    bid_quarter = models.CharField()
    description = models.TextField()
    category = models.ForeignKey(ProjectCategory,
                                 null=True,
                                 on_delete=models.SET_NULL)
    funded = models.CharField(choices=FUNDING_CHOICES,
                              null=True,
                              blank=True)
    high_priority = models.BooleanField(default=False)
    rollover = MoneyField(default_currency='USD',
                          default=0.00)
    bond = MoneyField(default_currency='USD',
                      default=0.00)
    grant_funds = MoneyField(default_currency='USD',
                             default=0.00)
    fees = MoneyField(default_currency='USD',
                      default=0.00)
    year = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    
    budget = MoneyField(default_currency='USD',
                        default=0.00)
    
        
class ProjectFundingYear(models.Model):
    
    project = models.ForeignKey(Project,
                                null=True,
                                on_delete=models.CASCADE,
                                default=0.00)
    year = models.IntegerField()
    funds = MoneyField(default_current='USD')
    plan = models.ManyToManyField(Plan,
                                  related_names='projects')
    
    
class Asset(models.Model):
    
    name = models.CharField()
    location = models.latlong
    project = models.ManyToManyField(Project,
                                     related_name='assets')

    
class CapitalPlan(models.Model):
    
    name = models.CharField()
    user = models.ForeignKey(USER,
                             related_name='plans')
    
    
    

# Create your models here.
