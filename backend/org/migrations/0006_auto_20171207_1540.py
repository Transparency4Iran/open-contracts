# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-07 15:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('org', '0005_synonym_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budgets', to='org.Organization')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='budget',
            unique_together=set([('organization', 'year')]),
        ),
    ]