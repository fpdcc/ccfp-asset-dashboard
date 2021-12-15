import random

import pytest


def create_project(state, create_relations=True, **project_kwargs):
    """
    Given a state, create a Project and its relations. Pass additional kwargs
    to customize the default Project kwargs.
    """
    Project = state.apps.get_model('asset_dashboard', 'Project')

    default_kwargs = {
        'name': 'Test Project',
        'description': 'A project for testing',
    }
    default_kwargs.update(project_kwargs)

    project = Project.objects.create(**default_kwargs)

    if create_relations:
        ProjectFinances = state.apps.get_model('asset_dashboard', 'ProjectFinances')
        ProjectFundingYear = state.apps.get_model('asset_dashboard', 'ProjectFundingYear')

        budget = float(random.randint(1, 1000))
        ProjectFinances.objects.create(project=project, budget=budget)
        ProjectFundingYear.objects.create(project=project, year=2021, funds=budget)

    return project


def create_phase(state, create_relations=True, **phase_kwargs):
    """
    Given a state, create a Project and Phase. Pass additional kwargs to
    customize the default Phase kwargs.
    """
    Phase = state.apps.get_model('asset_dashboard', 'Phase')

    # If a project ID is provided, confirm that the relevant project exists.
    # Otherwise, create a default project to associate with a phase.
    if project_id := phase_kwargs.pop('project_id', None):
        Project = state.apps.get_model('asset_dashboard', 'Project')

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise ValueError(f'Provided project ID "{project_id}" does not exist')
        else:
            phase_kwargs['project'] = project
    else:
        project = create_project(state, create_relations=False)

    default_kwargs = {
        'project': project,
        'phase_type': 'implementation',
        'estimated_bid_quarter': 'Q1'
    }

    default_kwargs.update(phase_kwargs)

    phase = Phase.objects.create(**default_kwargs)

    if create_relations:
        PhaseFinances = state.apps.get_model('asset_dashboard', 'PhaseFinances')
        PhaseFundingYear = state.apps.get_model('asset_dashboard', 'PhaseFundingYear')

        budget = float(random.randint(1, 1000))
        PhaseFinances.objects.create(phase=phase, budget=budget)
        PhaseFundingYear.objects.create(phase=phase, year=2021, funds=budget)

    return phase


@pytest.mark.django_db
def test_migration_from_project_to_phase(migrator):
    # Apply all migrations up to the specified migration
    initial_state = migrator.apply_initial_migration(
        ('asset_dashboard', '0018_auto_20211124_2000'),
    )

    # Create two projects, one with a phase and one without
    project_1 = create_project(initial_state, estimated_bid_quarter='Q1')

    # Retrieve the funding year prior to applying the next migration, because
    # the funding year table changes in the migration, making this query
    # impossible to run afterwards
    project_1_funding_year = project_1.projectfundingyear_set.get()

    project_2 = create_project(initial_state, estimated_bid_quarter='Q2', phase='feasibility')
    project_2_funding_year = project_2.projectfundingyear_set.get()

    # Apply the new migration for testing
    forward_state = migrator.apply_tested_migration(
        ('asset_dashboard', '0019_add_phase'),
    )
    Project = forward_state.apps.get_model('asset_dashboard', 'Project')
    Phase = forward_state.apps.get_model('asset_dashboard', 'Phase')

    assert Project.objects.count() == Phase.objects.count()

    # Compare the generated Phases with the original Projects to confirm
    # attributes were migrated as expected
    phase_1 = Phase.objects.get(project__id=project_1.id)

    assert phase_1.estimated_bid_quarter == project_1.estimated_bid_quarter
    assert phase_1.phase_type == 'implementation'
    assert phase_1.phasefinances.budget == project_1.projectfinances.budget
    assert phase_1.phasefundingyear_set.get().funds == project_1_funding_year.funds

    phase_2 = Phase.objects.get(project__id=project_2.id)

    assert phase_2.estimated_bid_quarter == project_2.estimated_bid_quarter
    assert phase_2.phase_type == project_2.phase
    assert phase_2.phasefinances.budget == project_2.projectfinances.budget
    assert phase_2.phasefundingyear_set.get().funds == project_2_funding_year.funds

    migrator.reset()


@pytest.mark.django_db
def test_migration_from_phase_to_project(migrator):
    # Apply all migrations up to the specified migration
    initial_state = migrator.apply_initial_migration(
        ('asset_dashboard', '0019_add_phase')
    )

    phase_1 = create_phase(initial_state)

    # Retrieve the funding year prior to applying the next migration, because
    # the funding year table changes in the migration, making this query
    # impossible to run afterwards
    phase_1_funding_year = phase_1.phasefundingyear_set.get()

    # Create a phase with a custom phase type
    phase_2 = create_phase(initial_state, phase_type='design')
    phase_2_funding_year = phase_2.phasefundingyear_set.get()

    # Create a second phase associated with project ID number 2
    phase_3 = create_phase(initial_state, sequence=2, project_id=2)
    phase_3_funding_year = phase_3.phasefundingyear_set.get()

    # Assert only two Projects exist prior to the migration (because the third
    # phase is also associated with project ID number 2)
    assert initial_state.apps.get_model('asset_dashboard', 'Project').objects.count() == 2

    # Retrieve the number of Phases for comparison after the migration
    phase_count = initial_state.apps.get_model('asset_dashboard', 'Phase').objects.count()

    backward_state = migrator.apply_tested_migration(
        ('asset_dashboard', '0018_auto_20211124_2000'),
    )

    Project = backward_state.apps.get_model('asset_dashboard', 'Project')

    # Assert there is a Project for every Phase after the migration
    assert Project.objects.count() == phase_count

    # Check the generated Projects with the original Phases to confirm
    # attributes were migrated as expected
    project_1 = Project.objects.get(id=phase_1.project.id)

    assert project_1.estimated_bid_quarter == phase_1.estimated_bid_quarter
    assert project_1.phase == phase_1.phase_type
    assert project_1.projectfinances.budget == phase_1.phasefinances.budget
    assert project_1.projectfundingyear_set.get().funds == phase_1_funding_year.funds

    project_2 = Project.objects.get(id=phase_2.project.id)

    assert project_2.estimated_bid_quarter == phase_2.estimated_bid_quarter
    assert project_2.phase == phase_2.phase_type
    assert project_2.projectfinances.budget == phase_2.phasefinances.budget
    assert project_2.projectfundingyear_set.get().funds == phase_2_funding_year.funds

    project_3 = Project.objects.exclude(id__in=[project_1.id, project_2.id]).get()

    assert project_3.estimated_bid_quarter == phase_3.estimated_bid_quarter
    assert project_3.phase == phase_3.phase_type
    assert project_3.projectfinances.budget == phase_3.phasefinances.budget
    assert project_3.projectfundingyear_set.get().funds == phase_3_funding_year.funds

    migrator.reset()
