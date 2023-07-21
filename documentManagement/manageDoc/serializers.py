from .models import Document, DocumentVersion
from django.contrib.auth.models import User
from rest_framework import serializers
import os
from docx import Document as DocxDocument
from PyPDF2 import PdfWriter
from fpdf import FPDF


class DocumentVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentVersion
        fields = ('id', 'owner', 'file', 'converted_file', 'timestamp')
        read_only_fields = ['id', 'owner', 'timestamp']

    def create(self, validated_data):
        user = self.context["request"].user
        document = DocumentVersion.objects.create(file=validated_data['file'], owner=user)
        # Perform the conversion
        self.convert_to_pdf(document)
        return document

    def convert_to_pdf(self, document):
        input_path = document.file.path
        output_path = f"{os.path.splitext(input_path)[0]}.pdf"

        # Convert docx to pdf
        doc = DocxDocument(input_path)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        for para in doc.paragraphs:
            pdf.multi_cell(0, 10, txt=para.text)

        pdf.output(output_path)

        # Save the PDF path to the converted_file field
        document.converted_file.name = output_path
        document.save()


class DocumentSerializer(serializers.ModelSerializer):
    shared_with = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False
    )

    class Meta:
        model = Document
        fields = ['id', 'file', 'upload_date', 'format', 'title', 'description',
                  'owner', 'shared_with', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']

    # def update(self, instance, validated_data):
    #     shared_with = validated_data.pop('shared_with', [])
    #     instance.shared_with.set(shared_with)
    #     return super().update(instance, validated_data)
