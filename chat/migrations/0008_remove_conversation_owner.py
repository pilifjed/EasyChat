# Generated by Django 2.0.5 on 2018-05-27 21:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_auto_20180527_2142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversation',
            name='owner',
        ),
    ]