# Generated by Django 5.1.3 on 2024-12-26 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection_service', '0005_remove_collection_recipes_alter_collection_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='recipes',
            field=models.JSONField(default=list),
        ),
    ]
