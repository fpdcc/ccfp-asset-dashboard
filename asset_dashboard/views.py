from django.shortcuts import render
from django.views.generic import TemplateView, ListView, FormView, DetailView, CreateView, UpdateView, edit
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.core import serializers
from django.urls import reverse
from .models import DummyProject, Project
from .forms import ProjectForm
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
            return HttpResponseRedirect(reverse('project-detail', kwargs={'pk': project.pk}))
        else:
            return HttpResponseBadRequest('Form is invalid.')


class ProjectDetailView(DetailView, edit.FormMixin):
    template_name = 'asset_dashboard/project_detail.html'
    model = Project
    form_class = ProjectForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProjectForm(initial={
                'name': self.object.name,
                'description': self.object.description,
                'section_owner': self.object.section_owner.pk
            })
        return context

    # How to make this "put" instead of "post" ?
    # The HTML standard dictates that an HTML form can have
    # only post and get requests, so a put fails here. 
    # See https://developer.mozilla.org/en-US/docs/Web/HTML/Element/form#attr-method
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            project = Project.objects.update(**form.cleaned_data)
            messages.success(request, 'Project successfully updated!')
            return HttpResponseRedirect(reverse('project-detail', kwargs={'pk': kwargs['pk']}))
