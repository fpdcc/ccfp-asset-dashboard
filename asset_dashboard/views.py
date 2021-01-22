from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.core import serializers
from django.urls import reverse
from .models import DummyProject, Project, ProjectScore
from .forms import ProjectForm, ProjectScoreForm, ProjectCategoryForm
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

            messages.success(self.request, 'Project successfully created!')
            return HttpResponseRedirect(reverse('project-detail', kwargs={'pk': project.pk}))
        else:
            print('form invalid')
            print(form.errors)
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

        if self.request.POST:
            # instantiate the forms with data from the post request
            request_data = self.request.POST

            context['score_form'] = ProjectScoreForm(request_data, instance=self.object.projectscore)
            context['category_form'] = ProjectCategoryForm(request_data, instance=self.object.category)
        else:
            context['score_form'] = ProjectScoreForm(instance=self.object.projectscore)
            context['category_form'] = ProjectCategoryForm(instance=self.object.category)

        return context

    def get_success_url(self):
        return reverse('project-detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        context = self.get_context_data()

        forms = {
            'project': form,
            'score': context['score_form'],
        }

        for form_instance in forms:
            form_to_save = forms[form_instance]

            if form_to_save.is_valid():
                form_to_save.save()
            else:
                return super().form_invalid(form)

        messages.success(self.request, 'Project successfully saved!')
        return super().form_valid(form)
