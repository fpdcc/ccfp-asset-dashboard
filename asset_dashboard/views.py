from django.shortcuts import render
from django.views.generic import TemplateView, ListView, FormView, DetailView
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.core import serializers
from django.urls import reverse
from .models import DummyProject, Project
from .forms import ProjectForm


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


class AddEditProjectForm(FormView):
    template_name = 'asset_dashboard/partials/add_edit_project_form.html'
    form_class = ProjectForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            self.fcc_form = form.save()
           
            # redirect to the new Project's detail page
            return HttpResponseRedirect(reverse('project-detail', kwargs={'pk': self.fcc_form.id}))
        else:
            return HttpResponseBadRequest('Form data was invalid.')


class ProjectDetailView(DetailView):
    template_name = 'asset_dashboard/project_detail.html'
    model = Project