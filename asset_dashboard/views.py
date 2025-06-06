import json
import re
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.html import escape
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from django_datatables_view.base_datatable_view import BaseDatatableView

from .models import HouseDistrict, LocalAsset, Project, ProjectCategory, ProjectScore, \
    Section, SenateDistrict, CommissionerDistrict, Phase, FundingStream
from .forms import ProjectForm, ProjectScoreForm, ProjectCategoryForm, \
    FundingStreamForm, PhaseForm
from .serializers import PortfolioSerializer, LocalAssetReadSerializer


class CipPlannerView(LoginRequiredMixin, TemplateView):
    title = 'CIP Planner'
    template_name = 'asset_dashboard/planner.html'
    component = 'js/PortfolioPlanner.js'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        portfolios = []
        selected_portfolio = None

        if self.request.user.portfolio_set.count():
            portfolios = PortfolioSerializer(
                self.request.user.portfolio_set.order_by('-updated_at'),
                many=True
            ).data
            selected_portfolio = portfolios[0]

        phases = Phase.objects.all().select_related('project').prefetch_related('funding_streams')

        project_phases = []
        for phase in phases:
            funding_streams = phase.funding_streams.all()

            section = phase.project.section_owner.name \
                if phase.project.section_owner else ''
            category = phase.project.category.name \
                if phase.project.category else ''

            project_phases.append({
                'pk': phase.id,
                'phase': phase.get_phase_type_display(),
                'total_budget': phase.total_budget,
                'funded_amount': phase.total_funded_amount,
                'funded_amount_by_year': phase.funded_amount_by_year,
                'funding_streams': list(funding_streams.values()) if funding_streams else [],
                'phase_year': phase.year,
                'estimated_bid_quarter': phase.estimated_bid_quarter,
                'phase_status': phase.status,
                'phase_type': phase.get_phase_type_display(),
                'name': phase.project.name,
                'description': phase.project.description,
                'notes': phase.project.notes,
                'section': section,
                'category': category,
                'total_score': phase.project.projectscore.total_score,
                'project_manager': phase.project.project_manager,
                'countywide': phase.project.countywide,
                'zones': list(phase.project.zones.all().values('name')),
                'cost_by_zone': phase.cost_by_zone,
                'house_districts': list(phase.project.house_districts.all().values('name')),
                'senate_districts': list(phase.project.senate_districts.all().values('name')),
                'commissioner_districts': list(phase.project.commissioner_districts.all().values('name')),
                'assets': LocalAsset.group_assets_by_type(phase.localasset_set.all().values('asset_id', 'asset_model')),
                'project_id': phase.project.id,
                'project_status': phase.project.get_status_display(),
                'project_requester': phase.project.get_requester_display(),
            })

        context['props'] = {
            'projects': json.dumps(project_phases, cls=DjangoJSONEncoder),
            'portfolios': portfolios,
            'selectedPortfolio': selected_portfolio,
            'userId': self.request.user.id,
            'fundingSourceOptions': [{'value': type[0], 'label': type[1]} for type in FundingStream.SOURCE_TYPE_CHOICES],
            'phaseOptions': [{'value': type[0], 'label': type[1]} for type in Phase.PHASE_TYPE_CHOICES]
        }
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

        # send a new Project form to the modal in this view's template
        form = ProjectForm()
        context['form'] = form

        # need all of the Sections and Categories for filtering the table
        context['sections'] = [s.name for s in Section.objects.all().order_by('name')]
        context['categories'] = [c.name for c in ProjectCategory.objects.all().order_by('name')]

        return context


