# Generated by Django 4.2 on 2023-04-10 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_alter_ticketmodel_identification'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketmodel',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='static/images'),
        ),
    ]