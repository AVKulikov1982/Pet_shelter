# Generated by Django 4.0.3 on 2022-04-28 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_pets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PetType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='тип животного')),
            ],
        ),
        migrations.AddField(
            model_name='petmodel',
            name='type',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_pets.pettype', verbose_name='тип животного'),
        ),
    ]