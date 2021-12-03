import pytest

from django.db.utils import ProgrammingError

from asset_dashboard.models import Section, NaturePreserves


@pytest.mark.django_db(databases=['default', 'fp_postgis'])
def test_gis_query(nature_preserves):
    assert NaturePreserves.objects.db == 'fp_postgis'
    assert NaturePreserves.objects.count() == 1

    with pytest.raises(ProgrammingError) as excinfo:
        NaturePreserves.objects.using('default').count()
        assert 'relation "quercus.nature_preserves" does not exist' in str(excinfo.value)


@pytest.mark.django_db(databases=['default', 'fp_postgis'])
def test_nongis_query(section_owner):
    assert Section.objects.db == 'default'
    assert Section.objects.count() == 1

    with pytest.raises(ProgrammingError) as excinfo:
        Section.objects.using('fp_postgis').count()
        assert 'relation asset_dashboard_section does not exist' in str(excinfo.value)
