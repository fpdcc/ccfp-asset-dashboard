import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Project, ProjectCategory, ProjectFinances, ProjectScore, Section
from .forms import ProjectForm, ProjectScoreForm, ProjectCategoryForm, ProjectFinancesForm
from django.contrib import messages
from django.db.models import Q


class CipPlannerView(TemplateView):
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


class ProjectListView(ListView):
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


class ProjectListJson(BaseDatatableView):
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


class ProjectCreateView(CreateView):
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


class ProjectUpdateView(UpdateView):
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
