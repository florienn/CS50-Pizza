# Generated by Django 2.2.7 on 2019-11-26 22:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20191126_2153'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]