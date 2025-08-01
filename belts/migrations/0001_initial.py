# Generated by Django 5.2.3 on 2025-06-18 19:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Belt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='e.g., Orange, Brown 3, Black 1', max_length=100, unique=True)),
                ('display_order', models.IntegerField(help_text='Logical order for sorting belts.', unique=True)),
                ('pdf_file', models.FileField(blank=True, help_text='The PDF manual for this belt.', null=True, upload_to='pdfs/')),
            ],
            options={
                'ordering': ['display_order'],
            },
        ),
        migrations.CreateModel(
            name='Technique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('video_file', models.FileField(blank=True, null=True, upload_to='videos/')),
                ('order_in_belt', models.IntegerField(help_text='The sequential order of the technique within the belt.')),
                ('belt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='techniques', to='belts.belt')),
            ],
            options={
                'ordering': ['belt__display_order', 'order_in_belt'],
                'unique_together': {('belt', 'order_in_belt')},
            },
        ),
    ]
