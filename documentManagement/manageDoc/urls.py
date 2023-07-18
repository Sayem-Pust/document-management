from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSets, DocumentUploadView, DocumentDownloadView, DocumentShareView

router = DefaultRouter()
router.register('documents', DocumentViewSets, basename='documents')

urlpatterns = [
    path("", include(router.urls)),
    path('upload/', DocumentUploadView.as_view(), name='upload'),
    path('download/<int:pk>/', DocumentDownloadView.as_view(), name='download'),
    path('share/<int:pk>/', DocumentShareView.as_view(), name='share'),
]
