# Generated by Django 2.1.3 on 2019-08-19 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='slug',
            field=models.SlugField(allow_unicode=True, default='', max_length=200, unique=True),
        ),
    ]
