# belts/views.py

import random
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Belt, Technique

class ApprovedUserRequiredMixin(LoginRequiredMixin):
    """Custom mixin to verify a user is logged in AND approved by an admin."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        # Admins and staff can always access. Students must be approved.
        if not request.user.is_approved and not request.user.is_staff:
            return render(request, 'account/pending_approval.html')
        return super().dispatch(request, *args, **kwargs)

class BeltDetailView(ApprovedUserRequiredMixin, DetailView):
    """Displays the main page for a single belt."""
    model = Belt
    template_name = 'belts/belt_detail.html'
    context_object_name = 'belt'

    def get_context_data(self, **kwargs):
        """Add next/previous belt links to the context for easy navigation."""
        context = super().get_context_data(**kwargs)
        all_belts = list(Belt.objects.all())
        try:
            current_index = all_belts.index(self.object)
            context['prev_belt'] = all_belts[current_index - 1] if current_index > 0 else None
            context['next_belt'] = all_belts[current_index + 1] if current_index < len(all_belts) - 1 else None
        except ValueError:
            context['prev_belt'] = None
            context['next_belt'] = None
        return context

class BeltManualView(ApprovedUserRequiredMixin, DetailView):
    """Displays the embedded PDF training manual for a belt."""
    model = Belt
    template_name = 'belts/pdf_viewer.html'
    context_object_name = 'belt'

class FlashcardSequentialView(ApprovedUserRequiredMixin, ListView):
    """Displays all techniques for a belt in order (Browse Mode)."""
    template_name = 'belts/flashcard_list.html'
    context_object_name = 'techniques'

    def get_queryset(self):
        # FIX: Changed self.kwargs['belt_pk'] to self.kwargs['pk']
        self.belt = get_object_or_404(Belt, pk=self.kwargs['pk'])
        return Technique.objects.filter(belt=self.belt)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['belt'] = self.belt
        return context

class FlashcardRandomView(ApprovedUserRequiredMixin, DetailView):
    """Displays one random technique from a belt (Flashcard Mode)."""
    model = Technique
    template_name = 'belts/flashcard_random.html'
    context_object_name = 'technique'

    def get_object(self, queryset=None):
        """Override to select a random technique from the specified belt"""
        # FIX: Changed self.kwargs['belt_pk'] to self.kwargs['pk']
        belt_pk = self.kwargs['pk']
        technique_ids = list(Technique.objects.filter(belt__pk=belt_pk).values_list('id', flat=True))
        if not technique_ids:
            return None
        random_id = random.choice(technique_ids)
        return get_object_or_404(Technique, pk=random_id)

    def get_context_data(self, **kwargs):
        """Add the belt to the context for navigation."""
        context = super().get_context_data(**kwargs)
        # FIX: Changed self.kwargs['belt_pk'] to self.kwargs['pk']
        # Also simplified this logic. If self.object (the technique) exists, we can get the belt from it directly.
        if self.object:
            context['belt'] = self.object.belt
        else:
            # Fallback for when there are no techniques for a belt.
            context['belt'] = get_object_or_404(Belt, pk=self.kwargs['pk'])
        return context
