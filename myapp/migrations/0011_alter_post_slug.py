# Generated by Django 4.0.5 on 2022-07-31 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_alter_post_content_alter_post_slug_alter_post_tags_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=200, null=True, unique=True, verbose_name='URL'),
        ),
    ]
