# Generated by Django 3.1.7 on 2021-03-26 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sub_part', '0021_todolists'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorlists',
            name='phone_number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vendorlists',
            name='total',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vendorlists',
            name='total_sales',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]