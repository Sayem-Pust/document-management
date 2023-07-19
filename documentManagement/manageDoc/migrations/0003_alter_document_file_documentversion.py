# Generated by Django 4.2.3 on 2023-07-19 15:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import manageDoc.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('manageDoc', '0002_alter_document_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='documents/', validators=[manageDoc.models.validate_file_size]),
        ),
        migrations.CreateModel(
            name='DocumentVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='documents/')),
                ('converted_file', models.FileField(blank=True, null=True, upload_to='converted_documents/')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_conversion', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
