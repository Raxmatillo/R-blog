# Generated by Django 4.0.5 on 2022-07-31 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_alter_post_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=200, null=True, verbose_name='URL'),
        ),
    ]
