# Generated by Django 4.0.6 on 2023-04-21 20:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='too_user',
            new_name='too_username',
        ),
    ]