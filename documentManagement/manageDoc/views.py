from django.shortcuts import render
from rest_framework import viewsets, response, generics, status
from .serializers import DocumentSerializer, DocumentVersionSerializer
from .models import Document, DocumentVersion
from rest_framework import permissions
from .permissions import IsOwnerOrShared, UpdateOwn, OwnerAdmin
from django.http import HttpResponse
import os
import datetime
from django.db.models import Q
from rest_framework.mixins import ListModelMixin, DestroyModelMixin
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class DocumentViewSets(viewsets.ModelViewSet):
    """ API Group of Document get, post, put, patch and delete with permission """
    permission_classes = [IsOwnerOrShared]
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get_permissions(self):
        if self.action in ['delete', 'update']:
            self.permission_classes = [OwnerAdmin]
        return super(DocumentViewSets, self).get_permissions()

    def create(self, request, *args, **kwargs):
        """ post title, description, Upload a file on specific type and size (pdf, jpeg, png, doc, docx) and size not more
                                      then 5mb  """
        data = request.data
        valid_file_type = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.doc', '.docx']
        if data.get('file'):
            name, extension = os.path.splitext(data.get('file').name)
            if extension in valid_file_type:
                filesize = request.data.get('file').size
                if filesize > 5242880:
                    return response.Response({
                        "error": "You cannot upload file more than 5Mb"
                    })
                else:
                    serializer = DocumentSerializer(data=request.data, context={'request': request})
                    if serializer.is_valid():
                        serializer.save(owner=self.request.user, format=extension,
                                        upload_date=datetime.datetime.now().date())
                        return response.Response(serializer.data)
                    else:
                        print(serializer.errors)
                        return response.Response({
                            "error": "Invalid data"
                        })
            else:
                return response.Response({
                    "error": "Invalid file type. File must be pdf, jpg, jpeg, png, gif, doc, docx"
                })
        else:
            serializer = DocumentSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(owner=self.request.user)
                return response.Response(serializer.data)
            else:
                print(serializer.errors)
                return response.Response({
                    "error": "Invalid data"
                })

        # serializer = DocumentSerializer(data=data)
        # if serializer.is_valid():
        #     serializer.save(owner=request.user)
        #     return response.Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """ List of all documents created by the user and search using title, description, format and upload date with
            permissions """
        qs = None
        search = request.query_params.get('search', '')
        date_search = request.query_params.get('date_search', '')
        if request.user.is_superuser:
            qs = self.queryset.all()
        elif request.user:
            qs = self.queryset.filter(owner=request.user)
        qs = qs.filter(Q(title__icontains=search) | Q(description__icontains=search) |
                       Q(format__icontains=search))
        if date_search:
            print(date_search)
            qs = qs.filter(Q(upload_date__exact=date_search))
        serializer = self.serializer_class(qs, many=True)
        return response.Response(serializer.data)


class DocumentUploadView(generics.CreateAPIView):
    """ Upload a file on specific type and size (pdf, jpeg, png, doc, docx) and size not more
                              then 5mb  """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsOwnerOrShared]

    # def perform_create(self, serializer):
    #     print(self.request.data.get('file'))
    #     valid_file_type = ['pdf', 'jpg', 'jpeg', 'png', 'gif']
    #     if self.request.data.get('file'):
    #         name, extension = os.path.splitext(self.request.data.get('file').name)
    #         if extension in valid_file_type:
    #             serializer.save(owner=self.request.user, format=extension)
    #         else:
    #             return response.Response({
    #                 "error": "Invalid file type"
    #             })
    #         print(name, extension)
    # serializer.save(owner=self.request.user, format=extension)

    def create(self, request, *args, **kwargs):
        valid_file_type = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.doc', '.docx']
        if request.data.get('file'):
            name, extension = os.path.splitext(self.request.data.get('file').name)
            if extension in valid_file_type:
                filesize = request.data.get('file').size
                if filesize > 5242880:
                    return response.Response({
                        "error": "You cannot upload file more than 5Mb"
                    })
                else:
                    serializer = DocumentSerializer(data=request.data, context={'request': request})
                    if serializer.is_valid():
                        serializer.save(owner=self.request.user, format=extension,
                                        upload_date=datetime.datetime.now().date())
                        return response.Response(serializer.data)
                    else:
                        print(serializer.errors)
                        return response.Response({
                            "error": "Invalid data"
                        })
            else:
                return response.Response({
                    "error": "Invalid file type. File must be pdf, jpg, jpeg, png, gif, doc, docx"
                })


class DocumentDownloadView(generics.RetrieveAPIView):
    """ Download document with various permissions (download himself, shared persons and admin) """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsOwnerOrShared]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        file = instance.file
        response = HttpResponse(file, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=' + file.name
        return response


class DocumentShareView(generics.UpdateAPIView):
    """ Share document with another user """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [UpdateOwn]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        shared_with = request.data.getlist('shared_with', [])
        instance.shared_with.set(shared_with)
        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)


class DocumentVersionListCreateView(generics.ListCreateAPIView):

    queryset = DocumentVersion.objects.all()
    serializer_class = DocumentVersionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        # methods=['GET'],
        operation_description="Post a docx file to convert pdf",

        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['file'],
            title="Post object",
            properties={
                'file': openapi.Schema(type=openapi.TYPE_FILE),
            },
        ),
        responses={200: 'success'}
    )
    def post(self, request, *args, **kwargs):
        serializer = DocumentVersionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        """ Get All Conversion file for a user versioning """
        if request.user:
            qs = self.queryset.filter(owner=request.user)
            serializer = self.serializer_class(qs, many=True, context={'request': request})
            return response.Response(serializer.data)


class ConvertedDocumentDownloadView(generics.RetrieveAPIView):
    """ Download Conversion file for a user versioning """
    queryset = DocumentVersion.objects.all()
    serializer_class = DocumentVersionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        file = instance.converted_file
        response = HttpResponse(file, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=' + file.name
        return response


@swagger_auto_schema(responses={200: DocumentVersionSerializer(many=True)})
class UserConvertDocumentsViewSets(viewsets.GenericViewSet, ListModelMixin, DestroyModelMixin):
    """ Delete Conversion file for a user versioning """
    queryset = DocumentVersion.objects.all()
    serializer_class = DocumentVersionSerializer
    permission_classes = [UpdateOwn]

    def list(self, request, *args, **kwargs):
        """ Get All Conversion file for a user versioning """
        if request.user:
            qs = self.queryset.filter(owner=request.user)
            serializer = self.serializer_class(qs, many=True, context={'request': request})
            return response.Response(serializer.data)
