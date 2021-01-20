from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.core import serializers
from django.urls import reverse
from .models import DummyProject, Project, ProjectScore
from .forms import ProjectForm, ProjectScoreForm, ProjectCategoryForm, SenateDistrictFormset, HouseDistrictFormset, CommissionerDistrictFormset, ZoneFormset
from django.contrib import messages


class Home(TemplateView):
    title = 'home'
    template_name = 'asset_dashboard/index.html'
    component = 'js/pages/index.js'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        projects = serializers.serialize('json', DummyProject.objects.all())
        context['props'] = {'projects': projects}
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
        return context


class ProjectCreateView(CreateView):
    template_name = 'asset_dashboard/partials/add_project_modal_form.html'
    form_class = ProjectForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            project = Project.objects.create(**form.cleaned_data)
            ProjectScore.objects.get_or_create(project=project)
            return HttpResponseRedirect(reverse('project-detail', kwargs={'pk': project.pk}))
        else:
            return HttpResponseBadRequest('Form is invalid.')


class ProjectUpdateView(UpdateView):
    """
    Updated view that updates a Project and all related models.
    """
    model = Project
    template_name = 'asset_dashboard/project_detail.html'
    form_class = ProjectForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            # instantiate the forms with data from the post request
            request_data = self.request.POST

            context['score_form'] = ProjectScoreForm(request_data, instance=self.object.projectscore)
            context['category_form'] = ProjectCategoryForm(request_data, instance=self.object.category)
            context['senate_district_formset'] = SenateDistrictFormset(request_data, instance=self.object)
            context['house_district_formset'] = HouseDistrictFormset(request_data, instance=self.object)
            context['commissioner_district_formset'] = CommissionerDistrictFormset(request_data, instance=self.object)
            context['zone_formset'] = ZoneFormset(request_data, instance=self.object)
        else:
            context['score_form'] = ProjectScoreForm(instance=self.object.projectscore)
            context['category_form'] = ProjectCategoryForm(instance=self.object.category)
            context['senate_district_formset'] = SenateDistrictFormset(instance=self.object)
            context['house_district_formset'] = HouseDistrictFormset(instance=self.object)
            context['commissioner_district_formset'] = CommissionerDistrictFormset(instance=self.object)
            context['zone_formset'] = ZoneFormset(instance=self.object)

        return context

    def get_success_url(self):
        return reverse('project-detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        context = self.get_context_data()

        forms = {
            'project': form,
            'score': context['score_form'],
            'senate_district': context['senate_district_formset'],
            'house_district': context['house_district_formset'],
            'commissioner_district': context['commissioner_district_formset'],
            'zone_formset': context['zone_formset']
        }

        for form_instance in forms:
            form_to_save = forms[form_instance]

            if form_to_save.is_valid():
                form_to_save.save()
            else:
                return super().form_invalid(form)

        messages.success(self.request, 'Project successfully saved!')
        return super().form_valid(form)
