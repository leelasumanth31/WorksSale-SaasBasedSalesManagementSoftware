# Generated by Django 3.1.7 on 2021-03-25 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sub_part', '0016_auto_20210325_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerlists',
            name='phone_number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]