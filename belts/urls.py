# belts/urls.py
from django.urls import path
from . import views

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