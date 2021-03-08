import json
import re
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import HouseDistrict, Project, ProjectCategory, ProjectFinances, ProjectScore, Section, SenateDistrict, CommissionerDistrict
from .forms import ProjectForm, ProjectScoreForm, ProjectCategoryForm, ProjectFinancesForm
from django.contrib import messages
from django.db.models import Q
from django.utils.html import escape


class CipPlannerView(LoginRequiredMixin, TemplateView):
    title = 'CIP Planner'
    template_name = 'asset_dashboard/planner.html'
    component = 'js/planner.js'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        projects = Project.objects.all()
        projects = projects.select_related('section_owner', 'category', 'projectfinances', 'projectscore')

        projects_list = []
        for prj in projects:
            project = {
                'pk': prj.id,
                'name': prj.name,
                'description': prj.description,
                'section': prj.section_owner.name,
                'category': prj.category.name,
                'total_budget': prj.projectfinances.budget.amount,
                'total_score': prj.projectscore.total_score,
                'phase': prj.phase,
                'zones': list(prj.zones.all().values('name')),
                'house_districts': list(prj.house_districts.all().values('name')),
                'senate_districts': list(prj.senate_districts.all().values('name')),
                'commissioner_districts': list(prj.commissioner_districts.all().values('name'))
            }
            projects_list.append(project)

        context['props'] = {'projects': json.dumps(projects_list, cls=DjangoJSONEncoder)}
        return context


def page_not_found(request, exception, template_name='asset_dashboard/404.html'):
    return render(request, template_name, status=404)


def server_error(request, template_name='asset_dashboard/500.html'):
    return render(request, template_name, status=500)


class ProjectListView(LoginRequiredMixin, ListView):
    template_name = 'asset_dashboard/projects.html'
    queryset = Project.objects.all()
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # send the form to a modal in this view
        form = ProjectForm()
        context['form'] = form

        # need all of the Sections and Categories for filtering the table
        context['sections'] = [s.name for s in Section.objects.all().order_by('name')]
        context['categories'] = [c.name for c in ProjectCategory.objects.all().order_by('name')]

        return context


class ProjectListJson(LoginRequiredMixin, BaseDatatableView):
    model = Project
    columns = ['name', 'description', 'section_owner', 'category', 'id']
    order_columns = ['name', 'description', 'section_owner__name', 'category__category']
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        section = self.request.GET.get('columns[2][search][value]', None)
        category = self.request.GET.get('columns[3][search][value]', None)

        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(description__icontains=search))

        if section:
            qs = qs.filter(section_owner__name=section)

        if category:
            qs = qs.filter(Q(category__name=category))

        return qs


class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = 'asset_dashboard/partials/forms/add_project_modal_form.html'
    form_class = ProjectForm

    def form_valid(self, form):
        if form.is_valid():
            project_data = {
                'name': form.cleaned_data['name'],
                'description': form.cleaned_data['description'],
                'section_owner': form.cleaned_data['section_owner'],
                'category': form.cleaned_data['category']
            }

            project = Project.objects.create(**project_data)
            ProjectScore.objects.get_or_create(project=project)
            ProjectFinances.objects.get_or_create(project=project)

            messages.success(self.request, 'Project successfully created!')
            return HttpResponseRedirect(reverse('project-detail', kwargs={'pk': project.pk}))
        else:
            return super().form_invalid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    """
    Updated view that updates a Project and all related models.
    """
    model = Project
    template_name = 'asset_dashboard/project_detail.html'
    form_class = ProjectForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        project_finances, _ = ProjectFinances.objects.get_or_create(project_id=self.object.id)

        if self.request.POST:
            # instantiate the forms with data from the post request
            request_data = self.request.POST

            context['score_form'] = ProjectScoreForm(request_data, instance=self.object.projectscore)
            context['category_form'] = ProjectCategoryForm(request_data, instance=self.object.category)
            context['finances_form'] = ProjectFinancesForm(request_data, instance=project_finances)
        else:
            context['total_score'] = ProjectScore.objects.get(project=self.object).total_score
            context['score_form'] = ProjectScoreForm(instance=self.object.projectscore)
            context['category_form'] = ProjectCategoryForm(instance=self.object.category)
            context['finances_form'] = ProjectFinancesForm(instance=project_finances)

        return context

    def get_success_url(self):
        return reverse('project-detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        context = self.get_context_data()

        forms = {
            'project': form,
            'score': context['score_form'],
            'finances': context['finances_form']
        }

        for form_instance in forms:
            form_to_save = forms[form_instance]

            if form_to_save.is_valid():
                form_to_save.save()
            else:
                return super().form_invalid(form)

        messages.success(self.request, 'Project successfully saved!')
        return super().form_valid(form)


class ProjectsByDistrictListView(LoginRequiredMixin, ListView):
    template_name = 'asset_dashboard/projects_by_district_list.html'
    queryset = Project.objects.all()
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['senate_districts'] = SenateDistrict.objects.all()
        context['house_districts'] = HouseDistrict.objects.all()
        context['commissioner_districts'] = CommissionerDistrict.objects.all()

        return context


class ProjectsByDistrictListJson(LoginRequiredMixin, BaseDatatableView):
    model = Project
    columns = ['name', 'description', 'senate_districts', 'house_districts', 'commissioner_districts', 'id']
    order_columns = ['name', 'description']
    max_display_length = 500

    def filter_queryset(self, qs):
        senate_district = self.request.GET.get('columns[2][search][value]', None)
        house_district = self.request.GET.get('columns[3][search][value]', None)
        commissioner_district = self.request.GET.get('columns[4][search][value]', None)

        if senate_district:
            qs = qs.filter(senate_districts__name=senate_district)

        if house_district:
            qs = qs.filter(house_districts__name=house_district)

        if commissioner_district:
            qs = qs.filter(commissioner_districts__name=commissioner_district)

        return qs

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        json_data = []

        for item in qs:
            senate_districts = self.format_district_names(item.senate_districts)
            house_districts = self.format_district_names(item.house_districts)
            commissioner_districts = self.format_district_names(item.commissioner_districts)

            json_data.append([
                escape(item.name),
                escape(item.description),
                escape(senate_districts),
                escape(house_districts),
                escape(commissioner_districts),
                item.id
            ])

        return json_data

    def format_district_names(self, districts):
        """Parses a queryset of districts into something consumable by the table library."""

        # create a string with names separated by commma
        district_names = ', '.join([d.name for d in districts.all()])

        # only return the district's number and comma/space between numbers
        return re.sub('[^0-9, ]', '', district_names)
