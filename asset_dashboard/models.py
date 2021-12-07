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

    class Meta:
        verbose_name_plural = 'Staff'


class Project(models.Model):

    name = models.TextField()
    description = models.TextField()
    category = models.ForeignKey('ProjectCategory',
                                 null=True,
                                 on_delete=models.SET_NULL)
    section_owner = models.ForeignKey(Section,
                                      null=True,
                                      on_delete=models.SET_NULL)

    house_districts = models.ManyToManyField('HouseDistrict', blank=True)
    senate_districts = models.ManyToManyField('SenateDistrict', blank=True)
    commissioner_districts = models.ManyToManyField('CommissionerDistrict', blank=True)
    zones = models.ManyToManyField('Zone', blank=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    """
    A sub-project unit of work. Projects without defined tasks are assigned a
    default Task of type "implementation".
    """

    # TODO: Identify better choice list (e.g., what's the difference between
    # Phase 3 Construction and Construction?)
    TASK_TYPE_CHOICES = [
        ('phase_1', 'Phase 1'),
        ('phase_2', 'Phase 2'),
        ('phase_3_engineering', 'Phase 3 Engineering'),
        ('phase_3_construction', 'Phase 3 Construction'),
        ('feasibility', 'Feasibility'),
        ('design', 'Design'),
        ('construction', 'Construction'),
        ('implementation', 'Implementation'),
    ]

    BID_QUARTER_CHOICES = [
        ('Q1', 'Q1'),
        ('Q2', 'Q2'),
        ('Q3', 'Q3'),
        ('Q4', 'Q4')
    ]

    sequence = models.IntegerField(default=1)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='tasks')
    task_type = models.TextField(choices=TASK_TYPE_CHOICES, null=True, blank=True)
    estimated_bid_quarter = models.TextField(choices=BID_QUARTER_CHOICES, null=True, blank=True)
    # funding = models.ForeignKey('FundingSource', on_delete=models.SET_NULL)


class ScoreField(models.IntegerField):
    def __init__(self, *args, **kwargs):

        if 'null' not in kwargs:
            kwargs['null'] = True
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'validators' not in kwargs:
            kwargs['validators'] = [MinValueValidator(1), MaxValueValidator(5)]

        super().__init__(*args, **kwargs)


class ProjectScore(models.Model):

    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    core_mission_score = ScoreField()
    operations_impact_score = ScoreField()
    sustainability_score = ScoreField()
    ease_score = ScoreField()
    geographic_distance_score = ScoreField()
    social_equity_score = ScoreField()

    @property
    def total_score(self):
        score_fields = [f for f in self._meta.get_fields() if type(f) == ScoreField]

        # there should be one, and only one row in score weights.
        # this tuple unpacking will throw an error if that's not so
        score_weights, = ScoreWeights.objects.all()
        total_score = 0

        for field in score_fields:
            score_field_value = field.value_from_object(self)
            weight_field_value = field.value_from_object(score_weights)

            # return a total of 0 if any of the fields are missing a score
            if score_field_value is None:
                total_score = 0
                return total_score

            total_score += score_field_value * weight_field_value

        return total_score

    def add_score_to_queryset(self):
        """we'll need to add the total scores to the queryset"""

    def __str__(self):
        return self.project.name

    class Meta:
        verbose_name_plural = 'Project Scores'


class TaskFinances(models.Model):

    FUNDING_CHOICES = [
        ('unfunded', 'Unfunded'),
        ('partially funded', 'Partially Funded'),
        ('future unfunded', 'Future Unfunded'),
        ('funded', 'Funded')
    ]

    task = models.OneToOneField('Task', on_delete=models.CASCADE)
    budget = MoneyField(default_currency='USD',
                        default=0.00,
                        max_digits=11)

    class Meta:
        verbose_name_plural = 'Project Finances'


