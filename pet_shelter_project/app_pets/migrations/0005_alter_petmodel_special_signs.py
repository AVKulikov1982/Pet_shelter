# Generated by Django 4.0.3 on 2022-05-26 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_pets', '0004_remove_file_pet_petmodel_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petmodel',
            name='special_signs',
            field=models.CharField(db_index=True, max_length=200, verbose_name='особые приметы животного'),
        ),
    ]
