# Generated by Django 4.0.5 on 2022-07-29 05:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_profile_stars_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='stars',
            new_name='follower',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='stars_count',
            new_name='vote',
        ),
    ]
