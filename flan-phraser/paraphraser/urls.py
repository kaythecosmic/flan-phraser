from django.urls import path
from . import views

urlpatterns = [
    path("", views.BartesianInput, name="BartesianInput"),
    path("output", views.Paraphraser, name="Paraphraser"),
]
