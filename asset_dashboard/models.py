from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.gis.db import models
from django.db.models import Max, Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

from djmoney.models.fields import MoneyField


class SequencedModel(models.Model):

    class Meta:
        abstract = True

    sequence = models.IntegerField()

    @property
    def sequenced_instances(self):
        '''
        Queryset of instances belonging to the same sequence.
        '''
        raise NotImplementedError(
            'Property "sequenced_instances" must be defined on subclass'
        )

    @property
    def relative_position(self):
        '''
        The zero-index position of a given sequenced instance, in a list of all
        sequenced instances. Order incoming instances without a specified
        sequence last.
        '''
        if self.sequence is not None:
            return self.sequence - 1
        else:
            return self.sequenced_instances.aggregate(Max('sequence'))['sequence__max']

    def save(self, *args, **kwargs):
        '''
        Given a new sequenced instance, update sequence across all instances to
        account for arbitrary sequencing of new instance.

        For example, if we have two (instance, sequence) pairs (A, 1) and (B, 2),
        and we insert a new pair (C, 2), insert C with a sequence of 2 and update
        B to have a sequence of 3.
        '''
        if self.sequenced_instances.exists():
            instances = list(self.sequenced_instances.order_by('sequence'))
            instances.insert(self.relative_position, self)

            for_update = []

            for seq, instance in enumerate(instances, start=1):
                if instance.sequence != seq:
                    instance.sequence = seq
                    for_update.append(instance)

            # Save the new instance
            super().save(*args, **kwargs)

            # Update the sequence of all changed instances. N.b., bulk_update()
            # does not call the save() method of updated instances.
            type(self).objects.bulk_update(for_update, ['sequence'])

        else:
            # If there are no other sequenced instances, default to 1
            self.sequence = 1
            super().save(*args, **kwargs)


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


class Portfolio(models.Model):

    name = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PortfolioPhase(SequencedModel):

    portfolio = models.ForeignKey('Portfolio', related_name='phases', on_delete=models.CASCADE)
    phase = models.ForeignKey('Phase', related_name='portfolios', on_delete=models.CASCADE)

    @property
    def sequenced_instances(self):
        return self.portfolio.phases


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
        return self.name or ''

    @receiver(post_save, sender='asset_dashboard.LocalAsset')
    def calculate_zones_and_districts(sender, instance, **kwargs):
        zones = Zone.objects.filter(boundary__contains=instance.geom)

        for zone in zones:
            instance.phase.project.zones.add(zone)
            instance.phase.project.save()

        district_models = [
            ('commissioner_districts', CommissionerDistrict),
            ('senate_districts', SenateDistrict),
            ('house_districts', HouseDistrict)
        ]

        for attribute, model in district_models:
            districts = model.objects.filter(
                boundary__contains=instance.geom
            )

            for district in districts:
                project_district = getattr(instance.phase.project, attribute)
                project_district.add(district)
                instance.phase.project.save()

        house_districts = HouseDistrict.objects.filter(
            boundary__contains=instance.geom
        )

        print('house districts', house_districts)

class Phase(SequencedModel):
    """
    A sub-project unit of work. Projects without defined phases are assigned a
    default Phase of type "implementation".
    """

    PHASE_TYPE_CHOICES = [
        ('feasibility', 'Feasibility'),
        ('design', 'Design'),
        ('engineering', 'Engineering'),
        ('construction', 'Construction'),
        ('implementation', 'Implementation'),
    ]

    BID_QUARTER_CHOICES = [
        ('Q1', 'Q1'),
        ('Q2', 'Q2'),
        ('Q3', 'Q3'),
        ('Q4', 'Q4')
    ]

    STATUS_CHOICES = [
        ('unscheduled', 'Unscheduled'),
        ('in-progress', 'In Progress'),
        ('done', 'Done'),
    ]

    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='phases')
    phase_type = models.TextField(choices=PHASE_TYPE_CHOICES, null=True, blank=True)
    estimated_bid_quarter = models.TextField(choices=BID_QUARTER_CHOICES, null=True, blank=True)
    status = models.TextField(choices=STATUS_CHOICES, default='unscheduled')

    funding_streams = models.ManyToManyField('FundingStream')

    year = models.IntegerField(null=True, blank=True)

    total_estimated_cost = MoneyField(default_currency='USD',
                                      default=0.00,
                                      max_digits=11)

    @property
    def total_budget(self):
        total = self.funding_streams.all().values(
            'budget'
        ).aggregate(Sum('budget'))['budget__sum']

        return total if total else 0

    @property
    def sequenced_instances(self):
        return self.project.phases

    @property
    def name(self):
        return str(self)

    def __str__(self):
        return f'{self.phase_type} - {self.estimated_bid_quarter} - {self.status}'


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


