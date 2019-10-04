# Generated by Django 2.1.10 on 2019-09-25 08:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_auto_20190920_1559'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addr_name', models.CharField(max_length=30)),
                ('zip', models.CharField(max_length=20)),
                ('addr1', models.CharField(max_length=250)),
                ('addr2', models.CharField(max_length=100)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SmsSend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg_type', models.CharField(choices=[('sms', 'sms')], default='sms', max_length=3)),
                ('msg_getter', models.CharField(max_length=20)),
                ('msg_sender', models.CharField(default='01056373374', max_length=20)),
                ('msg_text', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='Phone',
        ),
    ]
