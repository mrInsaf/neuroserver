from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GeneratedModelViewSet, generate_model

router = DefaultRouter()
router.register(r'generated_models', GeneratedModelViewSet)

from django.urls import path
from . import views

urlpatterns = [
    path('generate_model/', views.generate_model, name='generate_model'),
]

