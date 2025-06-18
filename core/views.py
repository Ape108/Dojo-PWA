from django.shortcuts import render
from django.views.generic import ListView
from belts.models import Belt

class HomeView(ListView):
    """Displays the list of all belts on the main menu."""
    model = Belt
    template_name = 'home.html'
    context_object_name = 'belts'

# View to serve the manifest.json file
def manifest_json(request):
    return render(request, 'manifest.json', content_type='application/json')

# View to serve the service-worker.js file
def service_worker(request):
    return render(request, 'service-worker.js', content_type='application/javascript')


