from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from belts.models import Belt, BeltGroup
from belts.views import ApprovedUserRequiredMixin

class LandingPageView(TemplateView):
    """
    Renders the landing/login page for unauthenticated users.
    If a user is already authenticated, it redirects them to the dashboard.
    """
    template_name = 'landing.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all groups, prefetching the belts within them to avoid extra queries
        context['belt_groups'] = BeltGroup.objects.prefetch_related('belts').all()
        # Get all belts that do not belong to any group
        context['ungrouped_belts'] = Belt.objects.filter(group__isnull=True)
        return context

class DashboardView(ApprovedUserRequiredMixin, TemplateView):
    """
    Displays the list of all belts on the main dashboard,
    now with support for grouped and ungrouped belts.
    """
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all groups, prefetching the belts within them
        context['belt_groups'] = BeltGroup.objects.prefetch_related('belts').all()
        # Get all belts that do not belong to any group
        context['ungrouped_belts'] = Belt.objects.filter(group__isnull=True)
        return context

# View to serve the manifest.json file
def manifest_json(request):
    return render(request, 'manifest.json', content_type='application/json')

# View to serve the service-worker.js file
def service_worker(request):
    return render(request, 'service-worker.js', content_type='application/javascript')


