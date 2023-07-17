from django.shortcuts import render
from rest_framework import viewsets, response
from .serializers import DocumentSerializer
from .models import Document
from rest_framework import permissions


class DocumentViewSets(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = DocumentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return response.Response(serializer.data)



# from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from django.http import HttpResponse
# from .models import Document
# from .serializers import DocumentSerializer
#
# class DocumentUploadView(generics.CreateAPIView):
#     queryset = Document.objects.all()
#     serializer_class = DocumentSerializer
#     permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
# class DocumentDownloadView(generics.RetrieveAPIView):
#     queryset = Document.objects.all()
#     serializer_class = DocumentSerializer
#     permission_classes = [IsAuthenticated]
#
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         file = instance.file
#         response = HttpResponse(file, content_type='application/octet-stream')
#         response['Content-Disposition'] = 'attachment; filename=' + file.name
#         return response
#
# class DocumentShareView(generics.UpdateAPIView):
#     queryset = Document.objects.all()
#     serializer_class = DocumentSerializer
#     permission_classes = [IsAuthenticated]
#
#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         shared_with = request.data.get('shared_with', [])
#         instance.shared_with.set(shared_with)
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)


# permissions.py
# from rest_framework import permissions
#
# class IsOwnerOrShared(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.owner == request.user or request.user in obj.shared_with.all()



