# Generated by Django 5.1.2 on 2024-10-24 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection_service', '0002_remove_collection_labels_alter_collection_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='labels',
            field=models.JSONField(default=list),
        ),
    ]
