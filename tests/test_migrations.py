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


def create_task(state, create_relations=True, **task_kwargs):
    """
    Given a state, create a Project and Task. Pass additional kwargs to
    customize the default Task kwargs.
    """
    Task = state.apps.get_model('asset_dashboard', 'Task')

    # If a project ID is provided, confirm that the relevant project exists.
    # Otherwise, create a default project to associate with a task.
    if project_id := task_kwargs.pop('project_id', None):
        Project = state.apps.get_model('asset_dashboard', 'Project')

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise ValueError(f'Provided project ID "{project_id}" does not exist')
        else:
            task_kwargs['project'] = project
    else:
        project = create_project(state, create_relations=False)

    default_kwargs = {
        'project': project,
        'task_type': 'implementation',
        'estimated_bid_quarter': 'Q1'
    }

    default_kwargs.update(task_kwargs)

    task = Task.objects.create(**default_kwargs)

    if create_relations:
        TaskFinances = state.apps.get_model('asset_dashboard', 'TaskFinances')
        TaskFundingYear = state.apps.get_model('asset_dashboard', 'TaskFundingYear')

        budget = float(random.randint(1, 1000))
        TaskFinances.objects.create(task=task, budget=budget)
        TaskFundingYear.objects.create(task=task, year=2021, funds=budget)

    return task


@pytest.mark.django_db
def test_migration_from_project_to_task(migrator):
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
        ('asset_dashboard', '0019_add_task'),
    )
    Project = forward_state.apps.get_model('asset_dashboard', 'Project')
    Task = forward_state.apps.get_model('asset_dashboard', 'Task')

    assert Project.objects.count() == Task.objects.count()

    # Compare the generated Tasks with the original Projects to confirm
    # attributes were migrated as expected
    task_1 = Task.objects.get(project__id=project_1.id)

    assert task_1.estimated_bid_quarter == project_1.estimated_bid_quarter
    assert task_1.task_type == 'implementation'
    assert task_1.taskfinances.budget == project_1.projectfinances.budget
    assert task_1.taskfundingyear_set.get().funds == project_1_funding_year.funds

    task_2 = Task.objects.get(project__id=project_2.id)

    assert task_2.estimated_bid_quarter == project_2.estimated_bid_quarter
    assert task_2.task_type == project_2.phase
    assert task_2.taskfinances.budget == project_2.projectfinances.budget
    assert task_2.taskfundingyear_set.get().funds == project_2_funding_year.funds

    migrator.reset()


@pytest.mark.django_db
def test_migration_from_task_to_project(migrator):
    # Apply all migrations up to the specified migration
    initial_state = migrator.apply_initial_migration(
        ('asset_dashboard', '0019_add_task')
    )

    task_1 = create_task(initial_state)

    # Retrieve the funding year prior to applying the next migration, because
    # the funding year table changes in the migration, making this query
    # impossible to run afterwards
    task_1_funding_year = task_1.taskfundingyear_set.get()

    # Create a task with a custom task type
    task_2 = create_task(initial_state, task_type='design')
    task_2_funding_year = task_2.taskfundingyear_set.get()

    # Create a second task associated with project ID number 2
    task_3 = create_task(initial_state, sequence=2, project_id=2)
    task_3_funding_year = task_3.taskfundingyear_set.get()

    # Assert only two Projects exist prior to the migration (because the third
    # task is also associated with project ID number 2)
    assert initial_state.apps.get_model('asset_dashboard', 'Project').objects.count() == 2

    # Retrieve the number of Tasks for comparison after the migration
    task_count = initial_state.apps.get_model('asset_dashboard', 'Task').objects.count()

    backward_state = migrator.apply_tested_migration(
        ('asset_dashboard', '0018_auto_20211124_2000'),
    )

    Project = backward_state.apps.get_model('asset_dashboard', 'Project')

    # Assert there is a Project for every Task after the migration
    assert Project.objects.count() == task_count

    # Check the generated Projects with the original Tasks to confirm
    # attributes were migrated as expected
    project_1 = Project.objects.get(id=task_1.project.id)

    assert project_1.estimated_bid_quarter == task_1.estimated_bid_quarter
    assert project_1.phase == task_1.task_type
    assert project_1.projectfinances.budget == task_1.taskfinances.budget
    assert project_1.projectfundingyear_set.get().funds == task_1_funding_year.funds

    project_2 = Project.objects.get(id=task_2.project.id)

    assert project_2.estimated_bid_quarter == task_2.estimated_bid_quarter
    assert project_2.phase == task_2.task_type
    assert project_2.projectfinances.budget == task_2.taskfinances.budget
    assert project_2.projectfundingyear_set.get().funds == task_2_funding_year.funds

    project_3 = Project.objects.exclude(id__in=[project_1.id, project_2.id]).get()

    assert project_3.estimated_bid_quarter == task_3.estimated_bid_quarter
    assert project_3.phase == task_3.task_type
    assert project_3.projectfinances.budget == task_3.taskfinances.budget
    assert project_3.projectfundingyear_set.get().funds == task_3_funding_year.funds

    migrator.reset()
