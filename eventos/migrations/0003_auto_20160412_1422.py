# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-12 12:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0002_auto_20160412_1417'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='evento',
            table='eventos_evento',
        ),
        migrations.AlterModelTable(
            name='horario',
            table='eventos_horario',
        ),
        migrations.AlterModelTable(
            name='tipoevento',
            table='eventos_tipoevento',
        ),
    ]
