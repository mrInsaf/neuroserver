from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from models.views import GeneratedModelViewSet, generate_model_view
from accounts.views import RegisterView, LoginView

router = DefaultRouter()
router.register(r'generated_models', GeneratedModelViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/', include(router.urls)),
    path('api/generate_model/', generate_model_view, name='generate_model'),

]
