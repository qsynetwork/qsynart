# Generated by Django 3.2.6 on 2021-08-18 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainwebsite', '0003_auto_20210816_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderhistory',
            name='ketto_transaction_details',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