class ProjectListJson(LoginRequiredMixin, BaseDatatableView):
    model = Project
    columns = ['id', 'name', 'description', 'section_owner', 'category', 'project_manager']
    order_columns = ['id', 'name', 'description', 'section_owner__name', 'category__name', 'project_manager']
    max_display_length = 500

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        section = self.request.GET.get('columns[3][search][value]', None)
        category = self.request.GET.get('columns[4][search][value]', None)

        if search:
            qs = qs.filter(Q(id__startswith=search) | Q(name__icontains=search) | Q(description__icontains=search) | Q(project_manager__icontains=search))

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
                'category': form.cleaned_data['category'],
                'project_manager': form.cleaned_data['project_manager']
            }

            project = Project.objects.create(**project_data)

            # Default all the score fields to 0 when a Project is created
            ProjectScore.objects.get_or_create(
                project=project,
                core_mission_score=0,
                operations_impact_score=0,
                sustainability_score=0,
                ease_score=0,
                geographic_distance_score=0,
                social_equity_score=0
            )

            messages.success(self.request, 'Project successfully created.')
            return HttpResponseRedirect(reverse('project-detail', kwargs={'pk': project.pk}))
        else:
            return super().form_invalid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    """
    Project detail view for updating a Project.
    """
    model = Project
    template_name = 'asset_dashboard/project_detail.html'
    form_class = ProjectForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            request_data = self.request.POST

            context['score_form'] = ProjectScoreForm(request_data, instance=self.object.projectscore)
            context['category_form'] = ProjectCategoryForm(request_data, instance=self.object.category)
        else:
            context['total_score'] = ProjectScore.objects.get(project=self.object).total_score
            context['score_form'] = ProjectScoreForm(instance=self.object.projectscore)
            context['category_form'] = ProjectCategoryForm(instance=self.object.category)

            context['phases'] = Phase.objects.annotate().filter(project=self.kwargs['pk']).order_by('sequence')

            assets = LocalAsset.objects.filter(phase__project=self.object)

            if assets.exists():
                context['props'] = {
                    'assets': LocalAssetReadSerializer(assets, many=True).data
                }

        return context

    def get_success_url(self):
        return reverse('project-detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        context = self.get_context_data()

        forms = {
            'project': form,
            'score': context['score_form']
        }

        for form_instance in forms:
            form_to_save = forms[form_instance]

            if form_to_save.is_valid():
                form_to_save.save()
            else:
                return super().form_invalid(form)

        messages.success(self.request, 'Project successfully saved.')
        return super().form_valid(form)


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project

    def get_success_url(self):
        messages.success(self.request, 'Project successfully deleted.')
        return reverse('projects')


class PhaseCreateView(LoginRequiredMixin, CreateView):
    template_name = 'asset_dashboard/partials/forms/add_edit_phase_form.html'
    form_class = PhaseForm

    def form_valid(self, form):
        if form.is_valid():
            phase_data = {
                **form.cleaned_data,
                'project_id': self.kwargs['pk']
            }

            phase = Phase.objects.create(**phase_data)

            messages.success(self.request, 'Phase successfully created.')
            return HttpResponseRedirect(reverse('edit-phase', kwargs={'pk': phase.pk}))
        else:
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['project'] = Project.objects.get(id=self.kwargs['pk'])

        return context


class PhaseUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'asset_dashboard/partials/forms/add_edit_phase_form.html'
    form_class = PhaseForm
    model = Phase

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['project'] = self.object.project

        context['props'] = {
            'phase_id': self.object.pk,
            'is_countywide': self.object.project.countywide
        }

        assets = LocalAsset.objects.filter(phase=self.object)

        if assets.exists():
            context['props'].update({
                'assets': LocalAssetReadSerializer(assets, many=True).data
            })

        context['funding_streams'] = self.object.funding_streams.all()
        context['existing_funding_forms'] = []

        for funding in context['funding_streams']:
            context['existing_funding_forms'].append(
                {
                    'id': funding.id,
                    'funding': FundingStreamForm(initial={
                        'budget': funding.budget,
                        'year': funding.year,
                        'funding_secured': funding.funding_secured,
                        'source_type': funding.source_type,
                        'actual_cost': funding.actual_cost,
                    })
                }
            )

        # Set the initial values to something more readable than the default: [Decimal('0'), 'USD']
        context['form'].funding_streams.base_fields['budget'].initial = '$0'
        context['form'].funding_streams.base_fields['actual_cost'].initial = '$0'

        return context

    def form_valid(self, form):
        if form.is_valid():
            phase = form.save()

            messages.success(self.request, 'Phase successfully updated.')
            return HttpResponseRedirect(reverse('edit-phase', kwargs={'pk': phase.pk}))
        else:
            return super().form_invalid(form)


class PhaseDeleteView(LoginRequiredMixin, DeleteView):
    model = Phase

    def get_success_url(self):
        context = self.get_context_data()
        messages.success(self.request, 'Phase successfully deleted.')
        return reverse('project-detail', kwargs={'pk': context['phase'].project.id})


class FundingStreamDeleteView(LoginRequiredMixin, DeleteView):
    model = FundingStream

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['funding_phase'] = context['object'].phase_set.get()
        return context

    def get_success_url(self):
        context = self.get_context_data()
        messages.success(self.request, 'Funding Stream successfully deleted.')
        return reverse('edit-phase', kwargs={'pk': context['funding_phase'].id})


class AssetAddEditView(LoginRequiredMixin, TemplateView):
    template_name = 'asset_dashboard/asset_create_update.html'
    component = 'js/components/maps/SelectAssetsMap.js'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        phase = Phase.objects.get(id=self.kwargs['pk'])
        phase_list = Phase.objects.filter(project=phase.project).values(
            'id', 'phase_type', 'estimated_bid_quarter', 'status', 'year'
        )

        context.update({
            'phase': phase,
            'project': phase.project,
            'props': {
                'phase_id': phase.id,
                'phase_name': phase.name,
                'phases': json.dumps(list(phase_list), cls=DjangoJSONEncoder)
            }
        })

        existing_assets = LocalAsset.objects.filter(phase=phase)
        geojson_serializer = LocalAssetReadSerializer(existing_assets, many=True)

        if existing_assets.exists():
            context['props'].update({
                'existing_assets': geojson_serializer.data
            })

        return context


class ProjectsByDistrictListView(LoginRequiredMixin, ListView):
    template_name = 'asset_dashboard/projects_by_district_list.html'
    queryset = Project.objects.all()
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['senate_districts'] = SenateDistrict.objects.all().order_by('name')
        context['house_districts'] = HouseDistrict.objects.all().order_by('name')
        context['commissioner_districts'] = CommissionerDistrict.objects.all().order_by('name')

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

        search_filter = Q()

        if senate_district:
            search_filter |= Q(**{'senate_districts__name': senate_district})

        if house_district:
            search_filter |= Q(**{'house_districts__name': house_district})

        if commissioner_district:
            search_filter |= Q(**{'commissioner_districts__name': commissioner_district})

        return qs.filter(search_filter).distinct()

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


def pong(request):
    """
    Zero-downtime deployment config function.
    """
    from django.http import HttpResponse

    try:
        from django.conf import settings
        DEPLOYMENT_ID = settings.DEPLOYMENT_ID
    except ImportError as e:
        return HttpResponse('Bad deployment: {}'.format(e), status=401)

    return HttpResponse(DEPLOYMENT_ID)
