# Generated by Django 5.0.6 on 2024-06-14 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='repository',
            new_name='sources',
        ),
    ]