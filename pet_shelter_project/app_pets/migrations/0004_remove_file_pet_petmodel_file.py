# Generated by Django 4.0.3 on 2022-05-24 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_pets', '0003_alter_petmodel_published_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='pet',
        ),
        migrations.AddField(
            model_name='petmodel',
            name='file',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_pets.file', verbose_name='фото животного'),
        ),
    ]
