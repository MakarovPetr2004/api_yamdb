# Generated by Django 3.2 on 2023-05-18 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20230518_1743'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={},
        ),
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.category'),
        ),
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(blank=True, related_name='titles', to='reviews.Genre'),
        ),
    ]