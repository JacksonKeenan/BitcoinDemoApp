# Generated by Django 4.0.4 on 2022-04-26 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_senderwallet_total_received_senderwallet_total_sent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='senderwallet',
            name='private',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='senderwallet',
            name='public',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='senderwallet',
            name='address',
            field=models.CharField(default='', max_length=150),
        ),
    ]
