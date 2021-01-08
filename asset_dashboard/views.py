from django.shortcuts import render
from django.views.generic import TemplateView, ListView, FormView, DetailView, CreateView, UpdateView, edit, base
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.core import serializers
from django.urls import reverse
from .models import DummyProject, Project, ProjectScore
from .forms import ProjectForm, ProjectScoreForm
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


class AddProjectFormView(CreateView):
    template_name = 'asset_dashboard/partials/add_project_modal_form.html'
    form_class = ProjectForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            project = Project.objects.create(**form.cleaned_data)
            project_score = ProjectScore.objects.get_or_create(project=project)
            return HttpResponseRedirect(reverse('project-detail', kwargs={'pk': project.pk}))
        else:
            return HttpResponseBadRequest('Form is invalid.')


class ProjectScoreContextMixin(base.ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        project_score = self.object if isinstance(self.object, ProjectScore) else self.object.projectscore

        context.update({
            'project_score_form': ProjectScoreForm(instance=project_score),
            'project_score_pk': project_score.id
        })

        return context


class ProjectDetailView(ProjectScoreContextMixin, DetailView):
    model = Project
    template_name = 'asset_dashboard/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'project_form': ProjectForm(instance=self.object)
        })

        return context


class ProjectUpdateView(UpdateView):
    model = Project
    template_name = 'asset_dashboard/partials/forms/project_form.html'
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('project-detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, 'Project successfully saved!')
        return super().form_valid(form)


class ProjectScoreUpdateView(ProjectScoreContextMixin, UpdateView):
    model = ProjectScore
    template_name = 'asset_dashboard/partials/forms/project_score_form.html'
    form_class = ProjectScoreForm

    def get_success_url(self):
        project = Project.objects.get(projectscore=self.kwargs['pk'])
        return reverse('project-detail', kwargs={'pk': project.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Project score successfully saved!')
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
