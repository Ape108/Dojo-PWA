# belts/views.py

import random
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Belt, Technique, Tag, TechniqueTagAssignment
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Tag
from django import forms
from django.views.generic import CreateView, UpdateView, DeleteView
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Prefetch

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
        """Add next/previous belt links and supplemental materials to the context for easy navigation."""
        context = super().get_context_data(**kwargs)
        all_belts = list(Belt.objects.all())
        try:
            current_index = all_belts.index(self.object)
            context['prev_belt'] = all_belts[current_index - 1] if current_index > 0 else None
            context['next_belt'] = all_belts[current_index + 1] if current_index < len(all_belts) - 1 else None
        except ValueError:
            context['prev_belt'] = None
            context['next_belt'] = None
        # Add supplemental materials for this belt
        context['supplemental_materials'] = self.object.supplemental_materials.all()
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
        self.belt = get_object_or_404(Belt, pk=self.kwargs['pk'])
        queryset = Technique.objects.filter(belt=self.belt)
        tag_ids = self.request.GET.getlist('tag')
        if tag_ids:
            # Filter techniques that have ALL selected tags (global or user-specific)
            for tag_id in tag_ids:
                queryset = queryset.filter(
                    Q(tag_assignments__tag_id=tag_id) &
                    (Q(tag_assignments__user=self.request.user) | Q(tag_assignments__user__isnull=True))
                )
        # Prefetch tag assignments for current user and global
        queryset = queryset.prefetch_related(
            Prefetch(
                'tag_assignments',
                queryset=TechniqueTagAssignment.objects.filter(
                    Q(user=self.request.user) | Q(user__isnull=True)
                ).select_related('tag'),
                to_attr='filtered_tag_assignments'
            )
        )
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['belt'] = self.belt
        # Provide global tags (teacher-published)
        context['global_tags'] = Tag.objects.filter(is_global=True)
        # Provide user tags (student-created)
        context['user_tags'] = Tag.objects.filter(is_global=False, created_by=self.request.user)
        # Pass selected tag IDs for UI state
        context['selected_tag_ids'] = [int(t) for t in self.request.GET.getlist('tag') if t.isdigit()]
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

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tag name'}),
        }

class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'belts/tag_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        # Only allow global tag creation if ?global=1 and user is teacher/admin
        make_global = self.request.GET.get('global') == '1'
        if make_global and hasattr(self.request.user, 'user_type') and (self.request.user.user_type == 'teacher' or self.request.user.user_type == 'admin' or self.request.user.is_superuser):
            form.instance.is_global = True
        else:
            form.instance.is_global = False
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('belts:flashcard_list', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context

class TagUpdateView(LoginRequiredMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'belts/tag_form.html'

    def get_queryset(self):
        return Tag.objects.filter(created_by=self.request.user, is_global=False)

    def get_success_url(self):
        return reverse_lazy('belts:flashcard_list', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context

class TagDeleteView(LoginRequiredMixin, DeleteView):
    model = Tag
    template_name = 'belts/tag_confirm_delete.html'

    def get_queryset(self):
        return Tag.objects.filter(created_by=self.request.user, is_global=False)

    def get_success_url(self):
        return reverse_lazy('belts:flashcard_list', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context

class TechniqueTagAssignAjaxView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        technique_id = request.POST.get('technique_id')
        tag_ids = request.POST.getlist('tag_ids[]')
        try:
            technique = Technique.objects.get(id=technique_id)
        except Technique.DoesNotExist:
            return HttpResponseBadRequest('Technique not found')
        # Only allow assigning global tags or tags owned by the user
        allowed_tags = Tag.objects.filter(Q(is_global=True) | Q(created_by=request.user))
        tags_to_assign = allowed_tags.filter(id__in=tag_ids)
        # Remove all tag assignments for this user (or global) for this technique
        TechniqueTagAssignment.objects.filter(technique=technique).filter(Q(user=request.user) | Q(user__isnull=True)).delete()
        # Re-add assignments
        for tag in tags_to_assign:
            # Always assign global tags as global (user=None)
            TechniqueTagAssignment.objects.create(
                technique=technique,
                tag=tag,
                user=None if tag.is_global else request.user
            )
        # Return updated tag list for this technique
        updated_assignments = technique.tag_assignments.filter(Q(user=request.user) | Q(user__isnull=True)).select_related('tag')
        tag_data = [
            {
                'name': ta.tag.name,
                'is_global': ta.tag.is_global,
                'id': ta.tag.id,
            } for ta in updated_assignments
        ]
        return JsonResponse({'tags': tag_data})

class BulkTagEditorView(LoginRequiredMixin, TemplateView):
    template_name = 'belts/bulk_tag_editor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        belt = get_object_or_404(Belt, pk=self.kwargs['pk'])
        context['belt'] = belt
        context['techniques'] = Technique.objects.filter(belt=belt)
        context['global_tags'] = Tag.objects.filter(is_global=True)
        context['user_tags'] = Tag.objects.filter(created_by=self.request.user, is_global=False)
        return context

@method_decorator(csrf_exempt, name='dispatch')
class BulkTagToggleAjaxView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        tag_id = request.POST.get('tag_id')
        checked_technique_ids = set(request.POST.getlist('technique_ids[]'))
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            return HttpResponseBadRequest('Tag not found')
        # Only allow toggling tags the user owns or global tags
        if not (tag.is_global or tag.created_by == request.user):
            return HttpResponseBadRequest('Not allowed')
        # Get all techniques for this belt
        belt_id = request.POST.get('belt_id')
        if belt_id:
            all_techniques = Technique.objects.filter(belt_id=belt_id)
        else:
            all_techniques = Technique.objects.all()
        for technique in all_techniques:
            has_tag = TechniqueTagAssignment.objects.filter(
                technique=technique,
                tag=tag,
                user=None if tag.is_global else request.user
            ).exists()
            if str(technique.id) in checked_technique_ids:
                if not has_tag:
                    TechniqueTagAssignment.objects.create(
                        technique=technique,
                        tag=tag,
                        user=None if tag.is_global else request.user
                    )
            else:
                if has_tag:
                    TechniqueTagAssignment.objects.filter(
                        technique=technique,
                        tag=tag,
                        user=None if tag.is_global else request.user
                    ).delete()
        return JsonResponse({'success': True})
