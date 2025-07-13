# belts/urls.py
from django.urls import path
from . import views
from .views import TagCreateView, TagUpdateView, TagDeleteView

app_name = 'belts'
urlpatterns = [
    # e.g., /belts/1/
    path('<int:pk>/', views.BeltDetailView.as_view(), name='detail'),
    # e.g., /belts/1/manual/
    path('<int:pk>/manual/', views.BeltManualView.as_view(), name='manual'),
    # e.g., /belts/1/flashcards/
    path('<int:pk>/flashcards/', views.FlashcardSequentialView.as_view(), name='flashcard_sequential'),
    # e.g., /belts/1/flashcards/random/
    path('<int:pk>/flashcards/random/', views.FlashcardRandomView.as_view(), name='flashcard_random'),
]

urlpatterns += [
    path('<int:pk>/tags/add/', TagCreateView.as_view(), name='tag_add'),
    path('<int:pk>/tags/<int:tag_id>/edit/', TagUpdateView.as_view(), name='tag_edit'),
    path('<int:pk>/tags/<int:tag_id>/delete/', TagDeleteView.as_view(), name='tag_delete'),
    path('<int:pk>/flashcards/', views.FlashcardSequentialView.as_view(), name='flashcard_list'),
    path('ajax/assign_tags/', views.TechniqueTagAssignAjaxView.as_view(), name='ajax_assign_tags'),
    path('<int:pk>/bulk-tag-editor/', views.BulkTagEditorView.as_view(), name='bulk_tag_editor'),
    path('ajax/bulk_tag_toggle/', views.BulkTagToggleAjaxView.as_view(), name='ajax_bulk_tag_toggle'),
]