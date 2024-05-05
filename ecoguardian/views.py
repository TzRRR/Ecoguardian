from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from ecoguardian.models import IncidentCategory, IncidentReport
from .forms import IncidentReportForm, AdminDescriptionForm
from django.core.files.storage import default_storage
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.shortcuts import render

class MainView(TemplateView):
    template_name = "ecoguardian/main.html"


class IncidentReportView(FormView):

    template_name = 'ecoguardian/incident_report.html'
    form_class = IncidentReportForm
    success_url = reverse_lazy('ecoguardian:mainpage')

    def form_valid(self, form):
        # Process the form data
        description = form.cleaned_data['description']
        location = form.cleaned_data['location']
        date = form.cleaned_data['date']
        incident_categories = form.cleaned_data['incident_categories']
        evidence_file = form.cleaned_data['evidence']
        if evidence_file:
            file_path = default_storage.save(f'evidence/{evidence_file.name}', evidence_file)

        incident_category, created = IncidentCategory.objects.get_or_create(name=incident_categories)
        user_pk = self.request.user.email if self.request.user.is_authenticated and self.request.user.email else 'Anonymous User'

        incident_report = IncidentReport(
            description=description,
            location=location,
            incident_category=incident_category,
            date=date,
            evidence=evidence_file,
            user=user_pk
        )
        incident_report.save()

        return super().form_valid(form)
    
class IncidentReportListView(ListView):
    model = IncidentReport
    template_name = 'ecoguardian/incident_reports_view.html'
    context_object_name = 'incident_reports'
        
class UserIncidentReportListView(LoginRequiredMixin, ListView):
    model = IncidentReport
    template_name = 'ecoguardian/user_incident_report_list.html'
    context_object_name = 'user_incident_reports'

    def get_queryset(self):
        return IncidentReport.objects.filter(user=self.request.user.email)
    
class IncidentReportDetailView(DetailView):
    model = IncidentReport
    template_name = 'ecoguardian/incident_report_detail.html'
    context_object_name = 'report'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_form'] = AdminDescriptionForm(instance=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        report = self.get_object()
        form = AdminDescriptionForm(request.POST, instance=report)
        if form.is_valid():
            if report.status == 'New' and request.user.groups.filter(name="site_admin").exists():
                report.status = 'In Progress'
            form.save()
            return redirect('ecoguardian:incident_report_detail', pk=report.pk)
        else:
            return self.render_to_response(self.get_context_data(admin_form=form))

    def get(self, request, *args, **kwargs):
        report = self.get_object()
        if report.status == 'New' and request.user.groups.filter(name="site_admin").exists():
            report.status = 'In Progress'
            report.save()
        return super().get(request, *args, **kwargs)
    
class IncidentReportDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        report_id = request.POST.get('report_id')
        report = IncidentReport.objects.filter(id=report_id, user=request.user.email).first()
        if report:
            report.delete()
        return HttpResponseRedirect(reverse_lazy('ecoguardian:user_incident_reports'))