class TaskFundingYear(models.Model):

    task = models.ForeignKey('Task',
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
    name = models.TextField(null=False, default='project category')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            if self.subcategory:
                self.name = f'{self.category} > {self.subcategory}'
            else:
                self.name = self.category

        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Project Categories'


class HouseDistrict(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'House Districts'


class SenateDistrict(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Senate Districts'


class CommissionerDistrict(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Commissioner Districts'


class Zone(models.Model):
    name = models.TextField(null=False)

    def __str__(self):
        return self.name


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

    class Meta:
        verbose_name_plural = 'Score Weights'


class DummyProject(models.Model):
    """A Project model, based on the columns from ~/raw/simplified.csv"""
    name = models.CharField(max_length=100)
    project_description = models.CharField(max_length=1000)
    budget = models.IntegerField()
    zone = models.CharField(max_length=30)

    def __str__(self):
        """"String for representing the model object"""
        return self.name


class GISModel(models.Model):
    """
    Migrations will not be created for models inheriting from this base class
    because of allow_migrate() method in the GISRouter.
    """

    class Meta:
        abstract = True
        managed = False
        app_label = 'asset_dashboard_gis'


class NaturePreserves(GISModel):

    class Meta(GISModel.Meta):
        db_table = '"quercus"."nature_preserves"'

    id = models.AutoField(primary_key=True, db_column='nature_preserves_id')
    site_name = models.CharField(max_length=254)

    def __str__(self):
        return self.site_name


class Buildings(GISModel):

    class Meta(GISModel.Meta):
        db_table = 'quercus.buildings'


class Holdings(GISModel):

    class Meta(GISModel.Meta):
        db_table = 'quercus.holdings'


class LicenseIGA(GISModel):

    class Meta(GISModel.Meta):
        db_table = 'quercus.license_iga'


class MowAreaDB(GISModel):

    class Meta(GISModel.Meta):
        db_table = 'quercus.mow_area_db'


class MwrdFpdLease(GISModel):

    class Meta(GISModel.Meta):
        db_table = 'quercus.mwrd_fpd_lease'


class Names(GISModel):

    class Meta(GISModel.Meta):
        db_table = 'quercus.names'


class ParkingEntrance(GISModel):

    class Meta(GISModel.Meta):
        db_table = 'quercus.parking_entrance'


class ParkingEntranceInfo(GISModel):

    class Meta(GISModel.Meta):
        db_table = 'quercus.parking_entrance_info'


class ParkingEval17(GISModel):

    class Meta(GISModel.Meta):
        db_table = 'quercus.parking_eval17'


class ParkingLots(GISModel):

    class Meta(GISModel.Meta):
        db_table = 'quercus.parking_lots'


class PicnicGroves(GISModel):

    class Meta(GISModel.Meta):
        db_table = 'quercus.picnicgroves'


class PoiAmenity(GISModel):

    class Meta(GISModel.Meta):
        db_table = 'quercus.poi_amenity'


class PoiDesc(GISModel):

    class Meta(GISModel.Meta):
        db_table = 'quercus.poi_desc'


class PoiInfo(GISModel):

    class Meta(GISModel.Meta):
        db_table = 'quercus.poi_info'


class PoiToTrails(GISModel):

    class Meta(GISModel.Meta):
        db_table = 'quercus.poi_to_trails'


class PointsOfInterest(GISModel):

    class Meta(GISModel.Meta):
        db_table = 'quercus.pointsofinterest'


class Regions(GISModel):

    class Meta(GISModel.Meta):
        db_table = 'quercus.regions'


class Signage(GISModel):

    class Meta(GISModel.Meta):
        db_table = 'quercus.signage'


class TrailSubsystemLu(GISModel):

    class Meta(GISModel.Meta):
        db_table = 'quercus.trail_subsystem_lu'


class Trails(GISModel):

    class Meta(GISModel.Meta):
        db_table = 'quercus.trails'


class TrailsAmenity(GISModel):

    class Meta(GISModel.Meta):
        db_table = 'quercus.trails_amenity'


class TrailsDesc(GISModel):

    class Meta(GISModel.Meta):
        db_table = 'quercus.trails_desc'


class TrailsInfo(GISModel):

    class Meta(GISModel.Meta):
        db_table = 'quercus.trails_info'


class TrailsMaintenance(GISModel):

    class Meta(GISModel.Meta):
        db_table = 'quercus.trails_maintenace'


class Zones(GISModel):
    class Meta(GISModel.Meta):
        db_table = 'quercus.zones'

    # fpdcc=# \d quercus.zones
    #                                             Table "quercus.zones"
    #     Column    |            Type             | Collation | Nullable |                    Default
    # --------------+-----------------------------+-----------+----------+------------------------------------------------
    # zone_id      | integer                     |           | not null | nextval('quercus.zones_zone_id_seq'::regclass)
    # zone         | character varying(10)       |           |          |
    # abbreviation | character varying(2)        |           |          |
    # geom         | geometry(MultiPolygon,3435) |           |          |
    # Indexes:
    #     "zones_pkey" PRIMARY KEY, btree (zone_id)

    # zones_pk = models.IntegerField(primary_key=True)
    zone_id = models.IntegerField(primary_key=True)
    zone = models.CharField(max_length=10)
    geom = models.MultiPolygonField(srid=3435)  # TODO: i think this was srid? `geom | geometry(MultiPolygon,3435)`
