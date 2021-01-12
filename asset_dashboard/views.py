from django.shortcuts import render
from django.views.generic import TemplateView, ListView, FormView, DetailView, CreateView, UpdateView, edit, base
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.core import serializers
from django.urls import reverse
from .models import DummyProject, Project, ProjectScore, ProjectCategory
from .forms import ProjectForm, ProjectScoreForm
from django.forms import inlineformset_factory
from django.db import transaction
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


class CreateProjectView(CreateView):
    template_name = 'asset_dashboard/partials/add_project_modal_form.html'
    form_class = ProjectForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            project = Project.objects.create(**form.cleaned_data)
            project_score = ProjectScore.objects.get_or_create(project=project)
            project_category = ProjectCategory.objects.get_or_create(project=project, category='N\/A')
            return HttpResponseRedirect(reverse('project-detail', kwargs={'pk': project.pk}))
        else:
            return HttpResponseBadRequest('Form is invalid.')


class ProjectDetailView(UpdateView):
    """
    Detail view that updates a Project and all related models.
    """
    model = Project
    template_name = 'asset_dashboard/project_detail.html'
    form_class = ProjectForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['score_form'] = ProjectScoreForm(self.request.POST, instance=self.object.projectscore)
        else:
            context['score_form'] = ProjectScoreForm(instance=self.object.projectscore)

        return context

    def get_success_url(self):
        return reverse('project-detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        context = self.get_context_data()

        score_form = context['score_form']
        project_form = context['form']
        
        if form.is_valid() and score_form.is_valid():
            form.save()
            score_form.save()
            messages.success(self.request, 'Project successfully saved!')
            return super().form_valid(form)
        else:
            return super().form_invalid(form, score_form)
