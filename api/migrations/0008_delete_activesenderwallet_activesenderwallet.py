# Generated by Django 4.0.4 on 2022-05-04 00:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_activesenderwallet_address_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ActiveSenderWallet',
        ),
        migrations.CreateModel(
            name='ActiveSenderWallet',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('api.senderwallet',),
        ),
    ]
