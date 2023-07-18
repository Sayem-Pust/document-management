from django.db import models
import os
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size

    if filesize > 5242880:
        raise ValidationError("You cannot upload file more than 5Mb")
    else:
        return value


class Document(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(validators=[validate_file_size], upload_to='documents/', null=True, blank=True)
    upload_date = models.DateField(null=True, blank=True)
    format = models.CharField(max_length=10, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_documents')
    shared_with = models.ManyToManyField(User, related_name='shared_documents', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.owner.username


# @receiver(pre_save, sender=Document)
# def assign_format_upload_date(sender, instance, **kwargs):
#     if instance.file:
#         name, extension = os.path.splitext(instance.file.name)
#         valid_file_type = ['.pdf', '.jpg', '.jpeg', '.png', '.gif']
#         if extension in valid_file_type:
#             instance.upload_date = datetime.datetime.now().date()
