from .models import Document
from django.contrib.auth.models import User
from rest_framework import serializers


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

    def update(self, instance, validated_data):
        shared_with = validated_data.pop('shared_with', [])
        instance.shared_with.set(shared_with)
        return super().update(instance, validated_data)
