# Generated by Django 3.1.7 on 2021-03-25 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sub_part', '0015_productslists_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerlists',
            name='total',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customerlists',
            name='total_sales',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]