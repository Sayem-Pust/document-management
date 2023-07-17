from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSets

router = DefaultRouter()
router.register('documents', DocumentViewSets, basename='documents')

urlpatterns = [
    path("", include(router.urls)),
]
