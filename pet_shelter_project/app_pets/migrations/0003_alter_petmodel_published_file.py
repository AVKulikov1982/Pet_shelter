# Generated by Django 4.0.3 on 2022-05-17 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_pets', '0002_pettype_petmodel_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petmodel',
            name='published',
            field=models.BooleanField(default=False, verbose_name='опубликовать'),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='files/%Y-%m-%d')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('pet', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='app_pets.petmodel')),
            ],
        ),
    ]
