# Generated by Django 3.0.8 on 2020-07-22 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_customer_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='phone',
        ),
    ]