class FundingStream(models.Model):
    SOURCE_TYPE_CHOICES = [
        ('capital_improvement_fund', 'Capital Improvement Fund'),
        ('bonds', 'General Obligation Bonds'),
        ('construction_development', 'Construction & Development'),
        ('grants_fees_other', 'Grants, Fees, & Other'),
        ('rollover', 'Rollover')
    ]

    budget = MoneyField(default_currency='USD',
                        default=0.00,
                        max_digits=11)
    obligated_year = models.IntegerField(null=True, blank=True)
    obligated_completion_date = models.IntegerField(null=True, blank=True)
    funding_secured = models.BooleanField(default=False)
    source_type = models.TextField(choices=SOURCE_TYPE_CHOICES, default='capital_improvement_fund')

    class Meta:
        verbose_name_plural = 'Phase Funding Stream'


class LocalAsset(models.Model):
    """
    We save a local copy of a geo asset with this model.
    """

    phase = models.ForeignKey('Phase', on_delete=models.CASCADE)

    geom = models.GeometryField(srid=3435)

    asset_id = models.TextField(null=True, blank=True)
    asset_model = models.CharField(max_length=100)
    asset_name = models.CharField(max_length=600)


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
    boundary = models.GeometryField(srid=3435, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'House Districts'


class SenateDistrict(models.Model):
    name = models.TextField()
    boundary = models.GeometryField(srid=3435, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Senate Districts'


class CommissionerDistrict(models.Model):
    name = models.TextField()
    boundary = models.GeometryField(srid=3435, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Commissioner Districts'

class Zone(models.Model):
    name = models.TextField(null=False)
    boundary = models.MultiPolygonField(srid=3435, null=True)

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

# TODO: can we remove this?
class DummyProject(models.Model):
    """A Project model, based on the columns from ~/raw/simplified.csv. This is for testing."""
    name = models.CharField(max_length=100)
    project_description = models.CharField(max_length=1000)
    budget = models.IntegerField()
    zone = models.CharField(max_length=30)

    def __str__(self):
        """"String for representing the model object"""
        return self.name

## UNMANAGED MODELS
# These models are for using their GIS database.
# They are unmanaged and have only read privileges,
# so there is no ability to write to these tables.

class GISModel(models.Model):
    """
    Migrations will not be created for models inheriting from this base class
    because of allow_migrate() method in the GISRouter.
    """

    class Meta:
        abstract = True
        managed = False
        app_label = 'asset_dashboard_gis'


class Buildings(GISModel):
    """Includes all building structures within FPDCC boundaries"""

    class Meta(GISModel.Meta):
        db_table = '"quercus"."buildings"'

    class Search:
        fields = (
            ('fpd_uid', int),
            ('building_name', str),
        )

    id = models.AutoField(primary_key=True, db_column='buildings_id')
    geom = models.PolygonField(srid=3435)
    building_number = models.CharField(max_length=10)
    building_comments = models.CharField(max_length=75)
    grove_number = models.CharField(max_length=5)
    forest = models.CharField(max_length=40)
    commplace = models.CharField(max_length=20)
    fpd_uid = models.IntegerField(null=True)
    division_name = models.CharField(max_length=15)
    region = models.IntegerField()
    building_name = models.CharField(max_length=100)
    complex = models.CharField(max_length=100)
    building_type = models.CharField(max_length=50)
    sqft = models.FloatField()
    alternate_address = models.CharField(max_length=50)
    concession = models.CharField(max_length=10)
    public_access = models.CharField(max_length=5)
    support_building = models.CharField(max_length=5)
    demolished = models.CharField(max_length=5)
    a1_list_12 = models.CharField(max_length=5)
    ada_evaluation = models.CharField(max_length=3)
    current_occupant = models.CharField(max_length=25)
    building_description = models.CharField(max_length=100)
    commissioner_district = models.IntegerField()
    wastewater = models.CharField(max_length=20)
    water = models.CharField(max_length=35)
    ownership = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    managing_department = models.CharField(max_length=25)
    improvement_year = models.CharField(max_length=25)
    addition = models.CharField(max_length=1)
    fpd_zone = models.CharField(max_length=10)
    old_address = models.CharField(max_length=150)
    street_name_current = models.CharField(max_length=50)
    address_number_current = models.CharField(max_length=10)
    city_current = models.CharField(max_length=30)
    zip_city_current = models.CharField(max_length=30)
    zip_current = models.CharField(max_length=5)
    address_current = models.CharField(max_length=150)
    seasonal_closing = models.CharField(max_length=25)


class Holdings(GISModel):
    """Includes all individual parcels owned by the FPDCC."""

    class Meta(GISModel.Meta):
        db_table = '"quercus"."holdings"'

    id = models.AutoField(primary_key=True, db_column='holdings_id')

    geom = models.MultiPolygonField(srid=3435)
    pin14 = models.CharField(max_length=14)
    pin10 = models.CharField(max_length=10)
    taxpayer_name = models.CharField(max_length=50)
    exemption_type = models.BigIntegerField()
    street_direction = models.CharField(max_length=2)
    street_name = models.CharField(max_length=30)
    street_suffix = models.CharField(max_length=4)
    city_name = models.CharField(max_length=30)
    control_number = models.IntegerField()
    subcontrol_number = models.CharField(max_length=2)
    grantor = models.CharField(max_length=35)
    dashed_pin10 = models.CharField(max_length=50)
    check_letter_number = models.CharField(max_length=4)
    date_of_check_letter = models.DateField()
    closing_letter_number = models.CharField(max_length=4)
    date_of_closing_letter = models.DateField()
    date_of_condemnation_petition = models.DateField()
    proceedings_book_year = models.CharField(max_length=4)
    proceedings_book_page = models.CharField(max_length=4)
    deed_book_number = models.CharField(max_length=4)
    deed_book_page = models.CharField(max_length=7)
    legal_file_number = models.CharField(max_length=7)
    survey_number = models.CharField(max_length=20)
    plat_number = models.CharField(max_length=20)
    tract_name = models.CharField(max_length=20)
    remarks_a_index_remarks = models.CharField(max_length=10)
    chicago_real_estate_board_number = models.CharField(max_length=10)
    appraisal_per_acre_cost = models.CharField(max_length=10)
    improvement_appraisal = models.CharField(max_length=10)
    other_appraisal = models.CharField(max_length=20)
    chicago_real_estate_board_file_number = models.CharField(max_length=10)
    remarks_b_appraisal_remarks = models.CharField(max_length=10)
    total_acreage_acquired = models.DecimalField(max_digits=10, decimal_places=3)
    total_cost = models.FloatField()
    per_acre_cost = models.FloatField()
    acquired_by_negotiation = models.IntegerField()
    acquired_by_condemnation = models.IntegerField()
    condemnation_order = models.CharField(max_length=10)
    date_of_judgment_order = models.DateField()
    participation_percent = models.CharField(max_length=5)
    remarks_c_acquisition_remarks = models.CharField(max_length=10)
    title_guarantee_policy_number = models.CharField(max_length=7)
    torrens_certificate_number = models.CharField(max_length=7)
    type_of_document = models.CharField(max_length=7)
    date_of_document = models.DateField()
    document_number = models.CharField(max_length=8)
    book_number = models.CharField(max_length=6)
    page_number = models.CharField(max_length=4)
    date_recorded = models.DateField()
    remarks_d_document_remarks = models.CharField(max_length=10)
    volume_number = models.CharField(max_length=4)
    item_number = models.CharField(max_length=8)
    year_tax_claimed = models.CharField(max_length=4)
    tax_amount_claimed = models.CharField(max_length=7)
    date_injunction_was_filed = models.CharField(max_length=12)
    date_of_injunction_action = models.DateField()
    date_exempted = models.CharField(max_length=12)
    remarks_e_tax_remarks = models.CharField(max_length=10)
    status = models.CharField(max_length=50)
    dissolve = models.IntegerField()
    parcel_name = models.CharField(max_length=50)
    updated = models.DateField()
    fpd_ac = models.DecimalField(max_digits=10, decimal_places=3)
    fpd_zone = models.CharField(max_length=10)
    iga = models.CharField(max_length=250)
    iga_licensee = models.CharField(max_length=75)
    iga_exhibit = models.CharField(max_length=250)
    boundary_survey_corrected = models.CharField(max_length=3)

    # This model is missing a PostGIS `topogeom`, because
    #  the Django geo library doesn't have this data type
    #  and we don't yet need it.


class LicenseIGA(GISModel):
    """All licenses an IGA's registered with the FPDCC."""

    class Meta(GISModel.Meta):
        db_table = '"quercus"."license_iga"'

    id = models.AutoField(primary_key=True, db_column='license_iga_id')
    geom = models.GeometryField(srid=3435, spatial_index=True)

    license_no = models.CharField(max_length=32)
    lic_type = models.CharField(max_length=50)
    entity = models.CharField(max_length=100)
    diameter = models.CharField(max_length=50)
    material = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    end_date = models.DateField()
    status = models.CharField(max_length=50)
    agreement_type = models.CharField(max_length=50)
    plss_township = models.IntegerField()
    plss_range = models.IntegerField()
    plss_section = models.IntegerField()
    structure = models.CharField(max_length=10)


class MowAreaDB(GISModel):
    """All mowed areas by Landscape Maintenance and Resource Mgmt."""

    class Meta(GISModel.Meta):
        db_table = '"quercus"."mow_area_db"'

    id = models.AutoField(primary_key=True, db_column='id')

    geom = models.MultiPolygonField(srid=3435)

    filename = models.CharField(max_length=80)
    name = models.CharField(max_length=141)
    descriptio = models.CharField(max_length=187)
    region = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    area = models.FloatField()
    mow_freq = models.CharField(max_length=50)
    mow_date = models.DateField()


class MwrdFpdLease(GISModel):
    """Land Leased to the FPDCC by MWRD."""

    class Meta(GISModel.Meta):
        db_table = '"quercus"."mwrd_fpd_lease"'

    id = models.AutoField(primary_key=True, db_column='id')

    geom = models.PolygonField(srid=3435, spatial_index=True)

    lease_id = models.CharField(max_length=50)
    acreage = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.CharField(max_length=254)
    lease_end = models.DateField()
    lease_start = models.DateField()


class Names(GISModel):
    """Table of all FPDCC preserve/location names."""

    class Meta(GISModel.Meta):
        db_table = '"quercus"."names"'

        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_nameid_constraint')
        ]

    id = models.AutoField(primary_key=True, db_column='nameid')

    name = models.CharField(max_length=100)


class NaturePreserves(GISModel):
    """Official Nature Preserve boundaries within FPDCC boundaries."""

    class Meta(GISModel.Meta):
        db_table = '"quercus"."nature_preserves"'

    id = models.AutoField(primary_key=True, db_column='nature_preserves_id')

    geom = models.MultiPolygonField(srid=3435, spatial_index=True)

    org = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    site_name = models.CharField(max_length=254)
    np_date = models.DateField()
    pins = models.CharField(max_length=254)
    document = models.CharField(max_length=254)
    np_number = models.IntegerField()
    lwr_number = models.IntegerField()
    comments = models.CharField(max_length=254)
    source = models.CharField(max_length=50)
    acreage = models.DecimalField(max_digits=10, decimal_places=2)
    gis_acres = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.site_name


class ParkingEntrance(GISModel):
    """Point location of all official parking lot entrances."""

    class Meta(GISModel.Meta):
        db_table = '"quercus"."parking_entrance"'

    id = models.AutoField(primary_key=True, db_column='parking_entrance_id')
    geom = models.PointField(srid=3435, spatial_index=True)


class ParkingEntranceInfo(GISModel):
    """Companion metadata to "parking_entrance". Foreign Key reference "parking_entrance_id"."""

    class Meta(GISModel.Meta):
        db_table = '"quercus"."parking_entrance_info"'

        indexes = [
            models.Index(fields=['parking_entrance_id'])
        ]

    id = models.AutoField(primary_key=True, db_column='parking_info_id')

    parking_entrance = models.ForeignKey('ParkingEntrance', on_delete=models.RESTRICT)

    multi_entrance = models.CharField(max_length=10)
    private_lot = models.CharField(max_length=10)
    lot_id = models.IntegerField()
    fpd_uid = models.CharField(max_length=10)
    parking_entrance_addr = models.CharField(max_length=250)
    trailaccess = models.CharField(max_length=10)
    entrance_closed = models.CharField(max_length=10)


class ParkingEval17(GISModel):
    """Parking lot evaluation done by Cook County circa 2017."""

    class Meta(GISModel.Meta):
        db_table = '"quercus"."parking_eval17"'

    id = models.AutoField(primary_key=True, db_column='parking_eval17_id')

    # In postgres, these are all "character varying" with no character limit.
    # I them all TextFields since max_length is required for CharField.
    latitude = models.TextField()
    longitude = models.TextField()
    date = models.TextField()
    division = models.TextField()
    location = models.TextField()
    grove_name = models.TextField()
    grove_number = models.TextField()
    permits_visitors = models.TextField()
    parking_lot_area_sf = models.TextField()
    drive_area_sf = models.TextField()
    paser_rating = models.TextField()
    ramp_to_shelter = models.TextField()
    ramp_length_feet = models.TextField()
    ramp_paser_rating = models.TextField()
    regular_stalls = models.TextField()
    disabled_stalls = models.TextField()
    ramp_cuts_needed = models.TextField()
    ada_signs = models.TextField()
    signs_needed = models.TextField()
    ada_compliant_stalls = models.TextField()
    striping_visible = models.TextField()
    disabled_stalls_striping_needed = models.TextField()
    curb_gutter_type = models.TextField()
    c_g_length_replaced = models.TextField()
    wheel_stops = models.TextField()
    missing_wheel_stops = models.TextField()
    wheel_stops_replaced = models.TextField()
    storm_sewer_system = models.TextField()
    outlet_into = models.TextField()
    pipe_visible = models.TextField()
    grates_appropriate = models.TextField()
    cb_inlet_cleaning_needed = models.TextField()
    cb_inlet_adjustments_needed = models.TextField()
    cb_inlet_reconstruction_needed = models.TextField()
    low_areas_collect_water = models.TextField()
    unpaved_area_regrading_needed_sf = models.TextField()
    attendance_2012 = models.TextField()
    attendance_2013 = models.TextField()
    permits_booked_2016 = models.TextField()
    attendance_2016 = models.TextField()
    remarks = models.TextField()
    photos = models.TextField()


class ParkingLots(GISModel):
    """Parking lot polygons, for all public and non-public lots."""
    class Meta(GISModel.Meta):
        db_table = '"acer"."parking_lots_union_mv"'

    id = models.AutoField(primary_key=True, db_column='lot_id')
    geom = models.PolygonField(srid=3435, spatial_index=True)
    name = models.CharField(max_length=100)
    lot_access = models.CharField(max_length=25)
    maintained = models.CharField(max_length=10)
    closed = models.CharField(max_length=10)
    lot_surface = models.CharField(max_length=25)
    square_feet = models.DecimalField(max_digits=10, decimal_places=2)
    square_yards = models.DecimalField(max_digits=10, decimal_places=2)
    acres = models.DecimalField(max_digits=10, decimal_places=2)
    maintained_by = models.CharField(max_length=50)
    maintenance_comment = models.CharField(max_length=250)
    parking_info_id = models.IntegerField()


class PicnicGroves(GISModel):
    """All picnic groves with active status"""

    class Meta(GISModel.Meta):
        db_table = '"quercus"."picnicgroves"'

    class Search:
        fields = (
            ('fpd_uid', int),
            ('poi_info__nameid__name', str),
        )

    id = models.AutoField(primary_key=True, db_column='picnicgrove_id')

    poi_info = models.ForeignKey('PoiInfo', on_delete=models.SET_NULL)

    geom = models.PointField(srid=3435)

    preserve_name = models.CharField(max_length=100)
    grove = models.IntegerField()
    division = models.CharField(max_length=25)
    capacity = models.IntegerField()
    large_capacity = models.CharField(max_length=10)
    grove_type = models.CharField(max_length=10)
    location = models.CharField(max_length=50)
    status = models.CharField(max_length=10)
    fpd_uid = models.CharField(max_length=15)
    accessible = models.IntegerField()
    parking_to_shelter = models.IntegerField()
    shelter_to_bathroom = models.IntegerField()
    bathroom_type = models.CharField(max_length=15)


class PoiAmenity(GISModel):
    """Table of all amenities associated with a point of interest.
    Forgein Key reference poi_info.poi_info_id."""

    class Meta(GISModel.Meta):
        db_table = '"quercus"."poi_amenity"'
        indexes = [
            models.Index(fields=['poi_info_id'])
        ]

    id = models.AutoField(primary_key=True, db_column='poi_amenity_id')
    poi_info = models.ForeignKey('PoiInfo', on_delete=models.CASCADE)

    ada = models.IntegerField()
    bike_parking = models.IntegerField()
    bike_rental = models.IntegerField()
    birding = models.IntegerField()
    boat_ramp = models.IntegerField()
    boat_rental = models.IntegerField()
    camping = models.IntegerField()
    canoe = models.IntegerField()
    comfortstation = models.IntegerField()
    cross_country = models.IntegerField()
    cycling = models.IntegerField()
    disc_golf = models.IntegerField()
    dog_friendly = models.IntegerField()
    dog_leash = models.IntegerField()
    drinkingwater = models.IntegerField()
    drone = models.IntegerField()
    ecological = models.IntegerField()
    equestrian = models.IntegerField()
    fishing = models.IntegerField()
    ice_fishing = models.IntegerField()
    gas_powered = models.IntegerField()
    golf = models.IntegerField()
    hiking = models.IntegerField()
    indoor_rental = models.IntegerField()
    large_capacity = models.IntegerField()
    m_airplane = models.IntegerField()
    m_boat = models.IntegerField()
    nature_center = models.IntegerField()
    natureplay = models.IntegerField()
    no_alcohol = models.IntegerField()
    no_parking = models.IntegerField()
    overlook = models.IntegerField()
    public_building = models.IntegerField()
    picnic_grove = models.IntegerField()
    shelter = models.IntegerField()
    skating_ice = models.IntegerField()
    skating_inline = models.IntegerField()
    sledding = models.IntegerField()
    snowmobile = models.IntegerField()
    swimming = models.IntegerField()
    toboggan = models.IntegerField()
    volunteer = models.IntegerField()
    zip_line = models.IntegerField()
    nature_preserve = models.IntegerField()
    no_fishing = models.IntegerField()
    driving_range = models.IntegerField()
    pavilion = models.IntegerField()
    recreation_center = models.IntegerField()
    bathroom_building_winter = models.IntegerField()
    bathroom_building_summer = models.IntegerField()
    bathroom_building_ada = models.IntegerField()
    bathroom_portable_summer = models.IntegerField()
    bathroom_portable_winter = models.IntegerField()
    bathroom_portable_ada = models.IntegerField()
    shower = models.IntegerField()
    dining_hall = models.IntegerField()
    sanitation_station = models.IntegerField()
    camp_store = models.IntegerField()
    no_dogs = models.IntegerField()
    fitness_stairs = models.IntegerField()
    accessible_shelter = models.IntegerField()
    accessible_canoe = models.IntegerField()
    accessible_boat = models.IntegerField()
    accessible_fishing = models.IntegerField()
    accessible_campsite = models.IntegerField()


class PoiDesc(GISModel):
    """Table of POI description for a select group of POIs.
     Mainly used for the webmap. Foreign Key reference poi_info.poi_info_id."""

    class Meta(GISModel.Meta):
        db_table = '"quercus"."poi_desc"'
        indexes = [
            models.Index(fields=['poi_info_id'])
        ]

    id = models.AutoField(primary_key=True, db_column='poi_desc_id')
    poi_info = models.ForeignKey('PoiInfo', on_delete=models.CASCADE)

    hours1 = models.CharField(max_length=150)
    hours2 = models.CharField(max_length=150)
    phone = models.CharField(max_length=12)
    description = models.CharField(max_length=500)
    web_link = models.CharField(max_length=150)
    map_link = models.CharField(max_length=150)
    map_link_spanish = models.CharField(max_length=150)
    vol_link = models.CharField(max_length=150)
    vol_link2 = models.CharField(max_length=150)
    picnic_link = models.CharField(max_length=150)
    event_link = models.CharField(max_length=150)
    custom_link = models.CharField(max_length=150)
    season1 = models.CharField(max_length=50)
    season2 = models.CharField(max_length=50)
    special_hours = models.CharField(max_length=150)
    special_description = models.CharField(max_length=500)
    special_link = models.CharField(max_length=150)
    photo_link = models.CharField(max_length=150)
    fish_map = models.CharField(max_length=150)
    accessibility_description = models.CharField(max_length=1050)


class PoiInfo(GISModel):
    """Main table to the point of interest (POI) containing
     the main attributes for those points."""

    class Meta(GISModel.Meta):
        db_table = '"quercus"."poi_info"'
        indexes = [
            models.Index(fields=['nameid']),
            models.Index(fields=['parking_connection_id']),
            models.Index(fields=['parking_info_id']),
            models.Index(fields=['pointsofinterest_id'])
        ]

    class Search:
        fields = (
            ('fpd_uid', int),
            ('nameid__name', str),
        )

        not_null_fields = ['parking_info_id']

    id = models.AutoField(primary_key=True, db_column='poi_info_id')

    parking_info = models.ForeignKey(ParkingEntranceInfo, on_delete=models.RESTRICT)
    parking_connection = models.ForeignKey(ParkingEntranceInfo, on_delete=models.RESTRICT)

    nameid = models.ForeignKey(Names, on_delete=models.RESTRICT, db_column='nameid')

    point_type = models.CharField(max_length=50)
    addr = models.CharField(max_length=100)
    zip = models.CharField(max_length=5)
    zipmuni = models.CharField(max_length=50)
    municipality = models.CharField(max_length=50)
    public_access = models.CharField(max_length=25)
    latitude = models.DecimalField(max_digits=15, decimal_places=13)
    longitude = models.DecimalField(max_digits=15, decimal_places=13)
    commdist = models.IntegerField()
    zone_name = models.CharField(max_length=10)
    zonemapno = models.IntegerField()
    dwmapno = models.IntegerField()

    pointsofinterest_id = models.IntegerField()

    fpd_uid = models.IntegerField()
    web_poi = models.CharField(max_length=80)
    web_street_addr = models.CharField(max_length=100)
    web_muni_addr = models.CharField(max_length=100)

    alt_nameid = models.IntegerField()
    alt2_nameid = models.IntegerField()
    trail_info_id = models.IntegerField()
    poi_info_id_group = models.IntegerField()
    maintenance_div = models.CharField(max_length=15)
    maintenance_div_nickname = models.CharField(max_length=25)


class PoiToTrails(GISModel):
    """No longer used"""

    class Meta(GISModel.Meta):
        db_table = '"quercus"."poi_to_trails"'
        indexes = [
            models.Index(fields=['poi_info_id']),
            models.Index(fields=['trail_info_id'])
        ]

    # This table has no pk specified, but it is indexed by these fields.
    # Django models require a PK, so set both of these fields as primary keys.
    # Otherwise, without a PK set, this model won't work.
    # See https://stackoverflow.com/a/28516276
    # and https://stackoverflow.com/q/55127195
    poi_info = models.ForeignKey('PoiInfo', on_delete=models.DO_NOTHING, primary_key=True)
    trail_info = models.ForeignKey('TrailsInfo', on_delete=models.DO_NOTHING, primary_key=True)
    distance = models.FloatField()


class PointsOfInterest(GISModel):
    """Geometry table to the points of interest.
     Foreign Key Reference poi_info.poi_info_id."""

    class Meta(GISModel.Meta):
        db_table = '"quercus"."pointsofinterest"'

    id = models.AutoField(primary_key=True, db_column='pointsofinterest_id')
    geom = models.PointField(srid=3435, spatial_index=True)
    web_map_geom = models.PointField(srid=4326)
    poi_info = models.ForeignKey('PoiInfo', on_delete=models.CASCADE)


class Regions(GISModel):
    """This table has been moved to pinus.regoins.
     Should be removed from quercus in the future."""

    class Meta(GISModel.Meta):
        db_table = '"quercus"."regions"'

    id = models.AutoField(primary_key=True, db_column='region_id')
    region_number = models.IntegerField()
    geom = models.MultiPolygonField(srid=3435)


class Signage(GISModel):
    """Point table of misc. features on FPDCC property.
     Including; signs, markers, utilities, monuments,
     manhole covers, culverts, bridges, etc."""

    class Meta(GISModel.Meta):
        db_table = '"quercus"."signage"'

    id = models.AutoField(primary_key=True, db_column='signage_id')
    geom = models.PointField(srid=3435, spatial_index=True)

    type = models.CharField(max_length=254)
    division = models.CharField(max_length=254)
    zone = models.CharField(max_length=254)
    preserve = models.CharField(max_length=254)
    trail_system = models.CharField(max_length=254)
    trail_color = models.CharField(max_length=254)
    comment = models.CharField(max_length=254)
    old_name = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    path = models.CharField(max_length=60)
    full_path = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=15, decimal_places=13)
    longitude = models.DecimalField(max_digits=15, decimal_places=13)
    poi_info_id = models.IntegerField()
    current_image_date = models.DateField()
    sub_type = models.CharField(max_length=254)
    trail_segment_id = models.IntegerField()
    status = models.CharField(max_length=25)
    removed = models.CharField(max_length=3)
    bad_image = models.CharField(max_length=3)


class TrailSubsystemLu(GISModel):
    """Look up table for trail_subsystem ID. Mainly used for the webmap."""

    class Meta(GISModel.Meta):
        db_table = '"quercus"."trail_subsystem_lu"'

    trail_subsystem = models.CharField(primary_key=True, max_length=140, db_column='trail_subsystem')
    trail_subsystem_id = models.IntegerField()


class Trails(GISModel):
    """Main table for trails. Containing main attributes for that describe each trail."""

    class Meta(GISModel.Meta):
        db_table = '"quercus"."trails"'

    trails_id = models.AutoField(primary_key=True)
    geom = models.LineStringField(srid=3435, spatial_index=True)

    # topogeom isn't implemented


class TrailsAmenity(GISModel):
    """Geometry table for Trails. Each official trail tries to maintain topological consistency."""

    class Meta(GISModel.Meta):
        db_table = '"quercus"."trails_amenity"'

    id = models.AutoField(primary_key=True, db_column='trails_amenities_id')

    trail_info = models.ForeignKey('TrailsInfo', on_delete=models.DO_NOTHING)

    # For the following group of fields, the type is
    # `quercus.bin_1_0_dom`, an integer that can only be 1 or 0.
    hiking = models.IntegerField()
    biking = models.IntegerField()
    cross_country = models.IntegerField()
    rollerblade = models.IntegerField()
    snowshoe = models.IntegerField()
    interpretive = models.IntegerField()
    equestrian = models.IntegerField()
    dog_leash = models.IntegerField()
    no_dogs = models.IntegerField()


class TrailsDesc(GISModel):
    """Table of all amenities associated with a trail segment.
     Foreign Key reference trail_info.trail_info_id."""

    class Meta(GISModel.Meta):
        db_table = '"quercus"."trails_desc"'

    id = models.AutoField(primary_key=True, db_column='trail_desc_id')
    trail_subsystem = models.CharField(max_length=100)
    alt_name = models.CharField(max_length=50)
    trail_desc = models.CharField(max_length=250)
    map_link = models.CharField(max_length=150)
    map_link_spanish = models.CharField(max_length=150)
    photo_link = models.CharField(max_length=150)
    web_note = models.CharField(max_length=125)
    hours1 = models.CharField(max_length=150)
    hours2 = models.CharField(max_length=150)
    season1 = models.CharField(max_length=50)
    season2 = models.CharField(max_length=50)
    special_hours = models.CharField(max_length=150)
    web_link = models.CharField(max_length=150)


class TrailsInfo(GISModel):
    """Table of trail descriptions for a select group of trails.
     Mainly used for the webmap. Foreign Key reference trail_info.trail_info_id."""

    class Meta(GISModel.Meta):
        db_table = '"quercus"."trails_info"'

    class Search:
        fields = (
            ('trails', int),
            ('trail_subsystem', str),
        )

    id = models.AutoField(primary_key=True, db_column='trail_info_id')
    trails = models.ForeignKey(Trails, on_delete=models.RESTRICT)

    trail_system = models.CharField(max_length=100)
    trail_subsystem = models.CharField(max_length=100)
    trail_color = models.CharField(max_length=50)
    trail_surface = models.CharField(max_length=50)
    trail_type = models.CharField(max_length=50)
    trail_difficulty = models.CharField(max_length=50)
    regional_trail_name = models.CharField(max_length=50)
    trail_desc = models.CharField(max_length=250)
    gps = models.CharField(max_length=25)
    comment = models.CharField(max_length=254)
    alt_name = models.CharField(max_length=50)
    cambr_name = models.CharField(max_length=50)
    on_street = models.CharField(max_length=25)
    crossing_type = models.CharField(max_length=25)
    unrecognized = models.CharField(max_length=25)
    length_mi = models.DecimalField(max_digits=10, decimal_places=3)
    off_fpdcc = models.CharField(max_length=25)
    web_trail = models.CharField(max_length=25)
    maintenance = models.CharField(max_length=50)
    length_ft = models.DecimalField(max_digits=10, decimal_places=2)
    segment_type = models.CharField(max_length=4)
    direction = models.CharField(max_length=15)
    width = models.DecimalField(max_digits=4, decimal_places=1)
    gps_date = models.DateField()
    trail_name = models.CharField(max_length=50)


class TrailsMaintenance(GISModel):
    """Table of attributes to identify maintenance responsibilities for trails
     not only on FPDCC property but within the county trail system directly linked to the FPDCC.
     Forgein Key reference trail_info.trail_info_id."""

    class Meta(GISModel.Meta):
        db_table = '"quercus"."trails_maintenance"'

    id = models.AutoField(primary_key=True, db_column='trails_maintenance_id')
    poi_info = models.ForeignKey(TrailsInfo, on_delete=models.DO_NOTHING)
    iga_number = models.IntegerField()
    iga_doc = models.CharField(max_length=250)
    maintained_by = models.CharField(max_length=50)


class FPDCCZones(GISModel):
    class Meta(GISModel.Meta):
        db_table = '"pinus"."zones"'

    id = models.AutoField(primary_key=True, db_column='id')
    zone = models.CharField(max_length=10)
    geom = models.MultiPolygonField(srid=3435)
    abbr = models.CharField(max_length=10)


class FPDCCCommissionerDistricts(GISModel):
    class Meta(GISModel.Meta):
        db_table = '"pinus"."commdistricts"'

    id = models.AutoField(primary_key=True, db_column='id')
    district = models.CharField(max_length=10)
    geom = models.GeometryField(srid=3435)


class FPDCCSenateDistricts(GISModel):
    class Meta(GISModel.Meta):
        db_table = '"pinus"."il_senate_cb_2017_17_sldu_500k_cc"'

    id = models.AutoField(primary_key=True, db_column='id')
    district = models.IntegerField()
    geom = models.GeometryField(srid=3435)


class FPDCCHouseDistricts(GISModel):
    class Meta(GISModel.Meta):
        db_table = '"pinus"."il_house_cb_2017_17_sldl_500k_cc"'

    id = models.AutoField(primary_key=True, db_column='id')
    district = models.IntegerField()
    geom = models.GeometryField(srid=3435)
