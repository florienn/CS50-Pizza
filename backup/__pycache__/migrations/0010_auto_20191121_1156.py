# Generated by Django 2.2.7 on 2019-11-21 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_order2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='type',
        ),
        migrations.DeleteModel(
            name='Order2',
        ),
        migrations.DeleteModel(
            name='Type',
        ),
    ]
