# Generated by Django 4.2.3 on 2023-07-18 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manageDoc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
