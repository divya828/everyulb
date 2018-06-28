# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-12 15:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gMapsIntegration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LandfillsFinalSiteConceptualModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s0', models.TextField(default='')),
                ('s1', models.TextField(default='')),
                ('s2', models.TextField(default='')),
                ('s3', models.TextField(default='')),
                ('s4', models.TextField(default='')),
                ('s5', models.TextField(default='')),
                ('s6', models.TextField(default='')),
                ('s7', models.TextField(default='')),
                ('s8', models.TextField(default='')),
                ('s9', models.TextField(default='')),
                ('s10', models.TextField(default='')),
                ('s11', models.TextField(default='')),
                ('landfill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='landfill_final_site_conceptual_model', to='gMapsIntegration.Landfills')),
            ],
            options={
                'ordering': ['landfill'],
            },
        ),
    ]